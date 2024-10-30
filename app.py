# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt
import re
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")


# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)

# Save references to each table

Station = Base.classes.station 
Measurement = Base.classes.measurement 

# Create our session (link) from Python to the DB

session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return(
        f"Welcome to Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/1.0/tobs<br/>"
        f"/api/1.0/start (enter as YYYY-MM-DD)<br/>)"
        f"/api/1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    twelve_months = dt.date(2017, 8, 23)-dt.timedelta(days=365)
    last_date = dt.date(twelve_months.year, twelve_months.month, twelve_months.day)
    pre_score = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_date).order_by(Measurement.date.desc()).all()
    p_dict = dict(results)

    print("Result for precipitation - {p_dict}")
    print("Outside precipitation zone.")
    return jsonify(p_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    queryresult = session.query(*sel).all()
    session.close()

    stations = []
    for station, name, lat, lon, el in queryresult:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    queryresult = session.query( Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date>='2016-08-23').all()

    tob_obs = []
    for date, tobs in queryresult:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['Tobs'] = tobs
        tob_obs.append(tobs_dict)
    return jsonify(tob_obs)

@app.route("/api/v1.0/<start>")
def temps_start(start):
    session = Session(engine)
    temp_result = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    temps = []
    for min_temp, max_temp, avg_temp in temp_result:
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)

    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    session = Session(engine)
    start_end_result = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<= end).all()
    session.close()

    temps = []
    for min_temp, avg_temp, max_temp in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)
    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)
