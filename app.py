#%%
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#%%
# Set up engine
engine = create_engine("sqlite:///hawaii.sqlite")

#%%
# Reflect tables
Base = automap_base()
Base.prepare(engine, reflect=True)

#%%
# Making references
Measurement = Base.classes.measurement
Station = Base.classes.station

#%%
# Create session
session = Session(engine)

#%%
# Create flask
app = Flask(__name__)

#%%
# Define Data Route
@app.route("/")
def welcome():
    return(
    '''
    <h1>Welcome to the Climate Analysis API!</h1>
    <h2>Available Routes:</h2>
    <a href="/api/v1.0/precipitation">Precipitation</a><br>
    <a href="/api/v1.0/stations">Stations</a><br>
    <a href="/api/v1.0/tobs">Temperature</a><br>
    <a href="/api/v1.0/temp/2017-06-01/2017-06-30">Weather from 6/1/2017 - 6/30/2017</a><br>
    ''')

#%%
# Create precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


#%%
# Create stations route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# %%
# Create temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results=session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# %%
# Create statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end: 
        results = session.query(*sel).\
		    filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
	        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
 

# %%

# %%
