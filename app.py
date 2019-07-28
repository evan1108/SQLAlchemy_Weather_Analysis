import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
# @TODO: Initialize your Flask app here
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# @TODO: Complete the routes for your app here

@app.route("/")
def home():
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    twelve_mo_rain = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date > '2016-08-23').filter(Measurement.date < '2017-08-24')
    date_rain = {key:value for (value,key) in twelve_mo_rain}
    return jsonify(date_rain)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    active_stations = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).all()
    return jsonify(active_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_freq = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').filter(Measurement.date >'2016-08-23').all()
    return jsonify(tobs_freq)

@app.route("/api/v1.0/<start>")
def startonly(start):
    session = Session(engine)
    temp_info = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start)
    return (f"Lowest temp: {temp_info[0][0]} <br/>"
            f"Average temp: {temp_info[0][1]} <br/>"
            f"High temp: {temp_info[0][2]} <br/>"
        ) 

@app.route("/api/v1.0/<start>/<end>")
def startandend(start, end):
    session = Session(engine)
    temp_range_info = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return (f"Lowest temp: {temp_range_info[0][0]} <br/>"
            f"Average temp: {temp_range_info[0][1]} <br/>"
            f"High temp: {temp_range_info[0][2]} <br/>"
        )
if __name__ == "__main__":
    app.run(debug=True)

