from sqlalchemy import create_engine, Column, String, Integer, VARCHAR, Date, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import csv

# Base class for defining the schema
Base = declarative_base()

# Define the Airport table
class Airport(Base):
    __tablename__ = "airports"
    
    # Attributes/Columns
    airport_code = Column(VARCHAR(3), primary_key=True)
    airport_name = Column(String)
    airport_city = Column(String)
    airport_state = Column(String)

    def __init__(self, airport_code, airport_name, airport_city, airport_state):
        self.airport_code = airport_code
        self.airport_name = airport_name
        self.airport_city = airport_city
        self.airport_state = airport_state

    def __repr__(self):
        return f"<Airport(airport_code='{self.airport_code}', airport_name='{self.airport_name}', airport_city='{self.airport_city}', airport_state='{self.airport_state}')>"

class Flights(Base):
    __tablename__ = "flights"

    # Attributes/Columns
    flight_id = Column(Integer, primary_key=True)
    source_airport_code = Column(String, ForeignKey('airports.airport_code'))
    dest_airport_code = Column(String, ForeignKey('airports.airport_code'))
    departure_date = Column(Date)
    departure_time = Column(Time)
    arrival_date = Column(Date)
    arrival_time = Column(Time)
    airplane_type = Column(String)

    def __init__(self, flight_id, source_airport_code, dest_airport_code, departure_date, departure_time, arrival_date, arrival_time, airplane_type):
        self.flight_id = flight_id
        self.source_airport_code = source_airport_code
        self.dest_airport_code = dest_airport_code
        self.departure_date = departure_date
        self.departure_time = departure_time
        self.arrival_date = arrival_date
        self.arrival_time = arrival_time
        self.airplane_type = airplane_type
    

# Create an engine and bind it to the SQLite database
engine = create_engine("sqlite:///airportsdb.db", echo=True)

# Create the table(s)
Base.metadata.create_all(engine)

# Setup a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Function to read data from the airport text file and add to the database
def add_airports_from_file(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            # Ensure we have exactly four parts; handle unexpected formatting
            if len(row) == 4:
                code, name, city, state = row
                new_airport = Airport(airport_code=code.strip(), airport_name=name.strip(), airport_city=city.strip(), airport_state=state.strip())
                session.add(new_airport)
            else:
                print(f"Skipping line: {row} - Incorrect format")
    session.commit()

# Function to read data from the flights text file and add to the database
def add_flights_from_file(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 8:
                id, source, dest, dept_date, dept_time, arr_date, arr_time, type = row
                dept_date = datetime.strptime(dept_date.strip(), '%Y-%m-%d').date()
                dept_time = datetime.strptime(dept_time.strip(), '%H:%M').time()
                arr_date = datetime.strptime(arr_date.strip(), '%Y-%m-%d').date()
                arr_time = datetime.strptime(arr_time.strip(), '%H:%M').time()
                new_flight = Flights(flight_id=int(id.strip()), source_airport_code=source.strip(), dest_airport_code=dest.strip(), departure_date=dept_date, departure_time=dept_time, arrival_date=arr_date, arrival_time=arr_time, airplane_type=type.strip())
                session.add(new_flight)
            else:
                print(f"Skipping line: {row} - Incorrect format")
    session.commit()

# Path to the airport data text file
airports_txt = 'Add txt file path for airport'
flights_txt = 'Add txt file path for flights'

# Call the function to add airports from the text file
add_airports_from_file(airports_txt)
add_flights_from_file(flights_txt)

# Query the database to verify the data insertion
airports = session.query(Airport).all()
flights = session.query(Flights).all()