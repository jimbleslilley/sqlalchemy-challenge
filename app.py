import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date<br/>"
        f"/api/v1.0/start date/end date<br/>"
        f"Dates to be typed yyyy-mm-dd"
    )

#################################################
# /api/v1.0/precipitation
#################################################

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    #Query to get dates and precipitation
    data = session.query(Measurement.date,Measurement.prcp).all()

    session.close()
    
    #create json ready dictionary for dates and precipitation
    list_date_precip = []
    for date, precip in data:
        dict_dates = {}
        dict_dates[date] = precip
        list_date_precip.append(dict_dates)

    return jsonify(list_date_precip)

#################################################
# /api/v1.0/stations
#################################################

# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    #Get all station names,
    data = session.query(Station.station).all()

    session.close()


    # Convert list of tuples into normal list
    list_station = list(np.ravel(data,order="k"))

    return jsonify(list_station)

#################################################
# /api/v1.0/tobs
#################################################

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    # Return most recent date minus one year 
    latest_date = (session.query(func.max(Measurement.date)).scalar())
    date_last_year = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
    session.close()

    




if __name__ == '__main__':
    app.run(debug=True)
