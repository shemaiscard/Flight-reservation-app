// Database & State Management
const DB = {
    get: (key) => JSON.parse(localStorage.getItem(key)) || [],
    save: (key, data) => localStorage.setItem(key, JSON.stringify(data)),
    init: () => {
        if (!localStorage.getItem('flights')) {
            DB.save('flights', [{ id: 1, number: 'FN101', departure: '2026-05-01T10:00', arrival: '2026-05-01T14:00', origin: 'KGL', destination: 'DXB', seats: 150, airlineId: 1 }]);
            DB.save('passengers', [{ id: 1, firstName: 'John', lastName: 'Doe', email: 'john@example.com', passport: 'A1234567' }]);
            DB.save('airports', [{ id: 1, code: 'KGL', name: 'Kigali International', location: 'Kigali, Rwanda', facilities: 'VIP Lounge' }]);
            DB.save('airlines', [{ id: 1, name: 'RwandAir', contact: '+250788000', region: 'Global' }]);
        }
    }
};

const App = {
    state: {
        editingId: null,
        currentTab: 'dashboard'
    },

    init() {
        DB.init();
        this.bindEvents();
        this.updateDashboard();
        this.renderAll();
    },

    bindEvents() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });

        // Theme toggle
        document.getElementById('themeToggle').addEventListener('click', () => {
            const body = document.body;
            const newTheme = body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });

        // Init theme
        document.body.setAttribute('data-theme', localStorage.getItem('theme') || 'dark');
    },

    switchTab(tabId) {
        this.state.currentTab = tabId;
        this.state.editingId = null;
        
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === tabId));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.toggle('active', c.id === tabId));
        
        if (tabId === 'dashboard') this.updateDashboard();
        this.clearAllForms();
    },

    updateDashboard() {
        const flights = DB.get('flights');
        const bookings = DB.get('bookings');
        const payments = DB.get('payments');
        const passengers = DB.get('passengers');

        document.getElementById('statFlights').textContent = flights.length;
        document.getElementById('statBookings').textContent = bookings.length;
        document.getElementById('statPassengers').textContent = passengers.length;
        
        const totalRevenue = payments.reduce((sum, p) => sum + parseFloat(p.amount || 0), 0);
        document.getElementById('statRevenue').textContent = `$${totalRevenue.toFixed(2)}`;
    },

    renderTable(tableId, data, columns, type) {
        const tbody = document.querySelector(`#${tableId} tbody`);
        tbody.innerHTML = '';
        
        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.onclick = () => this.loadForEdit(type, item);
            tr.style.cursor = 'pointer';

            columns.forEach(col => {
                const td = document.createElement('td');
                if (col === 'status') {
                    const badgeClass = item[col] === 'Paid' ? 'badge-success' : (item[col] === 'Cancelled' ? 'badge-danger' : 'badge-warning');
                    td.innerHTML = `<span class="badge ${badgeClass}">${item[col]}</span>`;
                } else {
                    td.textContent = item[col] || '-';
                }
                tr.appendChild(td);
            });
            
            const actionsTd = document.createElement('td');
            actionsTd.className = 'actions-cell';
            actionsTd.innerHTML = `<button class="btn btn-danger btn-sm" onclick="event.stopPropagation(); App.deleteItem('${type}', ${item.id})">Delete</button>`;
            tr.appendChild(actionsTd);
            tbody.appendChild(tr);
        });
    },

    renderAll() {
        this.renderTable('flightsTable', DB.get('flights'), ['id', 'number', 'departure', 'arrival', 'origin', 'destination', 'seats', 'airlineId'], 'flights');
        this.renderTable('passengersTable', DB.get('passengers'), ['id', 'firstName', 'lastName', 'email', 'passport'], 'passengers');
        this.renderTable('airportsTable', DB.get('airports'), ['id', 'code', 'name', 'location', 'facilities'], 'airports');
        this.renderTable('airlinesTable', DB.get('airlines'), ['id', 'name', 'contact', 'region'], 'airlines');
        this.renderTable('bookingsTable', DB.get('bookings'), ['id', 'flightId', 'passengerId', 'status'], 'bookings');
        this.renderTable('paymentsTable', DB.get('payments'), ['id', 'bookingId', 'method', 'amount', 'time'], 'payments');
    },

    // CRUD Operations
    saveItem(type) {
        const data = DB.get(type);
        const item = this.getFormData(type);
        
        if (!item) return;

        if (this.state.editingId) {
            const index = data.findIndex(i => i.id === this.state.editingId);
            data[index] = { ...item, id: this.state.editingId };
            this.state.editingId = null;
            document.querySelector(`#${type} .btn-primary`).textContent = `Add ${type.slice(0, -1)}`;
        } else {
            item.id = data.length > 0 ? Math.max(...data.map(i => i.id)) + 1 : 1;
            data.push(item);
        }

        DB.save(type, data);
        this.renderAll();
        this.clearAllForms();
        if (this.state.currentTab === 'dashboard') this.updateDashboard();
    },

    deleteItem(type, id) {
        if (!confirm('Are you sure?')) return;
        const data = DB.get(type).filter(i => i.id !== id);
        DB.save(type, data);
        this.renderAll();
        this.updateDashboard();
    },

    loadForEdit(type, item) {
        this.state.editingId = item.id;
        const mapping = {
            flights: ['flightNumber:number', 'departureTime:departure', 'arrivalTime:arrival', 'originAirport:origin', 'destinationAirport:destination', 'availableSeats:seats', 'flightAirlineId:airlineId'],
            passengers: ['passengerFirstName:firstName', 'passengerLastName:lastName', 'passengerEmail:email', 'passengerPassport:passport'],
            airports: ['airportCode:code', 'airportName:name', 'airportLocation:location', 'airportFacilities:facilities'],
            airlines: ['airlineName:name', 'airlineContact:contact', 'airlineRegion:region'],
            bookings: ['bookingFlightId:flightId', 'bookingPassengerId:passengerId', 'bookingStatus:status'],
            payments: ['paymentBookingId:bookingId', 'paymentMethod:method', 'paymentAmount:amount', 'paymentTime:time']
        };

        mapping[type].forEach(m => {
            const [elId, key] = m.split(':');
            document.getElementById(elId).value = item[key];
        });

        document.querySelector(`#${type} .btn-primary`).textContent = `Update ${type.slice(0, -1)}`;
    },

    getFormData(type) {
        try {
            if (type === 'flights') {
                return {
                    number: document.getElementById('flightNumber').value,
                    departure: document.getElementById('departureTime').value,
                    arrival: document.getElementById('arrivalTime').value,
                    origin: document.getElementById('originAirport').value,
                    destination: document.getElementById('destinationAirport').value,
                    seats: document.getElementById('availableSeats').value,
                    airlineId: document.getElementById('flightAirlineId').value
                };
            }
            if (type === 'passengers') {
                return {
                    firstName: document.getElementById('passengerFirstName').value,
                    lastName: document.getElementById('passengerLastName').value,
                    email: document.getElementById('passengerEmail').value,
                    passport: document.getElementById('passengerPassport').value
                };
            }
            if (type === 'airports') {
                return {
                    code: document.getElementById('airportCode').value,
                    name: document.getElementById('airportName').value,
                    location: document.getElementById('airportLocation').value,
                    facilities: document.getElementById('airportFacilities').value
                };
            }
            if (type === 'airlines') {
                return {
                    name: document.getElementById('airlineName').value,
                    contact: document.getElementById('airlineContact').value,
                    region: document.getElementById('airlineRegion').value
                };
            }
            if (type === 'bookings') {
                return {
                    flightId: document.getElementById('bookingFlightId').value,
                    passengerId: document.getElementById('bookingPassengerId').value,
                    status: document.getElementById('bookingStatus').value
                };
            }
            if (type === 'payments') {
                return {
                    bookingId: document.getElementById('paymentBookingId').value,
                    method: document.getElementById('paymentMethod').value,
                    amount: document.getElementById('paymentAmount').value,
                    time: document.getElementById('paymentTime').value
                };
            }
        } catch (e) {
            alert('Please fill all fields correctly');
            return null;
        }
    },

    clearAllForms() {
        document.querySelectorAll('input, select').forEach(i => {
            if (i.id.includes('search')) return;
            i.value = i.type === 'number' ? 0 : '';
        });
        document.querySelectorAll('.btn-primary').forEach(b => {
            if (b.textContent.includes('Update')) {
                const tab = b.closest('section').id;
                b.textContent = `Add ${tab.slice(0, -1)}`;
            }
        });
    },

    search(type, query) {
        const data = DB.get(type);
        const filtered = data.filter(item => {
            return Object.values(item).some(val => 
                String(val).toLowerCase().includes(query.toLowerCase())
            );
        });
        
        const columns = {
            flights: ['id', 'number', 'departure', 'arrival', 'origin', 'destination', 'seats', 'airlineId'],
            passengers: ['id', 'firstName', 'lastName', 'email', 'passport'],
            airports: ['id', 'code', 'name', 'location', 'facilities'],
            airlines: ['id', 'name', 'contact', 'region'],
            bookings: ['id', 'flightId', 'passengerId', 'status'],
            payments: ['id', 'bookingId', 'method', 'amount', 'time']
        };

        this.renderTable(`${type}Table`, filtered, columns[type], type);
    },

    exportCSV(type) {
        const data = DB.get(type);
        if (data.length === 0) return alert('No data to export');
        
        const headers = Object.keys(data[0]).join(',');
        const rows = data.map(item => Object.values(item).join(','));
        const csvContent = "data:text/csv;charset=utf-8," + headers + "\n" + rows.join("\n");
        
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `${type}_report.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
};

// Global wrappers for HTML onclick attributes
window.addFlight = () => App.saveItem('flights');
window.addPassenger = () => App.saveItem('passengers');
window.addAirport = () => App.saveItem('airports');
window.addAirline = () => App.saveItem('airlines');
window.addBooking = () => App.saveItem('bookings');
window.addPayment = () => App.saveItem('payments');

window.searchFlights = () => App.search('flights', document.getElementById('searchFlight').value);
window.searchPassengers = () => App.search('passengers', document.getElementById('searchPassenger').value);
window.searchAirports = () => App.search('airports', document.getElementById('searchAirport').value);
window.searchAirlines = () => App.search('airlines', document.getElementById('searchAirline').value);
window.searchBookings = () => App.search('bookings', document.getElementById('searchBooking').value);
window.searchPayments = () => App.search('payments', document.getElementById('searchPayment').value);

window.exportData = (type) => App.exportCSV(type);
window.clearForm = () => App.clearAllForms();

App.init();
