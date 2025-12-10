from django import forms
from .models import LeaveRequest, Department, LeaveBalance, EmployeeProfile
from .services import validate_leave_request
from django.contrib.auth import get_user_model

User = get_user_model()

class HREmployeeCreateForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    employee_code = forms.CharField(label="รหัสพนักงาน", max_length=20)
    department = forms.ModelChoiceField(
        label="แผนก",
        queryset=Department.objects.all(),
        required=False,
    )
    manager = forms.ModelChoiceField(
        label="หัวหน้า (ถ้ามี)",
        queryset=User.objects.all(),
        required=False,
    )


class EmployeeImportForm(forms.Form):
    file = forms.FileField(
        label="ไฟล์ Excel (.xlsx)",
        help_text="ไฟล์ต้องเป็น .xlsx หัวตารางแถวแรก"
    )

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["leave_type", "start_date", "end_date", "half_day", "reason", "attachment"]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "border p-2 rounded w-full"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "border p-2 rounded w-full"}
            ),
            "reason": forms.Textarea(
                attrs={"rows": 3, "class": "border p-2 rounded w-full"}
            ),
            "attachment": forms.ClearableFileInput(
                attrs={"class": "border p-2 rounded w-full text-sm"}
            ),
        }

    def __init__(self, *args, **kwargs):
        # เราส่ง employee_profile มาจาก view
        self.employee_profile = kwargs.pop("employee_profile", None)
        super().__init__(*args, **kwargs)

        self.fields["leave_type"].widget.attrs.update(
            {"class": "border p-2 rounded w-full"}
        )
        self.fields["half_day"].widget.attrs.update({"class": "mr-2"})

    def clean(self):
        cleaned = super().clean()

        if not self.employee_profile:
            return cleaned

        leave_type = cleaned.get("leave_type")
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")
        half_day = cleaned.get("half_day")
        attachment = cleaned.get("attachment")

        # ถ้า LeaveType นี้ require_attachment แต่ไม่ได้แนบไฟล์
        if leave_type and leave_type.require_attachment and not attachment:
            raise forms.ValidationError("ประเภทการลานี้ต้องแนบเอกสารประกอบ")

        if leave_type and start_date and end_date:
            validate_leave_request(
                self.employee_profile,
                leave_type,
                start_date,
                end_date,
                half_day,
                instance=self.instance,
            )

        return cleaned
    
class LeaveBalanceForm(forms.ModelForm):
    class Meta:
        model = LeaveBalance
        fields = ["allocated", "used"]
        widgets = {
            "allocated": forms.NumberInput(
                attrs={"step": "0.5", "class": "border p-2 rounded w-full text-sm"}
            ),
            "used": forms.NumberInput(
                attrs={"step": "0.5", "class": "border p-2 rounded w-full text-sm"}
            ),
        }

class HREmployeeCreateForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    employee_code = forms.CharField(label="รหัสพนักงาน", max_length=20)
    department = forms.ModelChoiceField(
        label="แผนก",
        queryset=Department.objects.all(),
        required=False,
    )
    manager = forms.ModelChoiceField(
        label="หัวหน้า (ถ้ามี)",
        queryset=User.objects.all(),
        required=False,
    )


class HREmployeeUpdateForm(forms.ModelForm):
    # ฟิลด์จาก User
    first_name = forms.CharField(label="ชื่อ", required=False)
    last_name = forms.CharField(label="นามสกุล", required=False)
    email = forms.EmailField(label="อีเมล", required=False)
    is_active = forms.BooleanField(label="ใช้งานอยู่", required=False)

    class Meta:
        model = EmployeeProfile
        fields = ["employee_code", "department", "manager", "join_date"]
        labels = {
            "employee_code": "รหัสพนักงาน",
            "department": "แผนก",
            "manager": "หัวหน้า",
            "join_date": "วันที่เริ่มงาน",
        }
        widgets = {
            "join_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ดึงค่าเริ่มต้นจาก user
        user = self.instance.user if self.instance and self.instance.pk else None
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email
            self.fields["is_active"].initial = user.is_active

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.email = self.cleaned_data.get("email", "")
        user.is_active = self.cleaned_data.get("is_active", True)

        if commit:
            user.save()
            profile.save()

        return profile


class EmployeeImportForm(forms.Form):
    file = forms.FileField(
        label="ไฟล์ Excel (.xlsx)",
        help_text="ไฟล์ต้องเป็น .xlsx หัวตารางแถวแรก"
    )


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["leave_type", "start_date", "end_date", "half_day", "reason", "attachment"]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "border p-2 rounded w-full"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "border p-2 rounded w-full"}
            ),
            "reason": forms.Textarea(
                attrs={"rows": 3, "class": "border p-2 rounded w-full"}
            ),
            "attachment": forms.ClearableFileInput(
                attrs={"class": "border p-2 rounded w-full text-sm"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.employee_profile = kwargs.pop("employee_profile", None)
        super().__init__(*args, **kwargs)

        self.fields["leave_type"].widget.attrs.update(
            {"class": "border p-2 rounded w-full"}
        )
        self.fields["half_day"].widget.attrs.update({"class": "mr-2"})

    def clean(self):
        cleaned = super().clean()

        if not self.employee_profile:
            return cleaned

        leave_type = cleaned.get("leave_type")
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")
        half_day = cleaned.get("half_day")
        attachment = cleaned.get("attachment")

        if leave_type and leave_type.require_attachment and not attachment:
            raise forms.ValidationError("ประเภทการลานี้ต้องแนบเอกสารประกอบ")

        if leave_type and start_date and end_date:
            validate_leave_request(
                self.employee_profile,
                leave_type,
                start_date,
                end_date,
                half_day,
            )

        return cleaned


class LeaveBalanceForm(forms.ModelForm):
    class Meta:
        model = LeaveBalance
        fields = ["allocated", "used"]
        widgets = {
            "allocated": forms.NumberInput(
                attrs={"step": "0.5", "class": "border p-2 rounded w-full text-sm"}
            ),
            "used": forms.NumberInput(
                attrs={"step": "0.5", "class": "border p-2 rounded w-full text-sm"}
            ),
        }

class EmployeeImportForm(forms.Form):
    file = forms.FileField(
        label="ไฟล์ Excel (.xlsx)",
        help_text="ไฟล์ต้องเป็น .xlsx หัวตารางแถวแรก"
    )

    def clean_file(self):
        f = self.cleaned_data["file"]
        if not f.name.lower().endswith(".xlsx"):
            raise forms.ValidationError("ไฟล์ต้องเป็นนามสกุล .xlsx เท่านั้น")
        return f
