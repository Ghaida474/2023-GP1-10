# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser , Group, Permission , UserManager
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import ArrayField

class Admin(models.Model):
    email = models.CharField(db_column='Email', primary_key=True, max_length=130)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=130)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Admin'


class Collage(models.Model):
    collageid = models.AutoField(db_column='CollageID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=130)  # Field name made lowercase.
    nostudents = models.IntegerField(db_column='NoStudents')  # Field name made lowercase.
    nofaculty = models.IntegerField(db_column='NoFaculty')  # Field name made lowercase.
    nostaff = models.IntegerField(db_column='NoStaff')  # Field name made lowercase.
    nofemalestudents = models.IntegerField(db_column='NoFemaleStudents', blank=True, null=True)  # Field name made lowercase.
    nomalestudents = models.IntegerField(db_column='NoMaleStudents', blank=True, null=True)  # Field name made lowercase.
    adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail')  # Field name made lowercase.
    departments = ArrayField(models.TextField(),db_column='Departments',default=list)   # Field name made lowercase. This field type is a guess.
    buemail = models.CharField(db_column='BUemail')  # Field name made lowercase.
    userid = models.ForeignKey('FacultyStaff', models.DO_NOTHING, db_column='userid')
    buphonenumber = models.CharField(db_column='BUphoneNumber')  # Field name made lowercase.
    password = models.CharField()
    domain = models.TextField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'Collage'


class FacultyStaff(AbstractUser):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254 , unique=True)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130, blank=True, null=True)  
    gender = models.CharField(db_column='Gender', max_length=130, blank=True, null=True)  
    nationality = models.CharField(db_column='Nationality', max_length=130, blank=True, null=True)  
    adminemail = models.CharField(db_column='AdminEmail', blank=True, null=True)  
    is_staff = models.BooleanField(blank=True, null=True)
    employeeid = models.CharField(db_column='EmployeeID', max_length=130)  
    position = models.CharField(db_column='Position', max_length=130) 
    major = models.CharField(db_column='Major', max_length=130) 
    specialization = models.CharField(db_column='Specialization', max_length=130, blank=True, null=True)
    workstatus = models.CharField(db_column='WorkStatus', max_length=130, blank=True, null=True) 
    assignedorganization = models.CharField(db_column='assignedOrganization', max_length=130, blank=True, null=True) 
    iban = models.CharField(db_column='Iban', max_length=130, blank=True, null=True , default='SA')  
    officeno = models.CharField(db_column='OfficeNo', max_length=130, blank=True, null=True) 
    researchinterest = ArrayField(models.TextField(),blank=True, null=True,db_column='ResearchInterest',default=list) 
    previouswork = ArrayField(models.TextField(),blank=True, null=True,db_column='PreviousWork',default=list) 
    cv = models.BinaryField(db_column='CV', blank=True, null=True) 
    collageid = models.ForeignKey(Collage, models.DO_NOTHING, db_column='CollageID', blank=True, null=True) 
    is_buhead = models.BooleanField(db_column='is_BUhead', blank=True, null=True) 
    username = models.CharField(max_length=150, unique=True)
    department_field = models.CharField(db_column='Department')
    rank = models.CharField(blank=True, null=True)
    first_nameeng = models.CharField(db_column='first_nameEng', blank=True, null=True)  # Field name made lowercase.
    last_nameeng = models.CharField(db_column='last_nameEng', blank=True, null=True)  # 

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='faculty_staff'  
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='faculty_staff'  
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name'] 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    objects = UserManager()

    class Meta:
        managed = False
        db_table = 'Faculty_Staff'


class Kaibuemployee(AbstractUser):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254 , unique=True)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130, blank=True, null=True)  
    gender = models.CharField(db_column='Gender', max_length=130, blank=True, null=True)  
    nationality = models.CharField(db_column='Nationality', max_length=130, blank=True, null=True) 
    adminemail = models.CharField(db_column='AdminEmail', blank=True, null=True)  
    kaiemployeeid = models.CharField(db_column='KAIEmployeeID') 
    position = models.CharField(db_column='Position') 
    is_staff = models.BooleanField(blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='kaibuemployee_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='kaibuemployee_permissions'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']  

    objects = UserManager()
    
    class Meta:
        managed = False
        db_table = 'KAIBUEmployee'



class Register(models.Model):
    registerid = models.AutoField(db_column='RegisterID', primary_key=True)  # Field name made lowercase.
    programid = models.ForeignKey('Trainingprogram', models.DO_NOTHING, db_column='ProgramID')  # Field name made lowercase.
    id = models.ForeignKey('Trainees', models.DO_NOTHING, db_column='id')
    certifications = models.TextField(blank=True, null=True , db_column='certifications')
    certifications_ext = models.CharField(blank=True, null=True , db_column='certifications_ext')
    hasregistered = models.BooleanField(db_column='hasRegistered', blank=True, null=True)  # Field name made lowercase.
    haspaid = models.BooleanField(blank=True, null=True , default=False)
    hasattended = models.BooleanField(db_column='hasAttended', blank=True, null=True , default=False)  # Field name made lowercase.
    refundrequsted = models.BooleanField(db_column='refundRequsted', blank=True, null=True , default=False)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'Register'



class Trainees(models.Model):
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150 , db_column='first_name')
    last_name = models.CharField(max_length=150 , db_column='last_name')
    email = models.CharField(max_length=254)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130, blank=True, null=True)  
    gender = models.CharField(db_column='Gender', max_length=130, blank=True, null=True)
    # nationality = models.CharField(db_column='Nationality', max_length=130, blank=True, null=True)
    adminemail = models.CharField(db_column='AdminEmail', blank=True, null=True)
    nationalid = models.CharField(db_column='NationalID', blank=True, null=True)
    fullnamearabic = models.CharField(db_column='fullNameArabic', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Trainees'


INITIATED_BY_CHOICES = [
        ('FacultyOrStaff', 'FacultyOrStaff'),
        ('bu', 'bu'),
        ('kai', 'kai'),
    ]

class Trainingprogram(models.Model):
    Descriptionofrequirements = models.CharField(max_length=130 , db_column='Descriptionofrequirements')
    totalcost = models.FloatField(db_column='TotalCost', blank=True, null=True)  
    taxpercentage = models.FloatField(db_column='TaxPercentage', blank=True, null=True)  
    kaipercentage = models.FloatField(db_column='KAIPercentage', blank=True, null=True)  
    programtype = models.CharField(db_column='programType', max_length=130)  
    startdate = models.DateField(db_column='startDate')  
    enddate = models.DateField(db_column='endDate')  
    starttime = models.TimeField(db_column='startTime')
    endtime = models.TimeField(db_column='endTime') 
    capacity = models.IntegerField()
    attendeescount = models.IntegerField(db_column='AttendeesCount', blank=True, null=True) 
    programid = models.AutoField(db_column='programID', primary_key=True) 
    collageid = models.IntegerField(db_column='CollageID') 
    topic = models.CharField(db_column='Topic', max_length=500) 
    dataoffacultyproposal = models.DateField(db_column='dataOfFacultyProposal', blank=True, null=True) 
    dataofburejection = models.DateField(db_column='dataOfBuRejection', blank=True, null=True) 
    dataofkairejection = models.DateField(db_column='dataOfKaiRejection', blank=True, null=True) 
    isfacultyfound = models.BooleanField(blank=True, null=True)
    iskaiaccepted = models.BooleanField(blank=True, null=True)
    isreleased_field = models.BooleanField(db_column='isreleased ', blank=True, null=True)  
    attachment = models.BinaryField(db_column='Attachment', blank=True, null=True)  
    instructorid = ArrayField(models.IntegerField(), default=list, blank=True, null=True , db_column='InstructorID')
    program_domain = models.CharField(db_column='Program_domain',max_length=130, blank=True, null=True)
    isbuaccepted = models.BooleanField(db_column='isbuaccepted', blank=True, null=True)
    initiatedby = models.CharField(db_column='initiatedby',choices=INITIATED_BY_CHOICES,blank=True,null=True,)
    status = models.CharField(db_column='status', max_length=130, blank=True, null=True)
    cost = models.FloatField()
    costtype = models.CharField(db_column='costType', max_length=130)
    attachment_name = models.CharField(db_column='Attachment_name', max_length=130, blank=True, null=True) 
    num_ofinstructors = models.IntegerField(db_column='num_ofInstructors', blank=True, null=True)
    rejectionresons = models.CharField(max_length=500, blank=True, null=True)
    programleader = models.IntegerField(blank=True, null=True)
    lastenrollmentdate = models.DateField(blank=True, null=True)
    programdescription = models.CharField(db_column='programDescription', max_length=300, blank=True, null=True) 
    appourtunityopentoall = models.BooleanField(blank=True, null=True)
    programdescription_english = models.CharField(db_column='programDescription_english', max_length=300, blank=True, null=True)  
    isonline = models.BooleanField(db_column='isOnline', blank=True, null=True) 
    location_field = models.CharField(db_column='location ', max_length=130, blank=True, null=True) 
    topic_english = models.CharField(max_length=130, blank=True, null=True)
    # adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail', blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'TrainingProgram'




class IdStatusDate(models.Model):
    instructor = models.ForeignKey('FacultyStaff', on_delete=models.CASCADE, db_column='instructorid', null=True)
    status = models.CharField(max_length=130, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    training_program = models.ForeignKey('TrainingProgram', on_delete=models.CASCADE, db_column='training_program')
    rejectionresons = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'WorksOn'



class StatusDateCheck(models.Model):
    status = models.CharField(max_length=130, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    indicator = models.CharField(max_length=1, blank=True, null=True)
    training_program =models.ForeignKey('TrainingProgram', on_delete=models.CASCADE, db_column='training_program')

    class Meta:
        managed = False
        db_table = 'Trainingprogram _status'


