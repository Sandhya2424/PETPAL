from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import razorpay
import uuid

from groomingpet.models import Appointment
from groomingpet.forms import AppointmentForm

# --------------------------
# Razorpay Test Keys
# --------------------------
RAZORPAY_KEY_ID = "rzp_test_RrnpiKmyBDnWOF"
RAZORPAY_KEY_SECRET = "Fvlj6kxEDiUa27geptyCUbjI"

# --------------------------
# Services & Prices
# --------------------------
SERVICES = ['Basic', 'Basic + Hygiene', 'Essential', 'Advance', 'Haircut']
SERVICE_PRICES = {
    'Basic': 999,
    'Basic + Hygiene': 1199,
    'Essential': 1499,
    'Advance': 1999,
    'Haircut': 1199,
}

# --------------------------
# 1) SHOW SERVICES
# --------------------------
class ServicesView(View):
    def get(self, request):
        return render(request, 'services.html', {'services': SERVICES})

# --------------------------
# 2) BOOK APPOINTMENT
# --------------------------
class BookAppointmentView(View):
    def get(self, request, service_name):
        form = AppointmentForm()

        # Calculate remaining slots per time slot (ignores date for simplicity)
        updated_choices = []
        for slot, _ in form.fields['time_slot'].choices:
            booked_count = Appointment.objects.filter(
                service=service_name,
                time_slot=slot,
                is_cancelled=False
            ).count()
            remaining_slots = max(0, 5 - booked_count)
            updated_choices.append((slot, f"{slot} ({remaining_slots}/5 slots available)"))
        form.fields['time_slot'].choices = updated_choices

        return render(request, "book_appointment.html", {
            "form": form,
            "service_name": service_name
        })

    def post(self, request, service_name):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.adopter = request.user
            appointment.service = service_name
            appointment.amount = SERVICE_PRICES[service_name]
            appointment.save()
            return redirect('groomingpet:checkout', appointment.id)

        return render(request, "book_appointment.html", {
            "form": form,
            "service_name": service_name
        })

# --------------------------
# 3) CHECKOUT (COD + ONLINE)
# --------------------------
class CheckoutView(View):
    def get(self, request, appointment_id):
        appointment = Appointment.objects.get(id=appointment_id)
        return render(request, "checkout.html", {"appointment": appointment})

    def post(self, request, appointment_id):
        appointment = Appointment.objects.get(id=appointment_id)
        payment_method = request.POST.get("payment_method")

        # ---------- ONLINE PAYMENT ----------
        if payment_method == "online":
            client = razorpay.Client(
                auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
            )
            payment = client.order.create({
                "amount": appointment.amount * 100,
                "currency": "INR",
                "payment_capture": 1
            })
            appointment.order_id = payment["id"]
            appointment.payment_method = "online"
            appointment.save()
            return render(request, "payment.html", {
                "payment": payment,
                "appointment": appointment
            })

        # ---------- CASH ON DELIVERY ----------
        appointment.is_paid = True
        appointment.order_id = "COD_" + uuid.uuid4().hex[:10]
        appointment.payment_method = "cod"
        appointment.save()
        return render(request, "payment.html", {"appointment": appointment})

# --------------------------
# 4) PAYMENT SUCCESS (ONLINE)
# --------------------------
@method_decorator(csrf_exempt, name="dispatch")
class PaymentSuccessView(View):
    def post(self, request, username):
        order_id = request.POST.get("razorpay_order_id")
        appointment = Appointment.objects.get(order_id=order_id)
        appointment.is_paid = True
        appointment.save()

        user = User.objects.get(username=username)
        login(request, user)

        return render(request, "payment_success.html", {
            "appointment": appointment
        })

# --------------------------
# 5) ADOPTER - MY BOOKINGS
# --------------------------
def MyBookingsView(request):
    bookings = Appointment.objects.filter(adopter=request.user).order_by('-date', '-time_slot')
    return render(request, "my_bookings.html", {"bookings": bookings})

# --------------------------
# 6) GROOMER - ALL BOOKINGS
# --------------------------
def AllBookingsView(request):
    bookings = Appointment.objects.all().order_by('-date', '-time_slot')
    return render(request, "bookings.html", {"bookings": bookings})
