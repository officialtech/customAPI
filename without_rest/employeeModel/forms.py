
from django import forms
from .models import Student
from django.utils.translation import gettext, gettext_lazy as _

class StudentForm(forms.ModelForm):

    def clean_roll_no(self):
        roll_no = self.cleaned_data.get('roll_no')
        # print("Roll Number is...", roll_no)
        if roll_no <= 0:
            raise forms.ValidationError(_("Invaid value: %s" % roll_no), code="Invalid",)
        return roll_no

    def clean_registration_no(self):
        registration_no = self.cleaned_data.get('registration_no')
        if registration_no <= 100:
            raise forms.ValidationError(_("Registration Number cannot be zero or less than that"), code="Invalid", params={'value': '42'},)
        return registration_no

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) <= 2:
            raise forms.ValidationError("Invalid Name: %s" % name, code="Invalid")
        return name


    class Meta:
        model = Student
        fields = '__all__'