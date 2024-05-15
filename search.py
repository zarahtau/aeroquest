
from flask import Flask, render_template, request, jsonify, session
import json
from datetime import datetime
#from searchQueries import one_way_trip
current_date = datetime.now()
current_date.strftime('%m/%d/%Y')

# defining the current date
app = Flask(__name__)

# set a secret key for the session
app.secret_key = b'the_secret'

@app.route('/')
def home():
    return render_template('search.html')

# Load JSON data from AirportsFlightsandPrice- use your file path for this 
with open('/Users/zarahtaufique/Desktop/SJSU/Year3Semester2/CMPE131/AeroQuest/Resources/AirportFlightsandPrice.json', 'r') as file:
    flights_data = json.load(file)

@app.route('/OneWayFlights', methods=['POST'])
def one_way():
    # Get user inputs from the form
    departure_date = request.form['departure_date']
    departure_airport = request.form['departure_airport']
    destination_airport = request.form['destination_airport']
    
    if not (departure_date):
        departure_date = 0

    filtered_flights = one_way_flights_query(departure_date, departure_airport, destination_airport)
    
    # Store the filtered flights in session
    session['filtered_flights'] = filtered_flights
    
    # Pass the query result to the HTML template for rendering
    return render_template('one_way_flights.html', flights=filtered_flights)

@app.route('/SortOneWayFlights', methods=['POST'])
def sort_one_way_flights():
    # retrieve the filtered flights from session
    filtered_flights = session.get('filtered_flights', [])
    
    sort_option = request.form['sort_option']  # Get sort option from form input
    
    # sort the flights by price based on the user's selection
    if sort_option == 'asc':
        sorted_flights = sorted(filtered_flights, key=lambda x: float(x['Price']))
    elif sort_option == 'desc':
        sorted_flights = sorted(filtered_flights, key=lambda x: float(x['Price']), reverse=True)
    elif sort_option == 'time':
        sorted_flights = sorted(filtered_flights, key=lambda x: (x['Departure_Time']))
    else: # option in case of failure
        sorted_flights = filtered_flights        

    # Pass the sorted flights to the HTML template for rendering
    return render_template('one_way_flights.html', flights=sorted_flights)

def one_way_flights_query(departure_date, departure_airport, destination_airport):
    filtered_flights = []
    
    # query if the user provides a date
    if departure_date != 0:
        filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if flight['Departure_Date'] == departure_date and
            (flight['Source_Airport_Code'] == departure_airport or flight['Source_Airport_Name'] == departure_airport) and
            (flight['Destination_Airport_Code'] == destination_airport or flight['Destination_Airport_Name'] == destination_airport)
        ]
    else:
        filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            # Parse the departure date string from flight data into a datetime object
            if (flight['Source_Airport_Code'] == departure_airport or flight['Source_Airport_Name'] == departure_airport) and
            (flight['Destination_Airport_Code'] == destination_airport or flight['Destination_Airport_Name'] == destination_airport)
            and (departure_date_flight := datetime.strptime(flight['Departure_Date'], '%m/%d/%Y')) >= current_date 
        ]
    return filtered_flights

@app.route('/RoundTripFlights', methods=['POST'])
def round_trip_flights_query():
    departure_date = request.form.get('departure_date')
    departure_airport = request.form.get('departure_airport')
    destination_airport = request.form.get('destination_airport')

    if not(departure_date):
        departure_date = 0

    departure_filtered_flights, return_filtered_flights = round_trip_query(departure_date, departure_airport, destination_airport)
    session['departure_filtered_flights'] = departure_filtered_flights
    session['return_filtered_flights'] = return_filtered_flights

    return render_template('round_trip_flights.html', departure_flights=departure_filtered_flights, arrival_flights=return_filtered_flights)

@app.route('/SortRoundTripFlights', methods=['POST'])
def sort_round_trip_flights():
    departure_flights = session.get('departure_filtered_flights', [])
    return_flights = session.get('return_filtered_flights', [])

    sort_option = request.form['sort_option']  # get sort option from form input
    
    # sort the flights based on the user's selection
    if sort_option == 'asc':
        sorted_departures = sorted(departure_flights, key=lambda x: float(x['Price']))
        sorted_returns = sorted(return_flights, key=lambda x: float(x['Price']))
    elif sort_option == 'desc':
        sorted_departures = sorted(departure_flights, key=lambda x: float(x['Price']), reverse=True)
        sorted_returns = sorted(return_flights, key=lambda x: float(x['Price']), reverse=True)
    elif sort_option == 'time':
        sorted_departures = sorted(departure_flights, key=lambda x: x['Departure_Time'])
        sorted_returns = sorted(return_flights, key=lambda x: x['Departure_Time'])
    else: # option in case of failure
        sorted_departures = departure_flights
        sorted_returns = return_flights
       
    return render_template('round_trip_flights.html', departure_flights=sorted_departures, arrival_flights=sorted_returns)

def round_trip_query(departure_date, departure_airport, destination_airport):
    departure_filtered_flights = []
    return_filtered_flights = []  # Corrected variable name
    
    # Query departure flights given departure date from user
    if departure_date != 0: 
        departure_filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if flight['Departure_Date'] == departure_date and
            (flight['Source_Airport_Code'] == departure_airport or flight['Source_Airport_Name'] == departure_airport) and
            (flight['Destination_Airport_Code'] == destination_airport or flight['Destination_Airport_Name'] == destination_airport)  
        ]

        # Query arrival flights
        return_filtered_flights = [
            flight for flight in flights_data['AirportFlightsandPrice']
            if flight['Arrival_Date'] >= departure_date and
            (flight['Source_Airport_Code'] == destination_airport or flight['Source_Airport_Name'] == destination_airport) and
            (flight['Destination_Airport_Code'] == departure_airport or flight['Destination_Airport_Name'] == departure_airport)  
        ]
        return departure_filtered_flights, return_filtered_flights
    else:
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
        
        return departure_filtered_flights, return_filtered_flights
    
if __name__ == '__main__':
    app.run(debug=True)
