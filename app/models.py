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
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=130, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=130, blank=True, null=True)  # Field name made lowercase.
    adminemail = models.CharField(db_column='AdminEmail', blank=True, null=True)  # Field name made lowercase.
    is_staff = models.BooleanField(blank=True, null=True)
    employeeid = models.CharField(db_column='EmployeeID', max_length=130)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=130)  # Field name made lowercase.
    major = models.CharField(db_column='Major', max_length=130)  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=130, blank=True, null=True)  # Field name made lowercase.
    workstatus = models.CharField(db_column='WorkStatus', max_length=130, blank=True, null=True)  # Field name made lowercase.
    assignedorganization = models.CharField(db_column='assignedOrganization', max_length=130, blank=True, null=True)  # Field name made lowercase.
    iban = models.CharField(db_column='Iban', max_length=130, blank=True, null=True , default='SA')  # Field name made lowercase.
    officeno = models.CharField(db_column='OfficeNo', max_length=130, blank=True, null=True)  # Field name made lowercase.
    researchinterest = ArrayField(models.TextField(),blank=True, null=True,db_column='ResearchInterest',default=list)  # Field name made lowercase. This field type is a guess.
    previouswork = ArrayField(models.TextField(),blank=True, null=True,db_column='PreviousWork',default=list)  # Field name made lowercase. This field type is a guess.
    cv = models.BinaryField(db_column='CV', blank=True, null=True)  # Field name made lowercase.
    collageid = models.ForeignKey(Collage, models.DO_NOTHING, db_column='CollageID', blank=True, null=True)  # Field name made lowercase.
    is_buhead = models.BooleanField(db_column='is_BUhead', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(max_length=150, unique=True)
    department_field = models.CharField(db_column='Department')

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='faculty_staff'  # Provide a unique related name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='faculty_staff'  # Provide a unique related name
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
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=130, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=130, blank=True, null=True)  # Field name made lowercase.
    adminemail = models.CharField(db_column='AdminEmail', blank=True, null=True)  # Field name made lowercase.
    kaiemployeeid = models.CharField(db_column='KAIEmployeeID')  # Field name made lowercase.
    position = models.CharField(db_column='Position')  # Field name made lowercase.
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


class Project(models.Model):
    name = models.CharField(db_column='Name', max_length=130)  # Field name made lowercase.
    totalcost = models.FloatField(db_column='TotalCost', blank=True, null=True)  # Field name made lowercase.
    taxpercentage = models.FloatField(db_column='TaxPercentage', blank=True, null=True)  # Field name made lowercase.
    kaipercentage = models.FloatField(db_column='KAIPercentage', blank=True, null=True)  # Field name made lowercase.
    acceptancestatus = models.CharField(db_column='acceptanceStatus', max_length=130)  # Field name made lowercase.
    programtype = models.CharField(db_column='programType', max_length=130)  # Field name made lowercase.
    collage = models.CharField(db_column='Collage', max_length=130)  # Field name made lowercase.
    leaderid = models.CharField(db_column='LeaderID', max_length=130, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='startDate')  # Field name made lowercase.
    enddate = models.DateField(db_column='endDate')  # Field name made lowercase.
    adminemail = models.CharField(db_column='AdminEmail', max_length=130)  # Field name made lowercase.
    programstatus = models.TextField(db_column='programStatus')  # Field name made lowercase. This field type is a guess.
    companyname = models.CharField(db_column='companyName', max_length=130)  # Field name made lowercase.
    offeringdate = models.DateField(db_column='OfferingDate')  # Field name made lowercase.
    acceptancedeadline = models.DateField(db_column='AcceptanceDeadline')  # Field name made lowercase.
    questionsdeadline = models.DateField(db_column='QuestionsDeadline', blank=True, null=True)  # Field name made lowercase.
    etimaddeadline = models.DateField(db_column='EtimadDeadline', blank=True, null=True)  # Field name made lowercase.
    proposalsubmissiondeadline = models.DateField(db_column='ProposalSubmissionDeadline', blank=True, null=True)  # Field name made lowercase.
    contractduration = models.CharField(db_column='ContractDuration', max_length=130, blank=True, null=True)  # Field name made lowercase.
    envelopeopeningdate = models.DateField(db_column='EnvelopeOpeningDate', blank=True, null=True)  # Field name made lowercase.
    rejectionreason = models.CharField(db_column='RejectionReason', max_length=130, blank=True, null=True)  # Field name made lowercase.
    technicalproposalstatus = models.CharField(db_column='TechnicalProposalStatus', max_length=130, blank=True, null=True)  # Field name made lowercase.
    financialproposalstatus = models.CharField(db_column='FinancialProposalStatus', max_length=130, blank=True, null=True)  # Field name made lowercase.
    programid = models.AutoField(db_column='programID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Project'


class Register(models.Model):
    registerid = models.AutoField(db_column='RegisterID', primary_key=True)  # Field name made lowercase.
    programid = models.ForeignKey('Trainingprogram', models.DO_NOTHING, db_column='ProgramID')  # Field name made lowercase.
    registerstatus = models.CharField(db_column='RegisterStatus', max_length=130)  # Field name made lowercase.
    id = models.ForeignKey('Trainees', models.DO_NOTHING, db_column='id')

    class Meta:
        managed = False
        db_table = 'Register'


class Request(models.Model):
    requestid = models.AutoField(db_column='RequestID', primary_key=True)  # Field name made lowercase.
    documment = models.TextField(db_column='Documment')  # Field name made lowercase. This field type is a guess.
    id = models.ForeignKey(Kaibuemployee, models.DO_NOTHING, db_column='id')
    collageid = models.ForeignKey(Collage, models.DO_NOTHING, db_column='CollageID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Request'


class Trainees(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    certifications = models.TextField(blank=True, null=True)  # This field type is a guess.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=130, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=130, blank=True, null=True)  # Field name made lowercase.
    adminemail = models.CharField(db_column='AdminEmail', blank=True, null=True)  # Field name made lowercase.
    is_staff = models.BooleanField(blank=True, null=True)
    nationalid = models.CharField(db_column='NationalID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Trainees'


class Trainingprogram(models.Model):
    subject = models.CharField(max_length=130)
    totalcost = models.FloatField(db_column='TotalCost', blank=True, null=True)  # Field name made lowercase.
    taxpercentage = models.FloatField(db_column='TaxPercentage', blank=True, null=True)  # Field name made lowercase.
    kaipercentage = models.FloatField(db_column='KAIPercentage', blank=True, null=True)  # Field name made lowercase.
    programtype = models.CharField(db_column='programType', max_length=130)  # Field name made lowercase.
    startdate = models.DateField(db_column='startDate')  # Field name made lowercase.
    enddate = models.DateField(db_column='endDate')  # Field name made lowercase.
    starttime = models.TimeField(db_column='startTime')  # Field name made lowercase.
    endtime = models.TimeField(db_column='endTime')  # Field name made lowercase.
    capacity = models.IntegerField()
    attendeescount = models.IntegerField(db_column='AttendeesCount', blank=True, null=True)  # Field name made lowercase.
    programid = models.AutoField(db_column='programID', primary_key=True)  # Field name made lowercase.
    collageid = models.IntegerField(db_column='CollageID')  # Field name made lowercase.
    topic = models.CharField(db_column='Topic', max_length=500)  # Field name made lowercase.
    dataoffacultyproposal = models.DateField(db_column='dataOfFacultyProposal', blank=True, null=True)  # Field name made lowercase.
    dataofbuproposal = models.DateField(db_column='dataOfBuProposal', blank=True, null=True)  # Field name made lowercase.
    dataofbuacceptance = models.DateField(db_column='dataOfBuAcceptance', blank=True, null=True)  # Field name made lowercase.
    dataofburejection = models.DateField(db_column='dataOfBuRejection', blank=True, null=True)  # Field name made lowercase.
    dataofkaiacceptance = models.DateField(db_column='dataOfKaiAcceptance', blank=True, null=True)  # Field name made lowercase.
    dataoffacultyacceptance = models.DateField(db_column='dataOfFacultyAcceptance', blank=True, null=True)  # Field name made lowercase.
    dataofkairejection = models.DateField(db_column='dataOfKaiRejection', blank=True, null=True)  # Field name made lowercase.
    dataoffacultyrejection = models.DateField(db_column='dataOfFacultyRejection', blank=True, null=True)  # Field name made lowercase.
    isfacultyfound = models.BooleanField(blank=True, null=True)
    iskaiaccepted = models.BooleanField(blank=True, null=True)
    isreleased_field = models.BooleanField(db_column='isreleased ', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    attachment = models.BinaryField(db_column='Attachment', blank=True, null=True)  # Field name made lowercase.
    instructorid = models.IntegerField(db_column='InstructorID')  # Field name made lowercase.
    program_domain = models.CharField(db_column='Program_domain', max_length=130, blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'TrainingProgram'



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=130, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=130, blank=True, null=True)  # Field name made lowercase.
    adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail', blank=True, null=True)  # Field name made lowercase.
    is_staff = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Workson(models.Model):
    worksonid = models.AutoField(db_column='worksOnID', primary_key=True)  # Field name made lowercase.
    programid = models.ForeignKey(Trainingprogram, models.DO_NOTHING, db_column='programID')  # Field name made lowercase.
    employeepercentage = models.FloatField(db_column='employeePercentage')  # Field name made lowercase.
    id = models.ForeignKey(FacultyStaff, models.DO_NOTHING, db_column='id')

    class Meta:
        managed = False
        db_table = 'worksOn'
