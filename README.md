Flight Reservation System
--------------------

Overview:
-------------

The Flight Reservation System is a comprehensive database management application designed to streamline and optimize various aspects of airline operations. This system allows users to manage flights, passengers, airlines, airports, bookings, and payments through an intuitive graphical user interface (GUI). The application is built using Python with the tkinter library for the front-end and sqlite3 for database management.

Features:
----------
- Flight Management: Manage flight information, including flight numbers, departure and arrival times, origin and destination airports, and available seats.
- Passenger Management: Maintain passenger details such as names, contact information, and passport numbers.
- Airline Management: Keep track of airline information, including airline names, contact details, and operating regions.
- Airport Management: Store information about airports, including airport codes, names, locations, and facilities.
- Booking Management: Handle flight reservations, including booking IDs, flight details, passenger information, and payment status.
- Payment Processing: Securely process payments for flight bookings, including transaction IDs, payment methods, and amounts.

**Installation:**
Prerequisites:
- Python 3.x
- tkinter library (usually comes pre-installed with Python)
- sqlite3 library (usually comes pre-installed with Python)

**Steps:**
1. Clone the repository:
   git clone https://github.com/shemaiscard/flight-reservation-system.git
   cd flight-reservation-system

2. Run the application:
   python flight_reservation.py

**Usage:**
----------
**Flight Management:**
- Add Flight: Enter flight details such as flight number, departure time, arrival time, origin airport, destination airport, available seats, and airline ID. Click "Add Flight" to save the details.
- Update Flight: Select a flight from the list, modify the details, and click "Update Flight" to save changes.
- Delete Flight: Select a flight from the list and click "Delete Flight" to remove it from the database.
- Search Flight: Enter a flight number in the search bar and click "Search" to filter the list of flights.

**Passenger Management:**
- Add Passenger: Enter passenger details such as first name, last name, email, and passport number. Click "Add Passenger" to save the details.
- Update Passenger: Select a passenger from the list, modify the details, and click "Update Passenger" to save changes.
- Delete Passenger: Select a passenger from the list and click "Delete Passenger" to remove it from the database.
- Search Passenger: Enter a passenger name in the search bar and click "Search" to filter the list of passengers.

**Airline Management:**
- Add Airline: Enter airline details such as airline name, contact number, and operating region. Click "Add Airline" to save the details.
- Update Airline: Select an airline from the list, modify the details, and click "Update Airline" to save changes.
- Delete Airline: Select an airline from the list and click "Delete Airline" to remove it from the database.

**Airport Management:**
- Add Airport: Enter airport details such as airport code, name, location, and facilities. Click "Add Airport" to save the details.
- Update Airport: Select an airport from the list, modify the details, and click "Update Airport" to save changes.
- Delete Airport: Select an airport from the list and click "Delete Airport" to remove it from the database.

**Booking Management:**
- Add Booking: Enter booking details such as flight ID, passenger ID, and payment status. Click "Add Booking" to save the details.
- Update Booking: Select a booking from the list, modify the details, and click "Update Booking" to save changes.
- Delete Booking: Select a booking from the list and click "Delete Booking" to remove it from the database.

**Payment Management:**
- Add Payment: Enter payment details such as booking ID, payment method, amount, and transaction date/time. Click "Add Payment" to save the details.
- Update Payment: Select a payment from the list, modify the details, and click "Update Payment" to save changes.
- Delete Payment: Select a payment from the list and click "Delete Payment" to remove it from the database.

**Database Schema:**
--------------------
The database schema includes the following tables:
- Flight: Stores flight information.
- Passenger: Stores passenger details.
- Airline: Stores airline information.
- Airport: Stores airport details.
- Booking: Stores booking information.
- Payment: Stores payment details.

**SQL Queries:**
-------------------
- Search for a passenger by last name:
  SELECT * FROM Passenger WHERE LastName LIKE '%Smith%';
- Update available seats for a flight:
  UPDATE Flight SET AvailableSeats = 100 WHERE FlightID = 0;

Contributing:
-------------
Contributions are welcome! Please fork the repository and create a pull request with your changes.

**License:**
--------------
This project is licensed under the MIT License. See the LICENSE file for details.
