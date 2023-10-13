# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Admin(models.Model):
    email = models.CharField(db_column='Email', primary_key=True, max_length=130)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=130)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Admin'


class Businessunit(models.Model):
    buemail = models.CharField(db_column='BUemail', primary_key=True, max_length=130)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130)  # Field name made lowercase.
    collageid = models.ForeignKey('Collage', models.DO_NOTHING, db_column='CollageID')  # Field name made lowercase.
    employeeid = models.ForeignKey('FacultyAndStaff', models.DO_NOTHING, db_column='EmployeeID')  # Field name made lowercase.
    adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail')  # Field name made lowercase.
    password = models.CharField(max_length=130)

    class Meta:
        managed = False
        db_table = 'BusinessUnit'


class Collage(models.Model):
    collageid = models.IntegerField(db_column='CollageID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=130)  # Field name made lowercase.
    nostudents = models.IntegerField(db_column='NoStudents')  # Field name made lowercase.
    nofaculty = models.IntegerField(db_column='NoFaculty')  # Field name made lowercase.
    nostaff = models.IntegerField(db_column='NoStaff')  # Field name made lowercase.
    nofemalestudents = models.IntegerField(db_column='NoFemaleStudents', blank=True, null=True)  # Field name made lowercase.
    nomalestudents = models.IntegerField(db_column='NoMaleStudents', blank=True, null=True)  # Field name made lowercase.
    # employeeid = models.ForeignKey('FacultyAndStaff', models.DO_NOTHING, db_column='EmployeeID')  # Field name made lowercase.
    adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail')  # Field name made lowercase.
    departments = models.TextField(db_column='Departments')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Collage'


class FacultyAndStaff(models.Model):
    firstname = models.CharField(db_column='firstName', max_length=130)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=130)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130)  # Field name made lowercase.
    email = models.CharField(max_length=130)
    # userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=130)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=130)  # Field name made lowercase.
    adminemail = models.CharField(db_column='AdminEmail', max_length=130)  # Field name made lowercase.
    password = models.CharField(max_length=130)
    employeeid = models.CharField(db_column='EmployeeID', primary_key=True, max_length=130)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=130)  # Field name made lowercase.
    major = models.CharField(db_column='Major', max_length=130)  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=130, blank=True, null=True)  # Field name made lowercase.
    collage = models.CharField(db_column='Collage', max_length=130)  # Field name made lowercase.
    # workstatus = models.CharField(db_column='WorkStatus', max_length=130)  # Field name made lowercase.
    # assignedorganization = models.CharField(db_column='assignedOrganization', max_length=130, blank=True, null=True)  # Field name made lowercase.
    # cv = ArrayField(models.CharField(max_length=50, blank=True), blank=True) # Field name made lowercase. This field type is a guess.
    # iban = models.CharField(db_column='Iban', max_length=130)  # Field name made lowercase.
    # officeno = models.CharField(db_column='OfficeNo', max_length=130 ,blank=True, null=True)  # Field name made lowercase.
    # researchinterest = ArrayField(models.CharField(max_length=50, blank=True),  blank=True) # Field name made lowercase. This field type is a guess.
    # previouswork = ArrayField(models.CharField(max_length=50, blank=True), blank=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Faculty and staff'



class Kai(models.Model):
    firstname = models.CharField(db_column='firstName', max_length=130)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=130)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130)  # Field name made lowercase.
    email = models.CharField(max_length=130)
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=130, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=130, blank=True, null=True)  # Field name made lowercase.
    adminemail = models.CharField(db_column='AdminEmail', max_length=130)  # Field name made lowercase.
    password = models.CharField(max_length=130)
    kaiemployeeid = models.CharField(db_column='KAIEmployeeID', primary_key=True, max_length=130)  # Field name made lowercase.
    kaiposition = models.CharField(db_column='KAIPosition', max_length=130)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KAI'


class Program(models.Model):
    programid = models.IntegerField(db_column='ProgramID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=130)  # Field name made lowercase.
    totalcost = models.FloatField(db_column='TotalCost', blank=True, null=True)  # Field name made lowercase.
    taxpercentage = models.FloatField(db_column='TaxPercentage', blank=True, null=True)  # Field name made lowercase.
    kaipercentage = models.FloatField(db_column='KAIPercentage', blank=True, null=True)  # Field name made lowercase.
    acceptancestatus = models.CharField(db_column='acceptanceStatus', max_length=130)  # Field name made lowercase.
    programtype = models.CharField(db_column='programType', max_length=130)  # Field name made lowercase.
    collage = models.CharField(db_column='Collage', max_length=130)  # Field name made lowercase.
    leaderid = models.CharField(db_column='LeaderID', max_length=130, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='endDate', blank=True, null=True)  # Field name made lowercase.
    adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail')  # Field name made lowercase.
    programstatus = models.TextField(db_column='programStatus')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Program'


class Project(models.Model):
    programid = models.IntegerField(db_column='ProgramID')  # Field name made lowercase.
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

    class Meta:
        managed = False
        db_table = 'Project'


class Register(models.Model):
    registerid = models.IntegerField(db_column='RegisterID', primary_key=True)  # Field name made lowercase.
    nationalid = models.ForeignKey('Trainee', models.DO_NOTHING, db_column='NationalID')  # Field name made lowercase.
    trainingprogramid = models.ForeignKey('Trainingprogram', models.DO_NOTHING, db_column='TrainingProgramID')  # Field name made lowercase.
    registerstatus = models.CharField(db_column='RegisterStatus', max_length=130)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Register'


class Request(models.Model):
    requestid = models.IntegerField(db_column='RequestID', primary_key=True)  # Field name made lowercase.
    buemail = models.ForeignKey(Businessunit, models.DO_NOTHING, db_column='BUemail')  # Field name made lowercase.
    kaiemployeeid = models.ForeignKey(Kai, models.DO_NOTHING, db_column='KAIEmployeeID')  # Field name made lowercase.
    documment = models.TextField(db_column='Documment')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Request'


class Trainee(models.Model):
    firstname = models.CharField(db_column='firstName', max_length=130)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=130)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130)  # Field name made lowercase.
    email = models.CharField(max_length=130)
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=130, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=130, blank=True, null=True)  # Field name made lowercase.
    adminemail = models.CharField(db_column='AdminEmail', max_length=130)  # Field name made lowercase.
    password = models.CharField(max_length=130)
    certifications = models.TextField(blank=True, null=True)  # This field type is a guess.
    nationalid = models.CharField(db_column='NationalID', primary_key=True, max_length=130)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Trainee'


class Trainingprogram(models.Model):
    programid = models.IntegerField(db_column='ProgramID')  # Field name made lowercase.
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
    starttime = models.TimeField(db_column='startTime')  # Field name made lowercase.
    endtime = models.TimeField(db_column='endTime')  # Field name made lowercase.
    capacity = models.IntegerField()
    attendeescount = models.IntegerField(db_column='AttendeesCount', blank=True, null=True)  # Field name made lowercase.
    trainingprogramid = models.IntegerField(db_column='TrainingProgramID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TrainingProgram'


class User(models.Model):
    firstname = models.CharField(db_column='firstName', max_length=130)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=130)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=130)  # Field name made lowercase.
    email = models.CharField(max_length=130)
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=130, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=130, blank=True, null=True)  # Field name made lowercase.
    adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail')  # Field name made lowercase.
    password = models.CharField(max_length=130)

    class Meta:
        managed = False
        db_table = 'User'


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
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

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
    worksonid = models.IntegerField(db_column='worksOnID', primary_key=True)  # Field name made lowercase.
    employeeid = models.ForeignKey(FacultyAndStaff, models.DO_NOTHING, db_column='EmployeeID')  # Field name made lowercase.
    programid = models.ForeignKey(Program, models.DO_NOTHING, db_column='programID')  # Field name made lowercase.
    employeepercentage = models.FloatField(db_column='employeePercentage')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'worksOn'
