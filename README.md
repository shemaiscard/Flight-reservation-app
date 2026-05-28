# Flight Reservation System

**Live Demo (Web):** [zeflight.netlify.app](https://zeflight.netlify.app/)

A comprehensive flight booking system available in two versions: a modern browser-based web dashboard and the original Python/Tkinter desktop application. Includes real-time statistics and CSV reporting.

## Versions

### Web Version (Browser)
- Clean dark-mode UI
- Persistent storage via Browser LocalStorage
- No installation needed — works in any modern browser
- Deployable as a static site (Netlify, GitHub Pages)

### Desktop Version (Python/Tkinter)
Full-featured GUI for managing flights, passengers, airlines, airports, bookings, and payments.

## Desktop Setup

```bash
git clone https://github.com/shemaiscard/Flight-reservation-app.git
cd Flight-reservation-app
python flight_reservation.py
```

**Requirements:** Python 3.x (tkinter and sqlite3 are included by default)

## Features

- Flight, passenger, airline, and airport management
- Booking and payment processing
- Search, filter, and CSV export
- SQLite database with auto-creation on first run

## Database Schema

Tables: `Flight`, `Passenger`, `Airline`, `Airport`, `Booking`, `Payment`

## License
MIT License
