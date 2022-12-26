from flask import Flask, render_template, request 
import sqlite3

app = Flask(__name__)

def getconn():
    return sqlite3.connect("flights.db")

@app.route("/")
def flights():
    return """<h1>Flights App</h1>
    <ul>
    <li><a href=listflight>List</a></li>
    </ul>"""

@app.route('/listflight')
def list_flights():
    conn = getconn()
    cur = conn.cursor()
    rows = cur.execute("select id, airline, flight, airportfrom, airportto, dayofweek, time, length, delay from flights")
    html = "<h3>Flights</h3><table>\n" 
    for row in rows:
        html += ("<tr>" 
        + "<td align=right>%s"
        + "<td align=right>%s"
        + "<td align=right>%s"
        + "<td align=right>%s"
        + "<td align=right>%s"
        + "<td align=right>%s"
        + "<td align=right>%s"
        + "<td align=right>%s"
        + "<td align=right>%s\n") % row
    conn.close()
    return html + "</table>\n"

import pandas as pd
import numpy as np

df = pd.read_csv("Airlines_processed.csv")
df.head()

data = np.asarray(df)

conn = sqlite3.connect("flights.db")
cur = conn.cursor()
cur.execute("drop table if exists flights")
conn.commit()

fout = open("tmpdat.csv", "w")
fout.write("id,airline,flight,airportfrom,airportto,dayofweek,time,length,delay\n")
for x in data:
    fout.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % tuple(x[:9]))
fout.close()
pd.read_csv("tmpdat.csv").to_sql("flights", conn, index = False)
conn.commit()

app.run(port=4040)
