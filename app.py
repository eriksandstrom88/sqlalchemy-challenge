from flask import Flask, jsonify
# %matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)
# session = Session(bind=engine)
# last_measure_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
year_ago = dt.date(2017,8,23) - dt.timedelta(days=366)
# last_twelve_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).all()
# dates = [each_date[0] for each_date in last_twelve_query]
# precip = [each_precip[1] for each_precip in last_twelve_query]
# last_twelve_df = pd.DataFrame(last_twelve_query)
# last_twelve_df = last_twelve_df.set_index('date')
# grouped_last_twelve = last_twelve_df.groupby(['date']).mean()
# precip_dict = dict(zip(grouped_last_twelve.index,grouped_last_twelve.prcp))

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (f"Welcome to Erik's Hawiian Weather Station API!<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>")


@app.route("/api/v1.0/precipitation")
def about():
    print("Server received request for 'precipitation' data...")
    session=Session(engine)
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=366)
    last_twelve_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).all()
    last_twelve_df = pd.DataFrame(last_twelve_query)
    last_twelve_df = last_twelve_df.set_index('date')
    grouped_last_twelve = last_twelve_df.groupby(['date']).mean()
    precip_dict = dict(zip(grouped_last_twelve.index,grouped_last_twelve.prcp))
    session.close()
    return jsonify(precip_dict)
    

@app.route("/api/v1.0/stations")
def contact():
    print("Server received request for 'stations' data...")
    session=Session(engine)
    stations_display = session.query(Station.id, Station.station, Station.name, Station.latitude,\
    Station.longitude, Station.elevation).all()
    session.close()
    return jsonify(stations_display)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' data...")
    session=Session(engine)
    most_tobs_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_ago)\
    .filter(Measurement.station == 'USC00519281').all()
    session.close()
    return jsonify(most_tobs_station)

@app.route("/api/v1.0/<start>")
def start_query(start):
    session=Session(engine)
    tobs_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs))\
    .filter(Measurement.date>=start).all()
    min_tobs = tobs_query[0][0]
    max_tobs = tobs_query[0][1]
    avg_tobs = tobs_query[0][2]
    tobs_query_dict = [{"Start Date": start, "Max Temp": max_tobs, "Min Temp": min_tobs, "Avg Temp":avg_tobs}]
    session.close()
    return jsonify(tobs_query_dict)

@app.route("/api/v1.0/<start>/<end>")
def se_query(start, end):
    session=Session(engine)
    se_tobs_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs))\
    .filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    se_min_tobs = se_tobs_query[0][0]
    se_max_tobs = se_tobs_query[0][1]
    se_avg_tobs = se_tobs_query[0][2]
    se_tobs_query_dict = [{"0.Start Date": start, "1.End Date": end, "2.Max Temp": se_max_tobs, 
    "3.Min Temp": se_min_tobs, "4.Avg Temp":se_avg_tobs}]
    session.close()
    return jsonify(se_tobs_query_dict)


if __name__ == "__main__":
    app.run(debug=True)
