from django import forms
import re
from .models import Admin,FacultyStaff,Kaibuemployee
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password



ROLE_CHOICES= [
    
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
    password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control' , 'placeholder': '*************'}))
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
        ]

class updateFASform(forms.ModelForm):
    cv = forms.FileField(label='Upload your CV (PDF only)', required=False)

    class Meta:
         model = FacultyStaff
         fields = ['username', 'phonenumber', 'email','specialization','iban','officeno']
         labels = {
            'phonenumber': 'Mobile Number',
            'iban':'IBAN',
            'officeno':'OfficeNo',
        }
         widgets = {
            'username': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 250px;',
                }),
            'email': forms.EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'specialization': forms.TextInput(attrs={
                'placeholder': 'Specialization',
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'phonenumber': forms.TextInput(attrs={
                'placeholder': '05**********',
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'email': forms.TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'iban': forms.TextInput(attrs={
                'placeholder': 'SA**********************', 
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'officeno': forms.TextInput(attrs={
                'placeholder': 'OfficeNo',
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
        }
         
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        if not username:
            raise ValidationError("Username cannot be empty.")
        if len(username) < 10 or username[0].isdigit():
            raise ValidationError("Username must be at least 10 characters and not start with a digit.")

        # Check if the username is already in use
        if FacultyStaff.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This username is already in use.")
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
 
            # Add your custom email validation logic here
        if not email.endswith('ksu.edu.sa'):
            raise forms.ValidationError('Email must be from ksu.edu.sa')
           
        if email.find('@') == -1:
            raise forms.ValidationError('Email must contain the "@" symbol.')
            
        if not email:
            raise ValidationError("Email cannot be empty.")
        
        return email
    
    def clean_phonenumber(self):
        phonenumber = self.cleaned_data['phonenumber']

        if not phonenumber:
            raise ValidationError("Mobile number cannot be empty.")
        
        if  not phonenumber.isdigit():
            raise ValidationError("Mobile number must start with '05' and be exactly 10 digits long.")
        
        if not phonenumber.startswith('05'): 
             raise ValidationError("Mobile number must start with '05.")

        if  len(phonenumber) != 10:
            raise ValidationError("Mobile number be exactly 10 digits long.")

        return phonenumber

    def clean_specialization(self):
        specialization = self.cleaned_data['specialization']
        if specialization is not None:
            if len(specialization) < 5 or specialization.isdigit():
                raise ValidationError("Specialization must be at least 5 characters and not contain only digits.")

            return specialization

    def clean_iban(self):
        iban = self.cleaned_data['iban']
        if iban is not None:
            if not iban.lower().startswith('sa') or not iban[2:].isdigit() or len(iban) != 24:
                raise ValidationError("IBAN must start with 'SA' and be exactly 24 digits long after 'SA.")
            iban = 'SA' + iban[2:]
            return iban
    
    def clean_cv(self):
        cv_file = self.cleaned_data.get('cv')
        if cv_file is not None:
            if cv_file:
                if not cv_file.name.endswith('.pdf'):
                    raise forms.ValidationError('CV must be in PDF format.')

            return cv_file 

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    role = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Invalid email format")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")
        return password

class previousworkform(forms.ModelForm):

    class Meta:
          model = FacultyStaff
          fields = [
             'previouswork',
             'researchinterest',
         ]
          labels = {
            'previouswork': 'Previous Work',
            'researchinterest':'Research Interest',
        }
          widgets = {
             'previouswork': forms.TextInput(attrs={
                     'placeholder': 'Previous Work',
                     'class': "form-control", 
                     'style': 'max-width: 220px;',
                     }),
            'researchinterest': forms.TextInput(attrs={
                     'placeholder':'Research Interest',
                     'class': "form-control", 
                     'style': 'max-width: 220px;',
                     }),
            }
            
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'}),
    )
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password' }),
    )
    confirm_password = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password' }),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        user = self.user

        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # Check if the current password is correct
        if not user.check_password(current_password):
            raise forms.ValidationError("Current password does not match the your password.")

        # Check if the new password and confirmation password match
        if new_password != confirm_password:
            raise forms.ValidationError("New password and confirmation password do not match.")

        # Validate the new password based on Django's built-in password validation
        try:
            password_validation.validate_password(new_password, user=user)
        except forms.ValidationError as e:
            self.add_error('new_password', e)

        return cleaned_data

class updateKai(forms.ModelForm):
    class Meta:
                model = Kaibuemployee
                fields = ['phonenumber']
                widgets = {
                'phonenumber': forms.TextInput(attrs={
                'placeholder': '05**********',
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
              
            }
    def clean_phonenumber(self):
        phonenumber = self.cleaned_data['phonenumber']

        if not phonenumber:
            raise ValidationError("Mobile number cannot be empty.")
        
        if  not phonenumber.isdigit():
            raise ValidationError("Mobile number must start with '05' and be exactly 10 digits long.")
        
        if not phonenumber.startswith('05'): 
             raise ValidationError("Mobile number must start with '05.")

        if  len(phonenumber) != 10:
            raise ValidationError("Mobile number be exactly 10 digits long.")

        return phonenumber


          



    