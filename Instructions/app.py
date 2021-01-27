import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import distinct

from flask import Flask, jsonify

#set up database

engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

#set up Flask

app = Flask(__name__)



@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
    )


# FLask routes
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query measurement table for date and prcp 
    results = session.query(Measurement.date, Measurement.prcp).all()

    #close the session
    session.close()

    #Convert the query results to a dictionary using date as the key and prcp as the value
    all_data = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"]= date
        prcp_dict["prcp"]= prcp
        all_data.append(prcp_dict)

    return jsonify(all_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Return a JSON list of stations from the dataset
    list_stations = session.query(Measurement.station).distinct()

    #close session

    all_stations = []

    for station in list_stations:
        station_dict = {}
        station_dict["Stations"]= station
        all_stations.append(station_dict)

     return jsonify(all_stations)   
     












    

    













if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1",port=8060)
