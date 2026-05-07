# API Endpoint Summary

## Auth

```text
POST /api/auth/register/customer/
POST /api/auth/register/driver/
POST /api/auth/login/
POST /api/auth/token/refresh/
GET  /api/auth/profile/
PATCH /api/auth/profile/
GET  /api/auth/admin/users/
GET  /api/auth/admin/drivers/
PATCH /api/auth/admin/drivers/{driver_id}/approve/
PATCH /api/auth/admin/users/{user_id}/suspend/
PATCH /api/auth/admin/users/{user_id}/activate/
```

## Vehicles

```text
GET    /api/vehicles/types/
GET    /api/vehicles/admin/types/
POST   /api/vehicles/admin/types/
GET    /api/vehicles/admin/types/{id}/
PATCH  /api/vehicles/admin/types/{id}/
DELETE /api/vehicles/admin/types/{id}/
GET    /api/vehicles/admin/vehicles/
POST   /api/vehicles/admin/vehicles/
GET    /api/vehicles/admin/vehicles/{id}/
PATCH  /api/vehicles/admin/vehicles/{id}/
DELETE /api/vehicles/admin/vehicles/{id}/
PATCH  /api/vehicles/admin/vehicles/{id}/assign-driver/
```

## Bookings

```text
GET   /api/bookings/
POST  /api/bookings/
GET   /api/bookings/{id}/
PATCH /api/bookings/{id}/cancel/
GET   /api/bookings/admin/all/
GET   /api/bookings/admin/{id}/
PATCH /api/bookings/admin/{id}/accept/
PATCH /api/bookings/admin/{id}/cancel/
PATCH /api/bookings/admin/{id}/status/
```

## Trips

```text
POST  /api/trips/admin/assign/
GET   /api/trips/admin/all/
GET   /api/trips/admin/{id}/
GET   /api/trips/driver/my/
GET   /api/trips/driver/active/
GET   /api/trips/driver/earnings/
PATCH /api/trips/driver/{id}/accept/
PATCH /api/trips/driver/{id}/start/
PATCH /api/trips/driver/{id}/complete/
GET   /api/trips/my/
GET   /api/trips/{id}/
```

## Payments

```text
GET   /api/payments/
POST  /api/payments/
GET   /api/payments/{id}/
PATCH /api/payments/{id}/confirm/
PATCH /api/payments/{id}/initiate-gateway/
PATCH /api/payments/{id}/execute-bkash/
GET   /api/payments/{id}/invoice/
GET   /api/payments/admin/all/
GET   /api/payments/admin/{id}/
PATCH /api/payments/admin/{id}/refund/
```

## Maintenance

```text
GET    /api/maintenance/admin/all/
POST   /api/maintenance/admin/all/
GET    /api/maintenance/admin/{id}/
PATCH  /api/maintenance/admin/{id}/
DELETE /api/maintenance/admin/{id}/
GET    /api/maintenance/admin/report/
```
