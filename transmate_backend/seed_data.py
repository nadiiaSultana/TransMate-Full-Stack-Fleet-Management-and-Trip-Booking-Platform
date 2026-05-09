import os
import django
from decimal import Decimal
from django.utils import timezone
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.users.models import User
from apps.vehicles.models import VehicleType, Vehicle
from apps.bookings.models import Booking
from apps.trips.models import Trip
from apps.payments.models import Payment
from apps.ratings.models import Rating
from apps.complaints.models import Complaint
from apps.notifications.models import Notification
from apps.maintenance.models import VehicleMaintenance


def create_or_update_user(
    username,
    email,
    phone,
    password,
    role,
    is_verified=True,
    is_staff=False,
    is_superuser=False,
    address="Dhaka, Bangladesh",
):
    user, created = User.objects.get_or_create(username=username)

    user.email = email
    user.phone = phone
    user.role = role
    user.is_verified = is_verified
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.is_active = True
    user.address = address
    user.set_password(password)
    user.save()

    return user


def run():
    print("Seeding database...")

    # =========================
    # Users
    # =========================

    admin = create_or_update_user(
        username="admin",
        email="admin@transmate.com",
        phone="01700000000",
        password="admin123",
        role="ADMIN",
        is_verified=True,
        is_staff=True,
        is_superuser=True,
    )

    customer2 = create_or_update_user(
        username="customer2",
        email="customer2@gmail.com",
        phone="01722222222",
        password="123456",
        role="CUSTOMER",
        is_verified=True,
        address="Mirpur, Dhaka",
    )

    customer3 = create_or_update_user(
        username="customer3",
        email="customer3@gmail.com",
        phone="01733333333",
        password="123456",
        role="CUSTOMER",
        is_verified=True,
        address="Uttara, Dhaka",
    )

    driver1 = create_or_update_user(
        username="driver1",
        email="driver1@gmail.com",
        phone="01811111111",
        password="123456",
        role="DRIVER",
        is_verified=True,
        address="Gazipur, Bangladesh",
    )

    driver2 = create_or_update_user(
        username="driver2",
        email="driver2@gmail.com",
        phone="01822222222",
        password="123456",
        role="DRIVER",
        is_verified=True,
        address="Savar, Bangladesh",
    )

    # =========================
    # Vehicle Types
    # =========================

    bike, _ = VehicleType.objects.update_or_create(
        name="Bike",
        defaults={
            "base_fare": Decimal("50.00"),
            "per_km_rate": Decimal("15.00"),
            "capacity": 1,
            "description": "Fast and low-cost ride for one passenger.",
            "is_active": True,
        },
    )

    car, _ = VehicleType.objects.update_or_create(
        name="Car",
        defaults={
            "base_fare": Decimal("100.00"),
            "per_km_rate": Decimal("25.00"),
            "capacity": 4,
            "description": "Comfortable private car service.",
            "is_active": True,
        },
    )

    microbus, _ = VehicleType.objects.update_or_create(
        name="Microbus",
        defaults={
            "base_fare": Decimal("300.00"),
            "per_km_rate": Decimal("50.00"),
            "capacity": 10,
            "description": "Suitable for family and group travel.",
            "is_active": True,
        },
    )

    truck, _ = VehicleType.objects.update_or_create(
        name="Truck",
        defaults={
            "base_fare": Decimal("500.00"),
            "per_km_rate": Decimal("80.00"),
            "capacity": 2,
            "description": "Goods transportation service.",
            "is_active": True,
        },
    )

    # =========================
    # Vehicles
    # =========================

    vehicle1, _ = Vehicle.objects.update_or_create(
        registration_number="DHAKA-METRO-GA-123456",
        defaults={
            "vehicle_type": car,
            "driver": driver1,
            "model": "Toyota Corolla",
            "color": "White",
            "capacity": 4,
            "status": "AVAILABLE",
        },
    )

    vehicle2, _ = Vehicle.objects.update_or_create(
        registration_number="DHAKA-METRO-HA-654321",
        defaults={
            "vehicle_type": bike,
            "driver": driver2,
            "model": "Yamaha FZS",
            "color": "Black",
            "capacity": 1,
            "status": "AVAILABLE",
        },
    )

    vehicle3, _ = Vehicle.objects.update_or_create(
        registration_number="DHAKA-METRO-CHA-778899",
        defaults={
            "vehicle_type": microbus,
            "driver": None,
            "model": "Toyota Hiace",
            "color": "Silver",
            "capacity": 10,
            "status": "AVAILABLE",
        },
    )

    vehicle4, _ = Vehicle.objects.update_or_create(
        registration_number="DHAKA-METRO-TR-998877",
        defaults={
            "vehicle_type": truck,
            "driver": None,
            "model": "Tata Pickup",
            "color": "Blue",
            "capacity": 2,
            "status": "AVAILABLE",
        },
    )

    # =========================
    # Completed Booking for customer2
    # =========================

    booking1, _ = Booking.objects.update_or_create(
        customer=customer2,
        pickup_location="Mirpur, Dhaka",
        dropoff_location="Banani, Dhaka",
        defaults={
            "vehicle_type": car,
            "pickup_latitude": Decimal("23.8067000"),
            "pickup_longitude": Decimal("90.3686000"),
            "dropoff_latitude": Decimal("23.7937000"),
            "dropoff_longitude": Decimal("90.4066000"),
            "distance_km": Decimal("8.20"),
            "estimated_fare": Decimal("305.00"),
            "status": "COMPLETED",
            "cancellation_reason": None,
        },
    )

    trip1, _ = Trip.objects.update_or_create(
        booking=booking1,
        defaults={
            "driver": driver1,
            "vehicle": vehicle1,
            "status": "COMPLETED",
            "start_time": timezone.now() - timedelta(hours=3),
            "end_time": timezone.now() - timedelta(hours=2),
            "actual_distance_km": Decimal("8.50"),
            "final_fare": Decimal("315.00"),
        },
    )

    payment1, _ = Payment.objects.update_or_create(
        booking=booking1,
        defaults={
            "customer": customer2,
            "amount": Decimal("315.00"),
            "payment_method": "BKASH",
            "transaction_id": "BKASH-TXN-123456",
            "gateway_payment_id": "BKASH-PAY-001",
            "gateway_callback_url": "http://localhost:5173/payment/success",
            "gateway_response": {
                "status": "success",
                "trxID": "BKASH-TXN-123456",
            },
            "status": "PAID",
            "paid_at": timezone.now() - timedelta(hours=1),
        },
    )

    Rating.objects.update_or_create(
        trip=trip1,
        defaults={
            "customer": customer2,
            "driver": driver1,
            "rating": 5,
            "review": "Driver was professional and reached on time.",
        },
    )

    # =========================
    # Pending Booking for customer2
    # =========================

    Booking.objects.update_or_create(
        customer=customer2,
        pickup_location="Uttara, Dhaka",
        dropoff_location="Dhanmondi, Dhaka",
        defaults={
            "vehicle_type": bike,
            "pickup_latitude": Decimal("23.8759000"),
            "pickup_longitude": Decimal("90.3795000"),
            "dropoff_latitude": Decimal("23.7465000"),
            "dropoff_longitude": Decimal("90.3760000"),
            "distance_km": Decimal("18.50"),
            "estimated_fare": Decimal("327.50"),
            "status": "PENDING",
            "cancellation_reason": None,
        },
    )

    # =========================
    # Assigned Booking for customer3
    # =========================

    booking3, _ = Booking.objects.update_or_create(
        customer=customer3,
        pickup_location="Gulshan, Dhaka",
        dropoff_location="Bashundhara, Dhaka",
        defaults={
            "vehicle_type": bike,
            "pickup_latitude": Decimal("23.7925000"),
            "pickup_longitude": Decimal("90.4078000"),
            "dropoff_latitude": Decimal("23.8103000"),
            "dropoff_longitude": Decimal("90.4125000"),
            "distance_km": Decimal("5.00"),
            "estimated_fare": Decimal("125.00"),
            "status": "ASSIGNED",
            "cancellation_reason": None,
        },
    )

    Trip.objects.update_or_create(
        booking=booking3,
        defaults={
            "driver": driver2,
            "vehicle": vehicle2,
            "status": "ASSIGNED",
            "start_time": None,
            "end_time": None,
            "actual_distance_km": None,
            "final_fare": None,
        },
    )

    # =========================
    # Complaints
    # =========================

    Complaint.objects.update_or_create(
        user=customer2,
        subject="Payment confirmation issue",
        defaults={
            "booking": booking1,
            "message": "I want to confirm whether my payment was received successfully.",
            "status": "RESOLVED",
            "admin_reply": "Your payment was received successfully.",
        },
    )

    Complaint.objects.update_or_create(
        user=customer2,
        subject="Driver arrival delay",
        defaults={
            "booking": booking1,
            "message": "The driver arrived a little late during my last trip.",
            "status": "OPEN",
            "admin_reply": "",
        },
    )

    # =========================
    # Notifications
    # =========================

    Notification.objects.update_or_create(
        user=customer2,
        title="Trip Completed",
        defaults={
            "message": "Your trip from Mirpur to Banani has been completed.",
            "is_read": False,
        },
    )

    Notification.objects.update_or_create(
        user=customer2,
        title="Payment Completed",
        defaults={
            "message": "Your bKash payment of BDT 315 has been completed.",
            "is_read": False,
        },
    )

    Notification.objects.update_or_create(
        user=driver1,
        title="Payment Completed",
        defaults={
            "message": "Payment for your completed trip has been processed.",
            "is_read": False,
        },
    )

    Notification.objects.update_or_create(
        user=driver2,
        title="New Trip Assigned",
        defaults={
            "message": "You have been assigned a new trip from Gulshan to Bashundhara.",
            "is_read": False,
        },
    )

    # =========================
    # Maintenance Records
    # =========================

    VehicleMaintenance.objects.update_or_create(
        vehicle=vehicle1,
        title="Engine oil replacement",
        defaults={
            "maintenance_type": "OIL_CHANGE",
            "description": "Regular oil change after long route usage.",
            "cost": Decimal("2700.00"),
            "scheduled_date": date.today(),
            "completed_date": date.today(),
            "service_provider": "Dhaka Auto Service",
            "status": "COMPLETED",
        },
    )

    VehicleMaintenance.objects.update_or_create(
        vehicle=vehicle2,
        title="Brake checkup",
        defaults={
            "maintenance_type": "BRAKE",
            "description": "Routine brake inspection.",
            "cost": Decimal("1200.00"),
            "scheduled_date": date.today() + timedelta(days=3),
            "completed_date": None,
            "service_provider": "Bike Care BD",
            "status": "SCHEDULED",
        },
    )

    VehicleMaintenance.objects.update_or_create(
        vehicle=vehicle3,
        title="General service",
        defaults={
            "maintenance_type": "GENERAL_SERVICE",
            "description": "General servicing before long-distance route.",
            "cost": Decimal("4500.00"),
            "scheduled_date": date.today() + timedelta(days=5),
            "completed_date": None,
            "service_provider": "Fleet Service Center",
            "status": "SCHEDULED",
        },
    )

    print("Database seeded successfully.")
    print("")
    print("Demo Login Credentials:")
    print("Admin    -> username: admin      password: admin123")
    print("Customer -> username: customer2  password: 123456")
    print("Customer -> username: customer3  password: 123456")
    print("Driver   -> username: driver1    password: 123456")
    print("Driver   -> username: driver2    password: 123456")


if __name__ == "__main__":
    run()