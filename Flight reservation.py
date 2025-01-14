import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def execute_query(query, parameters=()):
    with sqlite3.connect("flight_reservation.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        conn.commit()

def execute_read_query(query, parameters=()):
    with sqlite3.connect("flight_reservation.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

class FlightReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Reservation System")
        self.root.geometry("900x600")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        self.create_flight_frame()
        self.create_passenger_frame()
        self.create_airport_frame()
        self.create_airline_frame()
        self.create_booking_frame()
        self.create_payment_frame()

    def create_flight_frame(self):
        frame = ttk.Frame(self.notebook, width=800, height=400)
        frame.pack(fill="both", expand=True)
        self.notebook.add(frame, text="Flights")

        # Flight form
        self.flight_number = tk.StringVar()
        self.departure_time = tk.StringVar()
        self.arrival_time = tk.StringVar()
        self.origin_airport = tk.StringVar()
        self.destination_airport = tk.StringVar()
        self.available_seats = tk.IntVar()
        self.airline_id = tk.IntVar()

        form_frame = ttk.LabelFrame(frame, text="Flight Details")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
       
        ttk.Label(form_frame, text="Flight Number:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.flight_number).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Departure Time:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.departure_time).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Arrival Time:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.arrival_time).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Origin Airport:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.origin_airport).grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Destination Airport:").grid(row=4, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.destination_airport).grid(row=4, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Available Seats:").grid(row=5, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.available_seats).grid(row=5, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Airline ID:").grid(row=6, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.airline_id).grid(row=6, column=1, padx=5, pady=5)
        self.search_flight_number = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.search_flight_number).grid(row=3, column=4, padx=5, pady=5)
        ttk.Button(form_frame, text="Search", command=self.search_flights).grid(row=3, column=3, padx=5, pady=5)
        
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(button_frame, text="Add Flight", command=self.add_flight).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Update Flight", command=self.update_flight).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Flight", command=self.delete_flight).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_flight_form).grid(row=0, column=3, padx=5, pady=5)
    # Search frame
        

        self.tree = ttk.Treeview(frame, columns=("ID", "Number", "Departure", "Arrival", "Origin", "Destination", "Seats", "AirlineID"), show="headings")
        self.tree.heading("ID", text="ID", anchor="w")
        self.tree.heading("Number", text="Flight Number", anchor="w")
        self.tree.heading("Departure", text="Departure Time", anchor="w")
        self.tree.heading("Arrival", text="Arrival Time", anchor="w")
        self.tree.heading("Origin", text="Origin Airport", anchor="w")
        self.tree.heading("Destination", text="Destination Airport", anchor="w")
        self.tree.heading("Seats", text="Available Seats", anchor="w")
        self.tree.heading("AirlineID", text="Airline ID", anchor="w")
        self.tree.grid(row=2, column=0, padx=10, pady=10)

        self.tree.bind("<Double-1>", self.load_selected_flight)

        self.load_flights(execute_read_query("SELECT * FROM Flight"))

    def add_flight(self):
        try:
            if not self.flight_number.get() or not self.departure_time.get() or not self.arrival_time.get() or not self.origin_airport.get() or not self.destination_airport.get() or not self.available_seats.get() or not self.airline_id.get():
                raise ValueError("All fields must be filled out")

            query = "INSERT INTO Flight (FlightNumber, DepartureDateTime, ArrivalDateTime, OriginAirportCode, DestinationAirportCode, AvailableSeats, AirlineID) VALUES (?, ?, ?, ?, ?, ?, ?)"
            parameters = (self.flight_number.get(), self.departure_time.get(), self.arrival_time.get(), self.origin_airport.get(), self.destination_airport.get(), self.available_seats.get(), self.airline_id.get())
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Flight added successfully")
            self.load_flights()
            self.clear_flight_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_flights(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        flights = execute_read_query("SELECT * FROM Flight")
        for flight in flights:
            self.tree.insert('', 'end', values=flight)

    def update_flight(self):
        try:
            selected_item = self.tree.selection()[0]
            flight_id = self.tree.item(selected_item, 'values')[0]

            if not self.flight_number.get() or not self.departure_time.get() or not self.arrival_time.get() or not self.origin_airport.get() or not self.destination_airport.get() or not self.available_seats.get() or not self.airline_id.get():
                raise ValueError("All fields must be filled out")

            query = "UPDATE Flight SET FlightNumber = ?, DepartureDateTime = ?, ArrivalDateTime = ?, OriginAirportCode = ?, DestinationAirportCode = ?, AvailableSeats = ?, AirlineID = ? WHERE FlightID = ?"
            parameters = (self.flight_number.get(), self.departure_time.get(), self.arrival_time.get(), self.origin_airport.get(), self.destination_airport.get(), self.available_seats.get(), self.airline_id.get(), flight_id)
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Flight updated successfully")
            self.load_flights()
            self.clear_flight_form()
        except IndexError:
            messagebox.showerror("Error", "No flight selected")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_flight(self):
        try:
            selected_item = self.tree.selection()[0]
            flight_id = self.tree.item(selected_item, 'values')[0]
            query = "DELETE FROM Flight WHERE FlightID = ?"
            execute_query(query, (flight_id,))
            messagebox.showinfo("Success", "Flight deleted successfully")
            self.load_flights()
        except IndexError:
            messagebox.showerror("Error", "No flight selected")

    def load_selected_flight(self, event):
        selected_item = self.tree.selection()[0]
        flight = self.tree.item(selected_item, 'values')

        self.flight_number.set(flight[1])
        self.departure_time.set(flight[2])
        self.arrival_time.set(flight[3])
        self.origin_airport.set(flight[4])
        self.destination_airport.set(flight[5])
        self.available_seats.set(flight[6])
        self.airline_id.set(flight[7])

    def search_flights(self):
        search_number = self.search_flight_number.get()
        query = "SELECT * FROM Flight WHERE FlightNumber LIKE ?"
        parameters = (f"%{search_number}%",)
        flights = execute_read_query(query, parameters)
        self.load_flights(flights)

    def load_flights(self, flights):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for flight in flights:
            self.tree.insert('', 'end', values=flight)

    def clear_flight_form(self):
        self.flight_number.set("")
        self.departure_time.set("")
        self.arrival_time.set("")
        self.origin_airport.set("")
        self.destination_airport.set("")
        self.available_seats.set(0)
        self.airline_id.set(0)

    def create_passenger_frame(self):
        frame = ttk.Frame(self.notebook, width=800, height=400)
        frame.pack(fill="both", expand=True)
        self.notebook.add(frame, text="Passengers")
    
            # Passenger form
        self.passenger_first_name = tk.StringVar()
        self.passenger_last_name = tk.StringVar()
        self.passenger_email = tk.StringVar()
        self.passenger_passport_number = tk.StringVar()

        form_frame = ttk.LabelFrame(frame, text="Passenger Details")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.passenger_first_name).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.passenger_last_name).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.passenger_email).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Passport Number:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.passenger_passport_number).grid(row=3, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(button_frame, text="Add Passenger", command=self.add_passenger).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Update Passenger", command=self.update_passenger).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Passenger", command=self.delete_passenger).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_passenger_form).grid(row=0, column=3, padx=5, pady=5)

        # Search frame
        search_frame = ttk.LabelFrame(frame, text="Search Passenger")
        search_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.search_passenger_name = tk.StringVar()
        ttk.Label(search_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(search_frame, textvariable=self.search_passenger_name).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_frame, text="Search", command=self.search_passengers).grid(row=0, column=2, padx=5, pady=5)

        self.passenger_tree = ttk.Treeview(frame, columns=("ID", "FirstName", "LastName", "Email", "PassportNumber"), show="headings")
        self.passenger_tree.heading("ID", text="ID")
        self.passenger_tree.heading("FirstName", text="First Name")
        self.passenger_tree.heading("LastName", text="Last Name")
        self.passenger_tree.heading("Email", text="Email")
        self.passenger_tree.heading("PassportNumber", text="Passport Number")
        self.passenger_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.passenger_tree.bind("<Double-1>", self.load_selected_passenger)

        self.load_passengers()

    def add_passenger(self):
        try:
            if not self.passenger_first_name.get() or not self.passenger_last_name.get() or not self.passenger_email.get() or not self.passenger_passport_number.get():
                raise ValueError("All fields must be filled out")

            query = "INSERT INTO Passenger (FirstName, LastName, Email, PassportNumber) VALUES (?, ?, ?, ?)"
            parameters = (self.passenger_first_name.get(), self.passenger_last_name.get(), self.passenger_email.get(), self.passenger_passport_number.get())
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Passenger added successfully")
            self.load_passengers()
            self.clear_passenger_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_passengers(self):
        for item in self.passenger_tree.get_children():
            self.passenger_tree.delete(item)
        passengers = execute_read_query("SELECT * FROM Passenger")
        for passenger in passengers:
            self.passenger_tree.insert('', 'end', values=passenger)

    def update_passenger(self):
        try:
            selected_item = self.passenger_tree.selection()[0]
            passenger_id = self.passenger_tree.item(selected_item, 'values')[0]

            if not self.passenger_first_name.get() or not self.passenger_last_name.get() or not self.passenger_email.get() or not self.passenger_passport_number.get():
                raise ValueError("All fields must be filled out")

            query = "UPDATE Passenger SET FirstName = ?, LastName = ?, Email = ?, PassportNumber = ? WHERE PassengerID = ?"
            parameters = (self.passenger_first_name.get(), self.passenger_last_name.get(), self.passenger_email.get(), self.passenger_passport_number.get(), passenger_id)
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Passenger updated successfully")
            self.load_passengers()
            self.clear_passenger_form()
        except IndexError:
            messagebox.showerror("Error", "No passenger selected")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_passenger(self):
        try:
            selected_item = self.passenger_tree.selection()[0]
            passenger_id = self.passenger_tree.item(selected_item, 'values')[0]
            query = "DELETE FROM Passenger WHERE PassengerID = ?"
            execute_query(query, (passenger_id,))
            messagebox.showinfo("Success", "Passenger deleted successfully")
            self.load_passengers()
        except IndexError:
            messagebox.showerror("Error", "No passenger selected")

    def load_selected_passenger(self, event):
        selected_item = self.passenger_tree.selection()[0]
        passenger = self.passenger_tree.item(selected_item, 'values')

        self.passenger_first_name.set(passenger[1])
        self.passenger_last_name.set(passenger[2])
        self.passenger_email.set(passenger[3])
        self.passenger_passport_number.set(passenger[4])

    def search_passengers(self):
        search_name = self.search_passenger_name.get()
        query = "SELECT * FROM Passenger WHERE FirstName LIKE ? OR LastName LIKE ?"
        parameters = (f"%{search_name}%", f"%{search_name}%")
        passengers = execute_read_query(query, parameters)
        self.load_passengers_to_tree(passengers)

    def load_passengers_to_tree(self, passengers):
        for item in self.passenger_tree.get_children():
            self.passenger_tree.delete(item)
        for passenger in passengers:
            self.passenger_tree.insert('', 'end', values=passenger)

    def clear_passenger_form(self):
        self.passenger_first_name.set("")
        self.passenger_last_name.set("")
        self.passenger_email.set("")
        self.passenger_passport_number.set("")
    
    def create_airport_frame(self):
        frame = ttk.Frame(self.notebook, width=800, height=400)
        frame.pack(fill="both", expand=True)
        self.notebook.add(frame, text="Airports")

        # Airport form
        self.airport_code = tk.StringVar()
        self.airport_name = tk.StringVar()
        self.airport_location = tk.StringVar()
        self.airport_facilities = tk.StringVar()

        form_frame = ttk.LabelFrame(frame, text="Airport Details")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(form_frame, text="Airport Code:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.airport_code).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Airport Name:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.airport_name).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Location:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.airport_location).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Facilities:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.airport_facilities).grid(row=3, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(button_frame, text="Add Airport", command=self.add_airport).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Update Airport", command=self.update_airport).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Airport", command=self.delete_airport).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_airport_form).grid(row=0, column=3, padx=5, pady=5)

        self.airport_tree = ttk.Treeview(frame, columns=("ID", "Code", "Name", "Location", "Facilities"), show="headings")
        self.airport_tree.heading("ID", text="ID")
        self.airport_tree.heading("Code", text="Airport Code")
        self.airport_tree.heading("Name", text="Airport Name")
        self.airport_tree.heading("Location", text="Location")
        self.airport_tree.heading("Facilities", text="Facilities")
        self.airport_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.airport_tree.bind("<Double-1>", self.load_selected_airport)

        self.load_airports()

    def add_airport(self):
        try:
            if not self.airport_code.get() or not self.airport_name.get() or not self.airport_location.get() or not self.airport_facilities.get():
                raise ValueError("All fields must be filled out")

            query = "INSERT INTO Airport (AirportCode, AirportName, Location, Facilities) VALUES (?, ?, ?, ?)"
            parameters = (self.airport_code.get(), self.airport_name.get(), self.airport_location.get(), self.airport_facilities.get())
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Airport added successfully")
            self.load_airports()
            self.clear_airport_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_airports(self):
        for item in self.airport_tree.get_children():
            self.airport_tree.delete(item)
        airports = execute_read_query("SELECT * FROM Airport")
        for airport in airports:
            self.airport_tree.insert('', 'end', values=airport)

    def update_airport(self):
        try:
            selected_item = self.airport_tree.selection()[0]
            airport_id = self.airport_tree.item(selected_item, 'values')[0]

            if not self.airport_code.get() or not self.airport_name.get() or not self.airport_location.get() or not self.airport_facilities.get():
                raise ValueError("All fields must be filled out")

            query = "UPDATE Airport SET AirportCode = ?, AirportName = ?, Location = ?, Facilities = ? WHERE AirportID = ?"
            parameters = (self.airport_code.get(), self.airport_name.get(), self.airport_location.get(), self.airport_facilities.get(), airport_id)
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Airport updated successfully")
            self.load_airports()
            self.clear_airport_form()
        except IndexError:
            messagebox.showerror("Error", "No airport selected")
        
    def delete_airport(self):
        try:
            selected_item = self.airport_tree.selection()[0]
            airport_id = self.airport_tree.item(selected_item, 'values')[0]
            query = "DELETE FROM Airport WHERE AirportID = ?"
            execute_query(query, (airport_id,))
            messagebox.showinfo("Success", "Airport deleted successfully")
            self.load_airports()
        except IndexError:
            messagebox.showerror("Error", "No airport selected")

    def load_selected_airport(self, event):
        selected_item = self.airport_tree.selection()[0]
        airport = self.airport_tree.item(selected_item, 'values')

        self.airport_code.set(airport[1])
        self.airport_name.set(airport[2])
        self.airport_location.set(airport[3])
        self.airport_facilities.set(airport[4])

    def clear_airport_form(self):
        self.airport_code.set("")
        self.airport_name.set("")
        self.airport_location.set("")
        self.airport_facilities.set("")

    # Methods for managing airlines

    def create_airline_frame(self):
        frame = ttk.Frame(self.notebook, width=800, height=400)
        frame.pack(fill="both", expand=True)
        self.notebook.add(frame, text="Airlines")

        # Airline form
        self.airline_name = tk.StringVar()
        self.airline_contact_number = tk.StringVar()
        self.airline_operating_region = tk.StringVar()

        form_frame = ttk.LabelFrame(frame, text="Airline Details")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(form_frame, text="Airline Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.airline_name).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Contact Number:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.airline_contact_number).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Operating Region:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.airline_operating_region).grid(row=2, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(button_frame, text="Add Airline", command=self.add_airline).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Update Airline", command=self.update_airline).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Airline", command=self.delete_airline).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_airline_form).grid(row=0, column=3, padx=5, pady=5)

        self.airline_tree = ttk.Treeview(frame, columns=("ID", "Name", "ContactNumber", "OperatingRegion"), show="headings")
        self.airline_tree.heading("ID", text="ID")
        self.airline_tree.heading("Name", text="Airline Name")
        self.airline_tree.heading("ContactNumber", text="Contact Number")
        self.airline_tree.heading("OperatingRegion", text="Operating Region")
        self.airline_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.airline_tree.bind("<Double-1>", self.load_selected_airline)

        self.load_airlines()

    def add_airline(self):
        try:
            if not self.airline_name.get() or not self.airline_contact_number.get() or not self.airline_operating_region.get():
                raise ValueError("All fields must be filled out")

            query = "INSERT INTO Airline (AirlineName, ContactNumber, OperatingRegion) VALUES (?, ?, ?)"
            parameters = (self.airline_name.get(), self.airline_contact_number.get(), self.airline_operating_region.get())
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Airline added successfully")
            self.load_airlines()
            self.clear_airline_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_airlines(self):
        for item in self.airline_tree.get_children():
            self.airline_tree.delete(item)
        airlines = execute_read_query("SELECT * FROM Airline")
        for airline in airlines:
            self.airline_tree.insert('', 'end', values=airline)

    def update_airline(self):
        try:
            selected_item = self.airline_tree.selection()[0]
            airline_id = self.airline_tree.item(selected_item, 'values')[0]

            if not self.airline_name.get() or not self.airline_contact_number.get() or not self.airline_operating_region.get():
                raise ValueError("All fields must be filled out")

            query = "UPDATE Airline SET AirlineName = ?, ContactNumber = ?, OperatingRegion = ? WHERE AirlineID = ?"
            parameters = (self.airline_name.get(), self.airline_contact_number.get(), self.airline_operating_region.get(), airline_id)
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Airline updated successfully")
            self.load_airlines()
            self.clear_airline_form()
        except IndexError:
            messagebox.showerror("Error", "No airline selected")

    def delete_airline(self):
        try:
            selected_item = self.airline_tree.selection()[0]
            airline_id = self.airline_tree.item(selected_item, 'values')[0]
            query = "DELETE FROM Airline WHERE AirlineID = ?"
            execute_query(query, (airline_id,))
            messagebox.showinfo("Success", "Airline deleted successfully")
            self.load_airlines()
        except IndexError:
            messagebox.showerror("Error", "No airline selected")

    def load_selected_airline(self, event):
        selected_item = self.airline_tree.selection()[0]
        airline = self.airline_tree.item(selected_item, 'values')

        self.airline_name.set(airline[1])
        self.airline_contact_number.set(airline[2])
        self.airline_operating_region.set(airline[3])

    def clear_airline_form(self):
        self.airline_name.set("")
        self.airline_contact_number.set("")
        self.airline_operating_region.set("")

    # Methods for managing bookings

    def create_booking_frame(self):
        frame = ttk.Frame(self.notebook, width=800, height=400)
        frame.pack(fill="both", expand=True)
        self.notebook.add(frame, text="Bookings")

        # Booking form
        self.booking_flight_id = tk.IntVar()
        self.booking_passenger_id = tk.IntVar()
        self.booking_payment_status = tk.StringVar()

        form_frame = ttk.LabelFrame(frame, text="Booking Details")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(form_frame, text="Flight ID:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.booking_flight_id).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Passenger ID:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.booking_passenger_id).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Payment Status:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.booking_payment_status).grid(row=2, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(button_frame, text="Add Booking", command=self.add_booking).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Update Booking", command=self.update_booking).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Booking", command=self.delete_booking).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_booking_form).grid(row=0, column=3, padx=5, pady=5)

        self.booking_tree = ttk.Treeview(frame, columns=("ID", "FlightID", "PassengerID", "PaymentStatus"), show="headings")
        self.booking_tree.heading("ID", text="ID")
        self.booking_tree.heading("FlightID", text="Flight ID")
        self.booking_tree.heading("PassengerID", text="Passenger ID")
        self.booking_tree.heading("PaymentStatus", text="Payment Status")
        self.booking_tree.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.booking_tree.bind("<Double-1>", self.load_selected_booking)

        self.load_bookings()

    def add_booking(self):
        try:
            if not self.booking_flight_id.get() or not self.booking_passenger_id.get() or not self.booking_payment_status.get():
                raise ValueError("All fields must be filled out")

            query = "INSERT INTO Booking (FlightID, PassengerID, PaymentStatus) VALUES (?, ?, ?)"
            parameters = (self.booking_flight_id.get(), self.booking_passenger_id.get(), self.booking_payment_status.get())
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Booking added successfully")
            self.load_bookings()
            self.clear_booking_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_bookings(self):
        for item in self.booking_tree.get_children():
            self.booking_tree.delete(item)
        bookings = execute_read_query("SELECT * FROM Booking")
        for booking in bookings:
            self.booking_tree.insert('', 'end', values=booking)

    def update_booking(self):
        try:
            selected_item = self.booking_tree.selection()[0]
            booking_id = self.booking_tree.item(selected_item, 'values')[0]

            if not self.booking_flight_id.get() or not self.booking_passenger_id.get() or not self.booking_payment_status.get():
                raise ValueError("All fields must be filled out")

            query = "UPDATE Booking SET FlightID = ?, PassengerID = ?, PaymentStatus = ? WHERE BookingID = ?"
            parameters = (self.booking_flight_id.get(), self.booking_passenger_id.get(), self.booking_payment_status.get(), booking_id)
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Booking updated successfully")
            self.load_bookings()
            self.clear_booking_form()
        except IndexError:
            messagebox.showerror("Error", "No booking selected")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_booking(self):
        try:
            selected_item = self.booking_tree.selection()[0]
            booking_id = self.booking_tree.item(selected_item, 'values')[0]
            query = "DELETE FROM Booking WHERE BookingID = ?"
            execute_query(query, (booking_id,))
            messagebox.showinfo("Success", "Booking deleted successfully")
            self.load_bookings()
        except IndexError:
            messagebox.showerror("Error", "No booking selected")

    def load_selected_booking(self, event):
        selected_item = self.booking_tree.selection()[0]
        booking = self.booking_tree.item(selected_item, 'values')

        self.booking_flight_id.set(booking[1])
        self.booking_passenger_id.set(booking[2])
        self.booking_payment_status.set(booking[3])

    def clear_booking_form(self):
        self.booking_flight_id.set("")
        self.booking_passenger_id.set("")
        self.booking_payment_status.set("")

    # Methods for managing payments

    def create_payment_frame(self):
        frame = ttk.Frame(self.notebook, width=800, height=400)
        frame.pack(fill="both", expand=True)  # Adjust width and height if necessary
        self.notebook.add(frame, text="Payments")  # Add the frame to the notebook with the tab title "Payments"

        # Define variables for the payment form fields
        self.payment_booking_id = tk.IntVar()
        self.payment_method = tk.StringVar()
        self.payment_amount = tk.DoubleVar()
        self.payment_transaction_datetime = tk.StringVar()

        # Create a label frame for the payment details form
        form_frame = ttk.LabelFrame(frame, text="Payment Details")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Add labels and entry fields for each form element
        ttk.Label(form_frame, text="Booking ID:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.payment_booking_id).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Payment Method:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.payment_method).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.payment_amount).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Transaction DateTime:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.payment_transaction_datetime).grid(row=3, column=1, padx=5, pady=5)

        # Create a frame for buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Add buttons for payment actions
        ttk.Button(button_frame, text="Add Payment", command=self.add_payment).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Update Payment", command=self.update_payment).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Payment", command=self.delete_payment).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_payment_form).grid(row=0, column=3, padx=5, pady=5)

        # Create a treeview to display payments
        self.payment_tree = ttk.Treeview(frame, columns=("ID", "BookingID", "Method", "Amount", "TransactionDateTime"), show="headings")
        self.payment_tree.heading("ID", text="ID")
        self.payment_tree.heading("BookingID", text="Booking ID")
        self.payment_tree.heading("Method", text="Method")
        self.payment_tree.heading("Amount", text="Amount")
        self.payment_tree.heading("TransactionDateTime", text="Transaction DateTime")
        self.payment_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.payment_tree.bind("<Double-1>", self.load_selected_payment)
        self.load_payments()

    def add_payment(self):
        try:
            if not self.payment_booking_id.get() or not self.payment_method.get() or not self.payment_amount.get() or not self.payment_transaction_datetime.get():
                raise ValueError("All fields must be filled out")

            query = "INSERT INTO Payment (BookingID, PaymentMethod, Amount, TransactionDateTime) VALUES (?, ?, ?, ?)"
            parameters = (self.payment_booking_id.get(), self.payment_method.get(), self.payment_amount.get(), self.payment_transaction_datetime.get())
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Payment added successfully")
            self.load_payments()
            self.clear_payment_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_payments(self):
        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)
        payments = execute_read_query("SELECT * FROM Payment")
        for payment in payments:
            self.payment_tree.insert('', 'end', values=payment)

    def update_payment(self):
        try:
            selected_item = self.payment_tree.selection()[0]
            payment_id = self.payment_tree.item(selected_item, 'values')[0]

            if not self.payment_booking_id.get() or not self.payment_method.get() or not self.payment_amount.get() or not self.payment_transaction_datetime.get():
                raise ValueError("All fields must be filled out")

            query = "UPDATE Payment SET BookingID = ?, PaymentMethod = ?, Amount = ?, TransactionDateTime = ? WHERE PaymentID = ?"
            parameters = (self.payment_booking_id.get(), self.payment_method.get(), self.payment_amount.get(), self.payment_transaction_datetime.get(), payment_id)
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Payment updated successfully")
            self.load_payments()
            self.clear_payment_form()
        except IndexError:
            messagebox.showerror("Error", "No payment selected")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_payment(self):
        try:
            selected_item = self.payment_tree.selection()[0]
            payment_id = self.payment_tree.item(selected_item, 'values')[0]
            query = "DELETE FROM Payment WHERE PaymentID = ?"
            execute_query(query, (payment_id,))
            messagebox.showinfo("Success", "Payment deleted successfully")
            self.load_payments()
        except IndexError:
            messagebox.showerror("Error", "No payment selected")

    def load_selected_payment(self, event):
        selected_item = self.payment_tree.selection()[0]
        payment = self.payment_tree.item(selected_item, 'values')

        self.payment_booking_id.set(payment[1])
        self.payment_method.set(payment[2])
        self.payment_amount.set(payment[3])
        self.payment_transaction_datetime.set(payment[4])

    def clear_payment_form(self):
        self.payment_booking_id.set("")
        self.payment_method.set("")
        self.payment_amount.set("")
        self.payment_transaction_datetime.set("")

    # Methods for managing airports

    def create_airport_frame(self):
        frame = ttk.Frame(self.notebook, width=800, height=400)
        frame.pack(fill="both", expand=True)
        self.notebook.add(frame, text="Airports")

        # Airport form
        self.airport_name = tk.StringVar()
        self.airport_location = tk.StringVar()

        form_frame = ttk.LabelFrame(frame, text="Airport Details")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(form_frame, text="Airport Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.airport_name).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Location:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.airport_location).grid(row=1, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(button_frame, text="Add Airport", command=self.add_airport).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Update Airport", command=self.update_airport).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Airport", command=self.delete_airport).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_airport_form).grid(row=0, column=3, padx=5, pady=5)

        self.airport_tree = ttk.Treeview(frame, columns=("ID", "Name", "Location"), show="headings")
        self.airport_tree.heading("ID", text="ID")
        self.airport_tree.heading("Name", text="Airport Name")
        self.airport_tree.heading("Location", text="Location")
        self.airport_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.airport_tree.bind("<Double-1>", self.load_selected_airport)

        self.load_airports()

    def add_airport(self):
        try:
            if not self.airport_name.get() or not self.airport_location.get():
                raise ValueError("All fields must be filled out")

            query = "INSERT INTO Airport (AirportName, Location) VALUES (?, ?)"
            parameters = (self.airport_name.get(), self.airport_location.get())
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Airport added successfully")
            self.load_airports()
            self.clear_airport_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_airports(self):
        for item in self.airport_tree.get_children():
            self.airport_tree.delete(item)
        airports = execute_read_query("SELECT * FROM Airport")
        for airport in airports:
            self.airport_tree.insert('', 'end', values=airport)

    def update_airport(self):
        try:
            selected_item = self.airport_tree.selection()[0]
            airport_id = self.airport_tree.item(selected_item, 'values')[0]

            if not self.airport_name.get() or not self.airport_location.get():
                raise ValueError("All fields must be filled out")

            query = "UPDATE Airport SET AirportName = ?, Location = ? WHERE AirportID = ?"
            parameters = (self.airport_name.get(), self.airport_location.get(), airport_id)
            execute_query(query, parameters)
            messagebox.showinfo("Success", "Airport updated successfully")
            self.load_airports()
            self.clear_airport_form()
        except IndexError:
            messagebox.showerror("Error", "No airport selected")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_airport(self):
        try:
            selected_item = self.airport_tree.selection()[0]
            airport_id = self.airport_tree.item(selected_item, 'values')[0]
            query = "DELETE FROM Airport WHERE AirportID = ?"
            execute_query(query, (airport_id,))
            messagebox.showinfo("Success", "Airport deleted successfully")
            self.load_airports()
        except IndexError:
            messagebox.showerror("Error", "No airport selected")

    def load_selected_airport(self, event):
        selected_item = self.airport_tree.selection()[0]
        airport = self.airport_tree.item(selected_item, 'values')

        self.airport_name.set(airport[1])
        self.airport_location.set(airport[2])

    def clear_airport_form(self):
        self.airport_name.set("")
        self.airport_location.set("")
if __name__ == "__main__":
    root = tk.Tk()
    app = FlightReservationApp(root)
    root.mainloop()
