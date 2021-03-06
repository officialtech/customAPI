
from django import forms
from .models import Student
from django.utils.translation import gettext, gettext_lazy as _

class StudentForm(forms.ModelForm):

    def clean_roll_no(self):
        """
            custom validation for `roll_no`, please keep remember
            ALERT:
                if you will write method name like <clean_modelFieldName(self)>
                forms will call it underthehood, no need to call by you
        """
        roll_no = self.cleaned_data.get('roll_no')
        if roll_no <= 0:
            raise forms.ValidationError(_("Invaid roll number cannot be %s" % roll_no), code="Invalid",)
        return roll_no

    def clean_registration_no(self):
        registration_no = self.cleaned_data.get('registration_no')
        if registration_no <= 100:
            raise forms.ValidationError(_("Registration number must be more than 100"), code="Invalid", params={'value': '42'},)
        return registration_no

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) <= 2:
            raise forms.ValidationError("Invalid Name: %s" % name, code="Invalid")
        return name


    class Meta:
        model = Student
        fields = '__all__'