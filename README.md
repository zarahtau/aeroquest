<p align="center">
  <img src = "https://github.com/zarahtau/aeroquest/assets/136948242/9d009009-3864-48b1-8d2b-edb045a8e578" width="500" alt="Plane in the sunset">
</p>

# AeroQuest
*A model airline reservation site using Python, Flask, and SQLAlchemy* 

## Team Members
- Jason Hernandez
- Lucas Mai
- Zarah Taufique

## Description
AeroQuest is an airline reservation website designed to simplify the process of booking flights. Our platform aims to overcome common issues such as cluttered interfaces, inconsistent pricing, and limited customization options. By providing a reliable platform, AeroQuest aims to streamline the booking experience, helping users find the "perfect fit" flight quickly and efficiently.

## Key Features
### Enhanced Search Functionality
- **Flight Search Criteria**: Search flights by date, number of passengers, and city.
- **Filtering and Sorting Options**: Users can filter and sort search results by price and departure time to easily compare and decide on bookings.

### User Account Management
- **User Authentication and Profile Management**: Login and profile management for personalization and better service delivery.

### Rewards
- **Rewards Program**: If a user had a valid login and was a member with AeroQuest, they are be able to sign up for a rewards program.

## Usage
### Prerequisites
You must have the following prerequisites met or installed on your system
- Python3 (version 3.10.12 or higher)
- Pip3
- Linux

### Instructions 
This shows how to clone the repository from Github. These commands should be run from the terminal and inscludes setting up the virtual environment, installing the required dependencies, and running the application.

1. ```git clone https://github.com/zarahtau/aeroquest.git```
2. ```cd aeroquest```
3. ```python3 -m venv venv```
4. ```source venv/bin/activate```
5. Install Dependencies ```pip3 install -r dependencies.txt```

Ensure that JSON file (‘AirportFlightsandPrices.json’) in the ‘Resources’ directory

To run the application, execute:
```python3 search.py```

Access the web application at http://127.0.0.1:5000

__Note:__
The flaskAPI.py is not required to run the AeroQuest application. It was solely used for connecting our datasets to SQLAlchemy and then converting these datasets to JSON format. The main functionality of the application does not depend on the Flask API.
