# TransMate — Transportation Management App

TransMate is a full-stack Transportation Booking and Fleet Management System built for a final-semester CSE project.

## Stack

- Frontend: React + Vite + Tailwind CSS + Leaflet/OpenStreetMap
- Backend: Django REST Framework
- Auth: JWT
- Database: SQLite by default, PostgreSQL supported
- Payment: Cash/mock + bKash/Nagad sandbox-ready gateway structure
- Invoice: ReportLab PDF invoice
- Email: Django email backend, console by default

## Folder Structure

```text
transmate_full_project/
├── transmate_backend/
├── transmate_frontend/
└── docs/
```

## Backend Setup

```bash
cd transmate_backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# or
cp .env.example .env     # macOS/Linux

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

After creating a superuser, go to:

```text
http://127.0.0.1:8000/admin/
```

Edit your superuser and set:

```text
role = ADMIN
is_verified = True
```

## Frontend Setup

```bash
cd transmate_frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

Backend API URL:

```text
http://127.0.0.1:8000/api
```

## Recommended Demo Flow

1. Create admin superuser and set role ADMIN.
2. Register a customer from frontend.
3. Register a driver from frontend.
4. Admin approves driver from Django admin or API.
5. Admin creates vehicle types and vehicles.
6. Admin assigns driver to a vehicle.
7. Customer creates booking using map route picker.
8. Admin accepts booking.
9. Admin assigns trip.
10. Driver accepts, starts, and completes trip.
11. Customer creates payment and confirms it.
12. Customer downloads invoice.
13. Customer gives rating.
14. Admin views reports and maintenance records.

## Common Admin API Examples

Create Vehicle Type:

```http
POST /api/vehicles/admin/types/
```

Assign Trip:

```http
POST /api/trips/admin/assign/
```

Dashboard Summary:

```http
GET /api/reports/admin/summary/
```

## Notes

- SQLite is used by default so the project can run immediately.
- To use PostgreSQL, update `.env`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=transmate_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

- bKash/Nagad real sandbox requires merchant credentials. Without credentials, bKash uses demo fallback and Nagad uses placeholder response.
