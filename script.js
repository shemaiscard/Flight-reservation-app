// Database Initialization
const db = {
    flights: JSON.parse(localStorage.getItem('flights')) || [
        { id: 1, number: 'FN101', departure: '2026-05-01T10:00', arrival: '2026-05-01T14:00', origin: 'KGL', destination: 'DXB', seats: 150, airlineId: 1 },
        { id: 2, number: 'FN202', departure: '2026-05-02T08:30', arrival: '2026-05-02T11:45', origin: 'NBO', destination: 'ADD', seats: 120, airlineId: 2 }
    ],
    passengers: JSON.parse(localStorage.getItem('passengers')) || [
        { id: 1, firstName: 'John', lastName: 'Doe', email: 'john@example.com', passport: 'A1234567' }
    ],
    airports: JSON.parse(localStorage.getItem('airports')) || [
        { id: 1, code: 'KGL', name: 'Kigali International', location: 'Kigali, Rwanda', facilities: 'VIP Lounge, Duty Free' }
    ],
    airlines: JSON.parse(localStorage.getItem('airlines')) || [
        { id: 1, name: 'RwandAir', contact: '+250788000', region: 'Africa/Global' }
    ],
    bookings: JSON.parse(localStorage.getItem('bookings')) || [],
    payments: JSON.parse(localStorage.getItem('payments')) || []
};

function saveDb() {
    Object.keys(db).forEach(key => {
        localStorage.setItem(key, JSON.stringify(db[key]));
    });
}

// UI Controllers
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initTheme();
    renderAll();
});

function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    const savedTheme = localStorage.getItem('theme') || 'dark';
    body.setAttribute('data-theme', savedTheme);
    
    themeToggle.addEventListener('click', () => {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

// Rendering Logic
function renderAll() {
    renderFlights();
    renderPassengers();
    renderAirports();
    renderAirlines();
    renderBookings();
    renderPayments();
}

function renderTable(tableId, data, columns, deleteFn, editFn) {
    const tbody = document.querySelector(`#${tableId} tbody`);
    tbody.innerHTML = '';
    
    data.forEach(item => {
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.onclick = () => editFn(item);

        columns.forEach(col => {
            const td = document.createElement('td');
            td.textContent = item[col] || '-';
            tr.appendChild(td);
        });
        
        const actionsTd = document.createElement('td');
        actionsTd.className = 'actions-cell';
        actionsTd.innerHTML = `
            <button class="icon-btn delete" onclick="event.stopPropagation(); ${deleteFn}(${item.id})">Delete</button>
        `;
        tr.appendChild(actionsTd);
        tbody.appendChild(tr);
    });
}

// Flights Module
let editingFlightId = null;

function renderFlights(data = db.flights) {
    renderTable('flightsTable', data, ['id', 'number', 'departure', 'arrival', 'origin', 'destination', 'seats', 'airlineId'], 'deleteFlight', loadFlightToForm);
}

function loadFlightToForm(flight) {
    editingFlightId = flight.id;
    document.getElementById('flightNumber').value = flight.number;
    document.getElementById('departureTime').value = flight.departure;
    document.getElementById('arrivalTime').value = flight.arrival;
    document.getElementById('originAirport').value = flight.origin;
    document.getElementById('destinationAirport').value = flight.destination;
    document.getElementById('availableSeats').value = flight.seats;
    document.getElementById('flightAirlineId').value = flight.airlineId;
    
    document.querySelector('#flights .btn-primary').textContent = 'Update Flight';
}

function addFlight() {
    const flightData = {
        number: document.getElementById('flightNumber').value,
        departure: document.getElementById('departureTime').value,
        arrival: document.getElementById('arrivalTime').value,
        origin: document.getElementById('originAirport').value,
        destination: document.getElementById('destinationAirport').value,
        seats: parseInt(document.getElementById('availableSeats').value),
        airlineId: parseInt(document.getElementById('flightAirlineId').value)
    };

    if (!flightData.number || !flightData.departure) return alert('Fill required fields');

    if (editingFlightId) {
        const index = db.flights.findIndex(f => f.id === editingFlightId);
        db.flights[index] = { ...db.flights[index], ...flightData };
        editingFlightId = null;
        document.querySelector('#flights .btn-primary').textContent = 'Add Flight';
    } else {
        const newFlight = {
            id: db.flights.length > 0 ? Math.max(...db.flights.map(f => f.id)) + 1 : 1,
            ...flightData
        };
        db.flights.push(newFlight);
    }
    
    saveDb();
    renderFlights();
    clearForm('flights');
}

function deleteFlight(id) {
    db.flights = db.flights.filter(f => f.id !== id);
    saveDb();
    renderFlights();
}

function searchFlights() {
    const query = document.getElementById('searchFlight').value.toLowerCase();
    const filtered = db.flights.filter(f => f.number.toLowerCase().includes(query));
    renderFlights(filtered);
}

// Passengers Module
function renderPassengers(data = db.passengers) {
    renderTable('passengersTable', data, ['id', 'firstName', 'lastName', 'email', 'passport'], 'deletePassenger');
}

function addPassenger() {
    const newPassenger = {
        id: db.passengers.length > 0 ? Math.max(...db.passengers.map(p => p.id)) + 1 : 1,
        firstName: document.getElementById('passengerFirstName').value,
        lastName: document.getElementById('passengerLastName').value,
        email: document.getElementById('passengerEmail').value,
        passport: document.getElementById('passengerPassport').value
    };
    
    db.passengers.push(newPassenger);
    saveDb();
    renderPassengers();
    clearForm('passengers');
}

function deletePassenger(id) {
    db.passengers = db.passengers.filter(p => p.id !== id);
    saveDb();
    renderPassengers();
}

function searchPassengers() {
    const query = document.getElementById('searchPassenger').value.toLowerCase();
    const filtered = db.passengers.filter(p => 
        p.firstName.toLowerCase().includes(query) || 
        p.lastName.toLowerCase().includes(query)
    );
    renderPassengers(filtered);
}

// Airports Module
function renderAirports() {
    renderTable('airportsTable', db.airports, ['id', 'code', 'name', 'location', 'facilities'], 'deleteAirport');
}

function addAirport() {
    const newAirport = {
        id: db.airports.length > 0 ? Math.max(...db.airports.map(a => a.id)) + 1 : 1,
        code: document.getElementById('airportCode').value,
        name: document.getElementById('airportName').value,
        location: document.getElementById('airportLocation').value,
        facilities: document.getElementById('airportFacilities').value
    };
    db.airports.push(newAirport);
    saveDb();
    renderAirports();
    clearForm('airports');
}

function deleteAirport(id) {
    db.airports = db.airports.filter(a => a.id !== id);
    saveDb();
    renderAirports();
}

// Airlines Module
function renderAirlines() {
    renderTable('airlinesTable', db.airlines, ['id', 'name', 'contact', 'region'], 'deleteAirline');
}

function addAirline() {
    const newAirline = {
        id: db.airlines.length > 0 ? Math.max(...db.airlines.map(a => a.id)) + 1 : 1,
        name: document.getElementById('airlineName').value,
        contact: document.getElementById('airlineContact').value,
        region: document.getElementById('airlineRegion').value
    };
    db.airlines.push(newAirline);
    saveDb();
    renderAirlines();
    clearForm('airlines');
}

function deleteAirline(id) {
    db.airlines = db.airlines.filter(a => a.id !== id);
    saveDb();
    renderAirlines();
}

// Bookings Module
function renderBookings() {
    renderTable('bookingsTable', db.bookings, ['id', 'flightId', 'passengerId', 'status'], 'deleteBooking');
}

function addBooking() {
    const newBooking = {
        id: db.bookings.length > 0 ? Math.max(...db.bookings.map(b => b.id)) + 1 : 1,
        flightId: parseInt(document.getElementById('bookingFlightId').value),
        passengerId: parseInt(document.getElementById('bookingPassengerId').value),
        status: document.getElementById('bookingStatus').value
    };
    db.bookings.push(newBooking);
    saveDb();
    renderBookings();
    clearForm('bookings');
}

function deleteBooking(id) {
    db.bookings = db.bookings.filter(b => b.id !== id);
    saveDb();
    renderBookings();
}

// Payments Module
function renderPayments() {
    renderTable('paymentsTable', db.payments, ['id', 'bookingId', 'method', 'amount', 'time'], 'deletePayment');
}

function addPayment() {
    const newPayment = {
        id: db.payments.length > 0 ? Math.max(...db.payments.map(p => p.id)) + 1 : 1,
        bookingId: parseInt(document.getElementById('paymentBookingId').value),
        method: document.getElementById('paymentMethod').value,
        amount: parseFloat(document.getElementById('paymentAmount').value),
        time: document.getElementById('paymentTime').value
    };
    db.payments.push(newPayment);
    saveDb();
    renderPayments();
    clearForm('payments');
}

function deletePayment(id) {
    db.payments = db.payments.filter(p => p.id !== id);
    saveDb();
    renderPayments();
}

// Helpers
function clearForm(tabId) {
    const inputs = document.querySelectorAll(`#${tabId} input, #${tabId} select`);
    inputs.forEach(input => {
        if (input.type === 'number') input.value = 0;
        else input.value = '';
    });
}
