from django import forms
import re
from .models import Admin,FacultyStaff,Kaibuemployee,Trainingprogram
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password




ROLE_CHOICES= [
    
    ('BU', 'رئيس وحدة الأعمال'),
    ('dean', 'عميد الكلية'),
    ('facultyandstaff', 'عضو هيئة التدريس - موظف/ة'),
    ('Hkai', 'رئيس قسم وحدات الأعمال بمعهد الملك عبدالله'),
    ('kaistaff', 'موظف بقسم وحدات الأعمال بمعهد الملك عبدالله'),
    ]

class emailcheckform(forms.Form):
     email= forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}))
     role= forms.CharField(label='Role', widget =forms.Select(choices=ROLE_CHOICES , attrs={'class': 'form-select text-center'}))


class ForgetPasswordForm(forms.Form):
  role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select())


class Loginform(forms.Form):
    email= forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'البريد الإلكتروني'}))
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
    cv = forms.FileField(label='قم بتحميل سيرتك الذاتية (PDF فقط)', required=False)

    class Meta:
         model = FacultyStaff
         fields = ['username', 'phonenumber','specialization','iban','officeno']
         labels = {
            'username':'اسم المستخدم',
            'phonenumber': 'رقم الهاتف المحمول',
            'iban':'الإيبان',
            'officeno':'رقم المكتب',
            'specialization':'التخصص الدقيق'
        }
         widgets = {
            'username': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 250px;',
                }),
            'specialization': forms.TextInput(attrs={
                'placeholder': 'التخصص الدقيق',
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'phonenumber': forms.TextInput(attrs={
                'placeholder': '05**********',
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'iban': forms.TextInput(attrs={
                'placeholder': 'SA**********************', 
                'class': "form-control", 
                'style': 'max-width: 250px;',
                }),
            'officeno': forms.TextInput(attrs={
                'placeholder': 'رقم المكتب',
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
            raise ValidationError("يجب أن لا يقل اسم المستخدم عن 10 أحرف وألا يبدأ برقم.")

        # Check if the username is already in use
        if FacultyStaff.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("اسم المستخدم هذا تم استخدامه.")
    
    
    def clean_phonenumber(self):
        phonenumber = self.cleaned_data['phonenumber']

        if not phonenumber:
            raise ValidationError("لا يمكن أن يكون رقم الهاتف المحمول فارغا.")
        
        if  not phonenumber.isdigit():
            raise ValidationError("يجب أن يبدأ رقم الهاتف المحمول بـ '05' وأن يتكون من 10 أرقام بالضبط.")
        
        if not phonenumber.startswith('05'): 
             raise ValidationError("'رقم الهاتف المحمول يجب أن يبدأ بـ '05.")

        if  len(phonenumber) != 10:
            raise ValidationError("رقم الهاتف المحمول يجب أن يتكون من 10 أرقام بالضبط.")

        return phonenumber

    def clean_specialization(self):
        specialization = self.cleaned_data['specialization']
        if specialization is not None:
            if len(specialization) < 5 or specialization.isdigit():
                raise ValidationError("يجب أن لا يقل التخصص الدقيق عن 5 أحرف ولا يحتوي على أرقام فقط.")

            return specialization

    def clean_iban(self):
        iban = self.cleaned_data['iban']
        if iban is not None:
            if not iban.lower().startswith('sa') or not iban[2:].isdigit() or len(iban) != 24:
                raise ValidationError("يجب أن يبدأ الإيبان بـ 'SA' ويتكون من رقم 22 بالضبط بعد 'SA'.")
            iban = 'SA' + iban[2:]
            return iban
    
    def clean_cv(self):
        cv_file = self.cleaned_data.get('cv')
        if cv_file is not None:
            if cv_file:
                if not cv_file.name.endswith('.pdf'):
                    raise forms.ValidationError('يجب أن تكون السيرة الذاتية بصيغة PDF.')

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
            'previouswork': 'الأعمال السابقة',
            'researchinterest':'الإهتمامات',
        }
          widgets = {
             'previouswork': forms.TextInput(attrs={
                     'placeholder': 'الأعمال السابقة',
                     'class': "form-control", 
                     'style': 'max-width: 220px;',
                     }),
            'researchinterest': forms.TextInput(attrs={
                     'placeholder':'الإهتمامات',
                     'class': "form-control", 
                     'style': 'max-width: 220px;',
                     }),
            }
            
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="كلمة السر الحالية",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة السر الحالية' }),
    )
    new_password = forms.CharField(
        label="كلمة السر الجديدة ",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة السر الجديدة ' }),
    )
    confirm_password = forms.CharField(
        label="تأكيد كلمة المرور الجديدة",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تأكيد كلمة المرور الجديدة' }),
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
            raise forms.ValidationError("كلمة المرور الحالية لا تتطابق مع كلمة المرور الخاصة بك.")

        # Check if the new password and confirmation password match
        if new_password != confirm_password:
            raise forms.ValidationError("كلمة المرور الجديدة وكلمة مرور التأكيد غير متطابقتين.")

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
                labels = {
                    'phonenumber': 'رقم الهاتف المحمول',
                }
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
            raise ValidationError("لا يمكن أن يكون رقم الهاتف المحمول فارغا.")
        
        if  not phonenumber.isdigit():
            raise ValidationError("يجب أن يبدأ رقم الهاتف المحمول بـ '05' وأن يتكون من 10 أرقام بالضبط.")
        
        if not phonenumber.startswith('05'): 
             raise ValidationError("'رقم الهاتف المحمول يجب أن يبدأ بـ '05.")

        if  len(phonenumber) != 10:
            raise ValidationError("رقم الهاتف المحمول يجب أن يتكون من 10 أرقام بالضبط.")

        return phonenumber


'''class TrainingProgramForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the 'user' argument if passed
        super(TrainingProgramForm, self).__init__(*args, **kwargs)
        
        # Filter the queryset of faculty members based on the user's collage
        if user:
            collage_id = user.collageid.collageid
            faculty_members = FacultyStaff.objects.filter(collageid =collage_id)
            queryset = faculty_members

    reqType = forms.ChoiceField(
        choices=[('دورة تدريبية', 'دورة تدريبية'), ('ورشة عمل', 'ورشة عمل')],
        label="النوع",
    )
    topic = forms.CharField(label="الموضوع", max_length=255)
    domain = forms.CharField(label="المجال", required=False)
    price = forms.IntegerField(label="السعر")
    numoftrainee = forms.IntegerField(label="عدد المتدربين")
    instructor = forms.ModelMultipleChoiceField(
        queryset= ,
        label="المدرب",
        widget=forms.SelectMultiple(attrs={'class': 'form-control custom-select select2'}),
    )
    statedate = forms.DateField(label="تاريخ البداية", input_formats=['%Y-%m-%d'])
    enddate = forms.DateField(label="تاريخ الانتهاء", input_formats=['%Y-%m-%d'])
    starttime = forms.TimeField(label="وقت البداية", input_formats=['%H:%M'])
    endtime = forms.TimeField(label="وقت الانتهاء", input_formats=['%H:%M'])
    subject = forms.CharField(label="وصف المتطلبات", widget=forms.Textarea)
    attachment = forms.FileField(label="ارفاق ملف", required=False)'''

