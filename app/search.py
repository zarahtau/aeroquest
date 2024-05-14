
from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

current_date = datetime.now()
current_date.strftime('%m/%d/%Y')

# defining the current date
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('search.html')

# load JSON data from AirportsFlightsandPrice - add your file path
with open(' ', 'r') as file:
    flights_data = json.load(file)


@app.route('/OneWayFlights', methods=['POST'])
def one_way_flights_query():
    # Get user inputs from the form
    departure_date = request.form['departure_date']
    departure_airport = request.form['departure_airport']
    destination_airport = request.form['destination_airport']

    # create list of flights
    filtered_flights = []
    
    # query if the user provides a date
    if departure_date:
        filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if flight['Departure_Date'] == departure_date and
            (flight['Source_Airport_Code'] == departure_airport or flight['Source_Airport_Name'] == departure_airport) and
            (flight['Destination_Airport_Code'] == destination_airport or flight['Destination_Airport_Name'] == destination_airport)
        ]
    # query if the user does not provide a data but provides an destination and source airport
    else:
        filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            # Parse the departure date string from flight data into a datetime object
            if (flight['Source_Airport_Code'] == departure_airport or flight['Source_Airport_Name'] == departure_airport) and
            (flight['Destination_Airport_Code'] == destination_airport or flight['Destination_Airport_Name'] == destination_airport)
            # convert the departure date string in json to date format and compare with the current date
            and (departure_date_flight := datetime.strptime(flight['Departure_Date'], '%m/%d/%Y')) >= current_date 
        ]
    # pass the query result to the HTML template for rendering
    return render_template('one_way_flights.html', flights=filtered_flights)

@app.route('/RoundTripFlights', methods = ['POST'])
def round_trip_flights_query():
    # Get user inputs from the form
    departure_date = request.form['departure_date']
    departure_airport = request.form['departure_airport']
    destination_airport = request.form['destination_airport']

    departure_filtered_flights = []
    return_filtered_flights = []  # corrected variable name
    
    # query departure flights given departure date from user
    if departure_date: 
        departure_filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if flight['Departure_Date'] == departure_date and
            (flight['Source_Airport_Code'] == departure_airport or flight['Source_Airport_Name'] == departure_airport) and
            (flight['Destination_Airport_Code'] == destination_airport or flight['Destination_Airport_Name'] == destination_airport)  
        ]

        # query return flights where flights are on or after the departure flight date
        return_filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if flight['Arrival_Date'] >= departure_date and
            (flight['Source_Airport_Code'] == destination_airport or flight['Source_Airport_Name'] == destination_airport) and
            (flight['Destination_Airport_Code'] == departure_airport or flight['Destination_Airport_Name'] == departure_airport)  
        ]
        
    else:
      # departure data is not given by the user so retrieve flights from the current day
        departure_filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if (flight['Source_Airport_Code'] == departure_airport or flight['Source_Airport_Name'] == departure_airport) and
            (flight['Destination_Airport_Code'] == destination_airport or flight['Destination_Airport_Name'] == destination_airport)
            and datetime.strptime(flight['Departure_Date'], '%m/%d/%Y') >= current_date
        ]
    
        return_filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if datetime.strptime(flight['Arrival_Date'], '%m/%d/%Y') >= current_date and
            (flight['Source_Airport_Code'] == destination_airport or flight['Source_Airport_Name'] == destination_airport) and
            (flight['Destination_Airport_Code'] == departure_airport or flight['Destination_Airport_Name'] == departure_airport)  
            and datetime.strptime(flight['Departure_Date'], '%m/%d/%Y') >= current_date
        ]

    return render_template('round_trip_flights.html', departure_flights=departure_filtered_flights, arrival_flights=return_filtered_flights)

if __name__ == '__main__':
    app.run(debug=True)
