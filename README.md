# Flight Reservation System

**Web version:** [zeflight.netlify.app](https://zeflight.netlify.app/)

A flight booking system in two versions: a browser app that keeps its data in `localStorage`, and the original Python desktop app with a Tkinter interface and a SQLite database.

## Web version

- Flights, passengers and bookings, with search and filters
- Seat selection for each booking
- CSV export of the tables
- Data saved in the browser with Local Storage, nothing sent to a server
- Installable PWA that works offline

Open `index.html` in a browser, or use the live link above.

## Desktop version (Python and Tkinter)

Six tabs to add, edit, delete and search flights, passengers, airlines, airports, bookings and payments. Each tab is a Tkinter form above a table (`ttk.Treeview`), backed by SQLite.

Setup: the schema script creates `flight_reservation.db` first, then the app opens it.

```bash
git clone https://github.com/shemaiscard/Flight-reservation-app.git
cd Flight-reservation-app
python "Flight reservation database.sqlite"   # a Python script that creates the six tables
python "Flight reservation.py"
```

Requires Python 3. `tkinter` and `sqlite3` ship with the standard installer.

**Tables:** `Flight`, `Passenger`, `Airline`, `Airport`, `Booking`, `Payment`. The full design is in `Flight Reservation report.pdf`.

## Tech stack

| Part | Technology |
| --- | --- |
| Web app | JavaScript, HTML5, CSS Grid, Local Storage, PWA |
| Desktop app | Python, Tkinter (`ttk`) |
| Database | SQLite |
| Hosting | Netlify |

## License

MIT License
