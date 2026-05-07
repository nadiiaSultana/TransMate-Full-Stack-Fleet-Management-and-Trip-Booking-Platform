# Project Specifications

## Project Name

TransMate

## Project Type

Transportation Booking and Fleet Management System

## Main Objective

To digitize transport booking, driver assignment, vehicle management, trip monitoring, payment, invoice generation, notification, maintenance tracking, and reporting.

## User Roles

### Customer

- Register/login
- Create booking
- Select pickup/drop-off on map
- View fare estimate
- View booking/trip history
- Make payment
- Download invoice
- Submit rating
- Submit complaint

### Driver

- Register/login
- Wait for admin approval
- View assigned trips
- Accept/start/complete trip
- View earnings report

### Admin

- Manage users and drivers
- Approve drivers
- Manage vehicle types
- Manage vehicles
- Assign drivers to vehicles
- Accept bookings
- Assign trips
- Manage payments
- Manage complaints
- View reports
- Manage vehicle maintenance

## Core Architecture

```text
React Frontend
    ↓ REST API
Django REST Framework Backend
    ↓ ORM
SQLite/PostgreSQL Database
    ↓ Optional Services
Email, PDF, bKash/Nagad, OpenStreetMap
```

## Backend Apps

- users
- vehicles
- bookings
- trips
- payments
- ratings
- complaints
- notifications
- reports
- maintenance

## Authentication

JWT-based authentication using SimpleJWT.

## Database

Default: SQLite
Recommended production: PostgreSQL

## API Design

RESTful APIs grouped by module:

- `/api/auth/`
- `/api/vehicles/`
- `/api/bookings/`
- `/api/trips/`
- `/api/payments/`
- `/api/ratings/`
- `/api/complaints/`
- `/api/notifications/`
- `/api/reports/`
- `/api/maintenance/`
