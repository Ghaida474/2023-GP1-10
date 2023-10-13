from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Admin,User,FacultyAndStaff,Businessunit,Kai,Collage,Program,Project,Register,Request,Trainee,Trainingprogram


ROLE_CHOICES= [
    ('admin', 'Admin'),
    ('BU', 'Head of Business Unit'),
    ('dean', 'Dean of Collage'),
    ('facultyandstaff', 'Faculty Member'),
    ('Hkai', 'Head of KAI Business Unit'),
    ('kaistaff', 'KAI Business Unit Staff'),
    ]


class Loginform(forms.Form):
    email= forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Mail or Username'}))
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
         model = FacultyAndStaff
         fields = [
            'firstname',
            'lastname',
            'phonenumber',
            'email',
            'gender',
            'nationality',
            'adminemail',
            'password',
            'employeeid',
            'position',
            'major',
            'collage'
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

