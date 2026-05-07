# Postman Testing Flow

Use this flow after running backend server.

## 1. Register Customer

```http
POST http://127.0.0.1:8000/api/auth/register/customer/
```

```json
{
  "username": "customer1",
  "email": "customer1@gmail.com",
  "phone": "01711111111",
  "password": "123456",
  "confirm_password": "123456",
  "address": "Dhaka"
}
```

## 2. Register Driver

```http
POST http://127.0.0.1:8000/api/auth/register/driver/
```

```json
{
  "username": "driver1",
  "email": "driver1@gmail.com",
  "phone": "01811111111",
  "password": "123456",
  "confirm_password": "123456",
  "address": "Dhaka"
}
```

## 3. Admin Login

```http
POST http://127.0.0.1:8000/api/auth/login/
```

```json
{
  "username": "admin",
  "password": "your_password"
}
```

Use access token as:

```text
Authorization: Bearer <token>
```

## 4. Approve Driver

```http
PATCH http://127.0.0.1:8000/api/auth/admin/drivers/2/approve/
```

## 5. Create Vehicle Type

```http
POST http://127.0.0.1:8000/api/vehicles/admin/types/
```

```json
{
  "name": "Car",
  "base_fare": "100.00",
  "per_km_rate": "25.00",
  "capacity": 4,
  "description": "Private car service"
}
```

## 6. Create Vehicle

```http
POST http://127.0.0.1:8000/api/vehicles/admin/vehicles/
```

```json
{
  "vehicle_type": 1,
  "driver": 2,
  "registration_number": "DHAKA-METRO-GA-123456",
  "model": "Toyota Corolla",
  "color": "White",
  "capacity": 4,
  "status": "AVAILABLE"
}
```

## 7. Customer Login and Create Booking

```http
POST http://127.0.0.1:8000/api/bookings/
```

```json
{
  "vehicle_type": 1,
  "pickup_location": "Uttara, Dhaka",
  "dropoff_location": "Dhanmondi, Dhaka",
  "pickup_latitude": "23.8759000",
  "pickup_longitude": "90.3795000",
  "dropoff_latitude": "23.7465000",
  "dropoff_longitude": "90.3760000",
  "distance_km": "18.50"
}
```

## 8. Admin Accept Booking

```http
PATCH http://127.0.0.1:8000/api/bookings/admin/1/accept/
```

## 9. Admin Assign Trip

```http
POST http://127.0.0.1:8000/api/trips/admin/assign/
```

```json
{
  "booking_id": 1,
  "driver_id": 2,
  "vehicle_id": 1
}
```

## 10. Driver Trip Actions

```http
PATCH /api/trips/driver/1/accept/
PATCH /api/trips/driver/1/start/
PATCH /api/trips/driver/1/complete/
```

Complete body:

```json
{
  "actual_distance_km": "18.90",
  "final_fare": "575.00"
}
```

## 11. Customer Payment

```http
POST /api/payments/
```

```json
{
  "booking_id": 1,
  "payment_method": "BKASH",
  "transaction_id": "TXN123"
}
```

Confirm:

```http
PATCH /api/payments/1/confirm/
```

Download invoice:

```http
GET /api/payments/1/invoice/
```
