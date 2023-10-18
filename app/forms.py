from django import forms
import re
from .models import Admin,FacultyStaff


ROLE_CHOICES= [
    ('admin', 'Admin'),
    ('BU', 'Head of Business Unit'),
    ('dean', 'Dean of Collage'),
    ('facultyandstaff', 'Faculty/Staff Member'),
    ('Hkai', 'Head of KAI Business Unit'),
    ('kaistaff', 'KAI Business Unit Staff'),
    ]

class emailcheckform(forms.Form):
     email= forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Mail or Username'}))
     role= forms.CharField(label='Role', widget =forms.Select(choices=ROLE_CHOICES , attrs={'class': 'form-select text-center'}))
class ForgetPasswordForm(forms.Form):

  role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select())

class Loginform(forms.Form):
    email= forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' , 'placeholder': '*************'}))
    role= forms.CharField(label='Role', widget =forms.Select(choices=ROLE_CHOICES , attrs={'class': 'form-select text-center'}))
  
    
class adminform(forms.ModelForm):

     class Meta:
            model = Admin
            fields = ['email','password']
            widgets = {
            'password': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
                }),
            'email': forms.EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                })
        }


class FASform(forms.ModelForm):
     
     class Meta:
         model = FacultyStaff
         fields = [
            'first_name',
            'last_name',
            'phonenumber',
            'email',
            'gender',
            'nationality',
            'adminemail',
            'password',
            'employeeid',
            'position',
            'major',
            # 'collage'
            # 'specialization',
            # 'collage',
            # 'workstatus',
            # 'assignedorganization',
            # 'iban',
            # 'officeno',
            # 'researchinterest',
            # 'previouswork',
        ]
        #  '__all__'

class updateFASform(forms.ModelForm):
    # cv = forms.FileField(label='Select a file', required=False)
    class Meta:
         model = FacultyStaff
         fields = [
            'first_name',
            'last_name',
            'phonenumber',
            'email',
            'specialization',
            'workstatus',
            # 'assignedorganization',
            'iban',
            'officeno',
            # 'researchinterest',
            # 'previouswork',
            # 'cv'
        ]
         widgets = {
            'first_name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 250px;',
                }),
            'last_name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 250px;',
                }),
            'email': forms.EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'specialization': forms.TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'workstatus': forms.TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'phonenumber': forms.TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'email': forms.TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'iban': forms.TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'officeno': forms.TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
        }
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phonenumber')

        # Define a regular expression pattern for a valid phone number format
        # phone_number_pattern = r'^\d{10,15}$'
        phone_number_pattern = r'^\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'

        if not re.match(phone_number_pattern, phone_number):
            raise forms.ValidationError("Please enter a valid phone number.")

        return phone_number
  

