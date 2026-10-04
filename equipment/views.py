from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import RegisterForm
from .models import Equipment, Transaction


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


@login_required
def dashboard(request):
    equipment = Equipment.objects.all()[:8]
    recent_transactions = Transaction.objects.filter(user=request.user).order_by("-id")[:5]

    if request.user.is_staff:
        borrowed_count = Transaction.objects.filter(status="borrowed").count()
        returned_count = Transaction.objects.filter(status="returned").count()
    else:
        borrowed_count = Transaction.objects.filter(user=request.user, status="borrowed").count()
        returned_count = Transaction.objects.filter(user=request.user, status="returned").count()

    metrics = {
        "total_equipment": Equipment.objects.count(),
        "available": sum(item.available_quantity for item in Equipment.objects.all()),
        "borrowed": borrowed_count,
        "returned": returned_count,
    }

    return render(
        request,
        "dashboard.html",
        {
            "metrics": metrics,
            "equipment": equipment,
            "recent_transactions": recent_transactions,
            "page_title": "Dashboard",
        },
    )


@login_required
def equipment_list(request):
    equipment_list = Equipment.objects.all().order_by("category", "name")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "borrow":
            if request.user.is_staff:
                messages.error(request, "Only students can borrow equipment.")
                return redirect("equipment")

            equipment_id = request.POST.get("equipment_id")
            purpose = request.POST.get("purpose", "Research Project")
            location = request.POST.get("location", "IT Office")
            due_at_value = request.POST.get("due_at")

            item = Equipment.objects.get(id=equipment_id)
            if item.available_quantity <= 0:
                messages.error(request, "This equipment is currently unavailable.")
                return redirect("equipment")

            due_at = timezone.datetime.strptime(due_at_value, "%Y-%m-%dT%H:%M") if due_at_value else None
            Transaction.objects.create(
                equipment=item,
                user=request.user,
                purpose=purpose,
                location=location,
                due_at=timezone.make_aware(due_at, timezone.get_current_timezone()) if due_at else None,
                status="borrowed",
            )
            item.available_quantity -= 1
            item.save()
            messages.success(request, f"{item.name} borrowed successfully.")
            return redirect("equipment")

        if action == "return":
            transaction_id = request.POST.get("transaction_id")
            equipment_id = request.POST.get("equipment_id")

            transaction = Transaction.objects.filter(id=transaction_id, user=request.user).first()
            if transaction:
                transaction.status = "returned"
                transaction.returned_at = timezone.now()
                transaction.save()

                equipment = Equipment.objects.get(id=equipment_id)
                equipment.available_quantity += 1
                equipment.save()
                messages.success(request, "Equipment returned successfully.")
            else:
                messages.error(request, "Unable to process return.")
            return redirect("equipment")

    if request.user.is_staff:
        my_borrowings = Transaction.objects.select_related("equipment", "user").order_by("-id")[:20]
    else:
        my_borrowings = Transaction.objects.filter(user=request.user).select_related("equipment").order_by("-id")

    return render(
        request,
        "equipment.html",
        {
            "equipment": equipment_list,
            "my_borrowings": my_borrowings,
            "page_title": "Equipment",
        },
    )


@login_required
def reports(request):
    if not request.user.is_staff:
        messages.error(request, "Access restricted to staff only.")
        return redirect("dashboard")

    transactions = Transaction.objects.select_related("equipment", "user").order_by("-id")
    return render(request, "reports.html", {"transactions": transactions, "page_title": "Reports"})
