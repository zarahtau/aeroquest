from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased

# intialize flask app
app = Flask(__name__)

# Set the database URI 
#------------------------------------------------------------------------
# ONCE TABLES ARE CREATED, ADD YOUR DATABASE PATH:  'sqlite:///absolute/path/to/database/file.db
#------------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/zarahtaufique/Desktop/SJSU/Year3Semester2/CMPE131/airportsdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Create class to connect to the flask app
#------------------------------------------------------------------------
#                           Flights Table
#------------------------------------------------------------------------
class Flights(db.Model):
    __tablename__ = 'flights'
    Flight_id = db.Column(db.Integer, primary_key=True)
    Source_Airport_Code = db.Column(db.String, db.ForeignKey('airports.airport_code'))
    Dest_Airport_Code = db.Column(db.String, db.ForeignKey('airports.airport_code'))
    Departure_Date = db.Column(db.Date)
    Departure_Time = db.Column(db.Time)
    Arrival_Date = db.Column(db.Date)
    Arrival_Time = db.Column(db.Time)
    Airplane_Type = db.Column(db.String)

#------------------------------------------------------------------------
#                           Airports Table
#------------------------------------------------------------------------
class Airports(db.Model):
    __tablename__ = "airports"
    Airport_Code = db.Column(db.VARCHAR(3), primary_key=True)
    Airport_Name = db.Column(db.String)
    Airport_City = db.Column(db.String)
    Airport_State = db.Column(db.String)
#------------------------------------------------------------------------
#                           Prices Table
#------------------------------------------------------------------------
class Prices(db.Model):
    __tablename__ = "prices"
    Flight_Id = db.Column(db.Integer, primary_key = True)
    Price = db.Column(db.FLOAT(2))

#========================================================================


#========================================================================
#                       Define App Routes
#========================================================================
@app.route('/')
def home():
    return (
        f"/Welcome to AeroQuest</br>"
        f"/Available Routes:</br>"
        f"/Airports</br>"
        f"/Flights</br>"
        f"/Prices</br>"
        f"/AirportFlightsandPrice</br>"
    )

#------------------------------------------------------------------------
#                       Flights App route
#------------------------------------------------------------------------
@app.route("/Flights")
def get_flights():
    flights = Flights.query.all()
    flights_list = [
        {
            'Flight_id': flight.Flight_id,
            'Source_Airport_Code': flight.Source_Airport_Code,
            'Destination_Airport_Code': flight.Dest_Airport_Code,
            'Departure_Date': flight.Departure_Date.strftime("%m/%d/%Y") if flight.Departure_Date is not None else None,
            'Departure_Time': flight.Departure_Time.strftime("%H:%M") if flight.Departure_Time is not None else None,
            'Arrival_Date': flight.Arrival_Date.strftime("%m/%d/%Y") if flight.Arrival_Date is not None else None,
            'Arrival_Time': flight.Arrival_Time.strftime("%H:%M") if flight.Arrival_Time is not None else None,
        } for flight in flights
    ]
    return jsonify({'Flights': flights_list})

#------------------------------------------------------------------------
#                       Airports App route
#------------------------------------------------------------------------

@app.route("/Airports")
def get_airports():
    airports = Airports.query.all()
    airports_list = [
        {
            'Airport_Code': airport.Airport_Code,
            'Airport_Name': airport.Airport_Name,
            'Airport_City': airport.Airport_City,
            'Airport_State': airport.Airport_State,
        } for airport in airports
    ]
    return jsonify({'Airports': airports_list})

#------------------------------------------------------------------------
#                       Prices App route
#------------------------------------------------------------------------
@app.route("/Prices")
def get_prices():
    prices = Prices.query.all()
    prices_list = [
        {
            'Flight_ID': price.Flight_Id,
            'Price': price.Price,
        } for price in prices
    ]
    return jsonify({'Prices': prices_list})
#------------------------------------------------------------------------
#                       All Tables App route
#------------------------------------------------------------------------
@app.route('/AirportFlightsandPrice')
def get_airports_andflights_and_price():
    # Aliases for airports
    Source_Airport = aliased(Airports)
    Destination_Airport = aliased(Airports)

    # Perform a join operations assuming there are key relationships between these tables
    joined_data = (
        db.session.query(Flights, Source_Airport, Destination_Airport, Prices)
        .join(Source_Airport, Flights.Source_Airport_Code == Source_Airport.Airport_Code)
        .join(Destination_Airport, Flights.Dest_Airport_Code == Destination_Airport.Airport_Code)
        .join(Prices, Flights.Flight_id==Prices.Flight_Id )
        .all()
    )

    # Format the joined data for JSON response
    merged_list = [
        {
            'Flight_ID': flight.Flight_id,
            'Source_Airport_Code': flight.Source_Airport_Code,
            'Source_Airport_Name': source_airport.Airport_Name,
            'Destination_Airport_Code': flight.Dest_Airport_Code,
            'Destination_Airport_Name': dest_airport.Airport_Name,
            'Departure_Date': flight.Departure_Date.strftime("%m/%d/%Y") if flight.Departure_Date is not None else None,
            'Departure_Time': flight.Departure_Time.strftime("%H:%M") if flight.Departure_Time is not None else None,
            'Arrival_Date': flight.Arrival_Date.strftime("%m/%d/%Y") if flight.Arrival_Date is not None else None,
            'Arrival_Time': flight.Arrival_Time.strftime("%H:%M") if flight.Arrival_Time is not None else None,
            'Price': price.Price,
        }
        for flight, source_airport, dest_airport, price in joined_data
    ]
    return jsonify({'AirportFlightsandPrice': merged_list})
#========================================================================

#------------------------------------------------------------------------
# Main block to run the application only if this script is executed directly
#------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
#------------------------------------------------------------------------
