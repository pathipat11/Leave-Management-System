import json

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone

from .models import EmployeeProfile, LeaveRequest


def is_ceo(user):
    return user.is_superuser or user.groups.filter(name="CEO").exists()


@user_passes_test(is_ceo)
def ceo_dashboard(request):
    year_param = request.GET.get("year")
    try:
        year = int(year_param) if year_param else timezone.now().year
    except ValueError:
        year = timezone.now().year

    total_employees = EmployeeProfile.objects.filter(
        user__is_active=True
    ).count()

    qs_year = LeaveRequest.objects.filter(start_date__year=year)

    total_requests = qs_year.count()
    pending_count = qs_year.filter(status=LeaveRequest.STATUS_PENDING).count()
    approved_count = qs_year.filter(status=LeaveRequest.STATUS_APPROVED).count()
    rejected_count = qs_year.filter(status=LeaveRequest.STATUS_REJECTED).count()
    cancelled_count = qs_year.filter(status=LeaveRequest.STATUS_CANCELLED).count()

    monthly_qs = (
        qs_year.annotate(month=TruncMonth("start_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    monthly_labels = [item["month"].strftime("%b") for item in monthly_qs]
    monthly_counts = [item["count"] for item in monthly_qs]

    dept_qs = (
        qs_year.values("employee__department__name")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    department_labels = [
        (item["employee__department__name"] or "No Dept") for item in dept_qs
    ]
    department_counts = [item["count"] for item in dept_qs]

    type_qs = (
        qs_year.values("leave_type__name")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    leave_type_labels = [item["leave_type__name"] for item in type_qs]
    leave_type_counts = [item["count"] for item in type_qs]

    context = {
        "year": year,
        "total_employees": total_employees,
        "total_requests": total_requests,
        "pending_count": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "cancelled_count": cancelled_count,
        "monthly_labels_json": json.dumps(monthly_labels),
        "monthly_counts_json": json.dumps(monthly_counts),
        "department_labels_json": json.dumps(department_labels),
        "department_counts_json": json.dumps(department_counts),
        "leave_type_labels_json": json.dumps(leave_type_labels),
        "leave_type_counts_json": json.dumps(leave_type_counts),
    }
    return render(request, "leave_app/ceo/ceo_dashboard.html", context)
