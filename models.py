# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    email = models.CharField(primary_key=True, max_length=-1)
    password = models.CharField(max_length=-1)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True)
    first_name = models.CharField(max_length=-1, blank=True, null=True)
    last_name = models.CharField(max_length=-1, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(blank=True, null=True)
    username = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Admin'


class Collage(models.Model):
    collageid = models.IntegerField(db_column='CollageID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=-1)  # Field name made lowercase.
    nostudents = models.IntegerField(db_column='NoStudents', blank=True, null=True)  # Field name made lowercase.
    nofaculty = models.IntegerField(db_column='NoFaculty', blank=True, null=True)  # Field name made lowercase.
    nostaff = models.IntegerField(db_column='NoStaff', blank=True, null=True)  # Field name made lowercase.
    nofemalestudents = models.IntegerField(db_column='NoFemaleStudents', blank=True, null=True)  # Field name made lowercase.
    nomalestudents = models.IntegerField(db_column='NoMaleStudents', blank=True, null=True)  # Field name made lowercase.
    adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail')  # Field name made lowercase.
    departments = models.TextField(db_column='Departments')  # Field name made lowercase. This field type is a guess.
    buemail = models.CharField(db_column='BUemail', max_length=-1)  # Field name made lowercase.
    userid = models.ForeignKey('FacultyStaff', models.DO_NOTHING, db_column='userid', blank=True, null=True)
    buphonenumber = models.CharField(db_column='BUphoneNumber', max_length=-1)  # Field name made lowercase.
    password = models.CharField(max_length=-1, blank=True, null=True)
    domain = models.TextField(blank=True, null=True)  # This field type is a guess.
    nobuilding = models.IntegerField(db_column='Nobuilding', blank=True, null=True) 
    nofloor = models.CharField(max_length=-1, blank=True, null=True)
    nodisk = models.IntegerField(db_column='Nodisk', blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'Collage'


class FacultyStaff(models.Model):
    password = models.CharField(max_length=-1)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=-1)
    last_name = models.CharField(max_length=-1)
    email = models.CharField(max_length=-1)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField(blank=True, null=True)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=-1)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=-1)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=-1)  # Field name made lowercase.
    adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail')  # Field name made lowercase.
    is_staff = models.BooleanField()
    employeeid = models.CharField(db_column='EmployeeID', max_length=-1)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=-1)  # Field name made lowercase.
    major = models.CharField(db_column='Major', max_length=-1)  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    workstatus = models.CharField(db_column='WorkStatus', max_length=-1)  # Field name made lowercase.
    assignedorganization = models.CharField(db_column='assignedOrganization', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    iban = models.CharField(db_column='Iban', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    officeno = models.CharField(db_column='OfficeNo', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    researchinterest = models.TextField(db_column='ResearchInterest', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    previouswork = models.TextField(db_column='PreviousWork', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    cv = models.BinaryField(db_column='CV', blank=True, null=True)  # Field name made lowercase.
    collageid = models.ForeignKey(Collage, models.DO_NOTHING, db_column='CollageID')  # Field name made lowercase.
    is_buhead = models.BooleanField(db_column='is_BUhead')  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=-1)  # Field name made lowercase.
    username = models.CharField(max_length=-1)
    rank = models.CharField(max_length=-1, blank=True, null=True)
    first_nameeng = models.CharField(db_column='first_nameEng', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    last_nameeng = models.CharField(db_column='last_nameEng', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    bu_assistant = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Faculty_Staff'


class Files(models.Model):
    file_id = models.IntegerField(primary_key=True)
    task = models.ForeignKey('Task', models.DO_NOTHING, db_column='task_ID', blank=True, null=True)  # Field name made lowercase.
    training_program = models.ForeignKey('Trainingprogram', models.DO_NOTHING, db_column='training_program', blank=True, null=True)
    attachment = models.BinaryField(db_column='Attachment', blank=True, null=True)  # Field name made lowercase.
    attachment_name = models.CharField(db_column='Attachment_name', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    project = models.ForeignKey('Project', models.DO_NOTHING, db_column='project', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Files'


class Kaibuemployee(models.Model):
    password = models.CharField(max_length=-1)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=-1)
    last_name = models.CharField(max_length=-1)
    email = models.CharField(max_length=-1)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    phonenumber = models.CharField(db_column='phoneNumber', max_length=-1)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=-1)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=-1)  # Field name made lowercase.
    adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail')  # Field name made lowercase.
    kaiemployeeid = models.CharField(db_column='KAIEmployeeID', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=-1)  # Field name made lowercase.
    is_staff = models.BooleanField()
    username = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'KAIBUEmployee'


class Project(models.Model):
    name = models.CharField(db_column='Name', max_length=150)  # Field name made lowercase.
    totalcost = models.FloatField(db_column='TotalCost', blank=True, null=True)  # Field name made lowercase.
    taxpercentage = models.FloatField(db_column='TaxPercentage', blank=True, null=True)  # Field name made lowercase.
    kaipercentage = models.FloatField(db_column='KAIPercentage', blank=True, null=True)  # Field name made lowercase.
    acceptancestatus = models.CharField(db_column='acceptanceStatus', max_length=130, blank=True, null=True)  # Field name made lowercase.
    programtype = models.CharField(db_column='programType', max_length=130)  # Field name made lowercase.
    collage = models.ForeignKey(Collage, models.DO_NOTHING, db_column='Collage')  # Field name made lowercase.
    leaderid = models.IntegerField(db_column='LeaderID', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='endDate')  # Field name made lowercase.
    adminemail = models.CharField(db_column='AdminEmail', max_length=200, blank=True, null=True)  # Field name made lowercase.
    programstatus = models.CharField(db_column='programStatus', max_length=150)  # Field name made lowercase.
    companyname = models.CharField(db_column='companyName', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    offeringdate = models.DateField(db_column='offeringDate', blank=True, null=True)  # Field name made lowercase.
    acceptancedeadline = models.DateField(db_column='AcceptanceDeadline', blank=True, null=True)  # Field name made lowercase.
    questiondeadline = models.DateField(db_column='QuestionDeadline', blank=True, null=True)  # Field name made lowercase.
    etimaddeadline = models.DateField(db_column='EtimadDeadline', blank=True, null=True)  # Field name made lowercase.
    proposalsubmissiondeadline = models.DateField(db_column='ProposalSubmissionDeadline', blank=True, null=True)  # Field name made lowercase.
    contractduration = models.CharField(db_column='contractDuration', max_length=130, blank=True, null=True)  # Field name made lowercase.
    envelopeopening = models.DateField(db_column='EnvelopeOpening', blank=True, null=True)  # Field name made lowercase.
    rejectionreason = models.CharField(db_column='RejectionReason', max_length=250, blank=True, null=True)  # Field name made lowercase.
    technicalproposalstatus = models.CharField(db_column='TechnicalProposalStatus', max_length=130, blank=True, null=True)  # Field name made lowercase.
    financialproposalstatus = models.CharField(db_column='FinancialProposalStatus', max_length=130, blank=True, null=True)  # Field name made lowercase.
    programid = models.IntegerField(db_column='programID', primary_key=True)  # Field name made lowercase.
    isteamfound = models.BooleanField(db_column='isTeamFound', blank=True, null=True)  # Field name made lowercase.
    isaccepted = models.BooleanField(db_column='isAccepted', blank=True, null=True)  # Field name made lowercase.
    teamid = models.TextField(db_column='teamID')  # Field name made lowercase. This field type is a guess.
    num_ofteam = models.IntegerField(db_column='num_ofTeam', blank=True, null=True)  # Field name made lowercase.
    appourtunityopentoall = models.BooleanField(blank=True, null=True)
    descrription = models.CharField(max_length=200, blank=True, null=True)
    durationtype = models.CharField(db_column='durationType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    chatgroup_id = models.CharField(max_length=200, blank=True, null=True)
    chat_access_key = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Project'


class ProjectStatus(models.Model):
    indicator = models.CharField(max_length=1, blank=True, null=True)
    status = models.CharField(max_length=-1, blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, db_column='project', blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Project_status'


class Register(models.Model):
    registerid = models.IntegerField(db_column='RegisterID', primary_key=True)  # Field name made lowercase.
    programid = models.ForeignKey('Trainingprogram', models.DO_NOTHING, db_column='ProgramID')  # Field name made lowercase.
    id = models.ForeignKey('Trainees', models.DO_NOTHING, db_column='id')
    certifications = models.CharField(max_length=-1, blank=True, null=True)
    certifications_ext = models.CharField(max_length=-1, blank=True, null=True)
    hasregistered = models.BooleanField(db_column='hasRegistered')  # Field name made lowercase.
    haspaid = models.BooleanField()
    hasattended = models.BooleanField(db_column='hasAttended')  # Field name made lowercase.
    refundrequsted = models.BooleanField(db_column='refundRequsted', blank=True, null=True)  # Field name made lowercase.
    preanswers = models.TextField(db_column='preAnswers', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    postanswers = models.TextField(db_column='postAnswers', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Register'


class Trainees(models.Model):
    password = models.CharField(max_length=-1)
    first_name = models.CharField(max_length=-1)
    last_name = models.CharField(max_length=-1)
    email = models.CharField(max_length=-1)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=-1)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=-1)  # Field name made lowercase.
    adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail')  # Field name made lowercase.
    nationalid = models.CharField(db_column='NationalID', max_length=-1)  # Field name made lowercase.
    fullnamearabic = models.CharField(db_column='fullNameArabic', max_length=-1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Trainees'


class Trainingprogram(models.Model):
    descriptionofrequirements = models.CharField(db_column='Descriptionofrequirements', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    totalcost = models.FloatField(db_column='TotalCost', blank=True, null=True)  # Field name made lowercase.
    taxpercentage = models.FloatField(db_column='TaxPercentage', blank=True, null=True)  # Field name made lowercase.
    kaipercentage = models.FloatField(db_column='KAIPercentage', blank=True, null=True)  # Field name made lowercase.
    programtype = models.CharField(db_column='programType', max_length=-1)  # Field name made lowercase.
    startdate = models.DateField(db_column='startDate')  # Field name made lowercase.
    enddate = models.DateField(db_column='endDate')  # Field name made lowercase.
    starttime = models.TimeField(db_column='startTime')  # Field name made lowercase.
    endtime = models.TimeField(db_column='endTime')  # Field name made lowercase.
    capacity = models.IntegerField()
    attendeescount = models.IntegerField(db_column='AttendeesCount', blank=True, null=True)  # Field name made lowercase.
    programid = models.IntegerField(db_column='programID', primary_key=True)  # Field name made lowercase.
    collageid = models.IntegerField(db_column='CollageID')  # Field name made lowercase.
    topic = models.CharField(db_column='Topic', max_length=-1)  # Field name made lowercase.
    dataoffacultyproposal = models.DateField(db_column='dataOfFacultyProposal', blank=True, null=True)  # Field name made lowercase.
    isfacultyfound = models.BooleanField(blank=True, null=True)
    iskaiaccepted = models.BooleanField(blank=True, null=True)
    isreleased_field = models.BooleanField(db_column='isreleased ', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    attachment = models.BinaryField(db_column='Attachment', blank=True, null=True)  # Field name made lowercase.
    program_domain = models.CharField(db_column='Program_domain', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    isbuaccepted = models.BooleanField(blank=True, null=True)
    status = models.CharField(max_length=-1, blank=True, null=True)
    initiatedby = models.CharField(max_length=-1, blank=True, null=True)
    instructorid = models.TextField(db_column='InstructorID')  # Field name made lowercase. This field type is a guess.
    cost = models.FloatField()
    costtype = models.CharField(db_column='costType', max_length=-1)  # Field name made lowercase.
    attachment_name = models.CharField(db_column='Attachment_name', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    num_ofinstructors = models.IntegerField(db_column='num_ofInstructors', blank=True, null=True)  # Field name made lowercase.
    rejectionresons = models.CharField(max_length=-1, blank=True, null=True)
    programleader = models.IntegerField(blank=True, null=True)
    lastenrollmentdate = models.DateField(blank=True, null=True)
    programdescription = models.CharField(db_column='programDescription', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    appourtunityopentoall = models.BooleanField(blank=True, null=True)
    dataofkairejection = models.DateField(db_column='dataOfKaiRejection', blank=True, null=True)  # Field name made lowercase.
    dataofburejection = models.DateField(db_column='dataOfBuRejection', blank=True, null=True)  # Field name made lowercase.
    programdescription_english = models.CharField(db_column='programDescription_english', max_length=-1, blank=True, null=True)  # Field name made lowercase.
    isonline = models.BooleanField(db_column='isOnline', blank=True, null=True)  # Field name made lowercase.
    location_field = models.CharField(db_column='location ', max_length=-1, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    topic_english = models.CharField(max_length=-1, blank=True, null=True)
    adminemail = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminEmail', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TrainingProgram'


class TrainingprogramStatus(models.Model):
    indicator = models.CharField(max_length=1, blank=True, null=True)
    status = models.CharField(max_length=-1, blank=True, null=True)
    training_program = models.ForeignKey(Trainingprogram, models.DO_NOTHING, db_column='training_program', blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Trainingprogram _status'


class Workson(models.Model):
    instructorid = models.ForeignKey(FacultyStaff, models.DO_NOTHING, db_column='instructorid', blank=True, null=True)
    status = models.CharField(max_length=-1, blank=True, null=True)
    training_program = models.ForeignKey(Trainingprogram, models.DO_NOTHING, db_column='training_program', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    rejectionresons = models.CharField(max_length=-1, blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, db_column='project', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'WorksOn'


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


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.TextField(blank=True, null=True)
    task_type = models.TextField(blank=True, null=True)
    task_description = models.TextField(blank=True, null=True)
    is_classified = models.BooleanField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    necessary_procedure = models.TextField(blank=True, null=True)
    priority = models.TextField(blank=True, null=True)
    faculty_initation = models.ForeignKey(FacultyStaff, models.DO_NOTHING, db_column='faculty_initation', blank=True, null=True)
    kai_initiation = models.ForeignKey(Kaibuemployee, models.DO_NOTHING, db_column='kai_initiation', blank=True, null=True)
    faculty_ids = models.TextField(blank=True, null=True)  # This field type is a guess.
    kai_ids = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.TextField(blank=True, null=True)
    main_task = models.ForeignKey('self', models.DO_NOTHING, db_column='main_task', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task'


class TaskToUser(models.Model):
    status = models.TextField(blank=True, null=True)
    kai_user = models.ForeignKey(Kaibuemployee, models.DO_NOTHING, db_column='kai_user', blank=True, null=True)
    faculty_user = models.ForeignKey(FacultyStaff, models.DO_NOTHING, db_column='faculty_user', blank=True, null=True)
    main_task = models.ForeignKey(Task, models.DO_NOTHING, db_column='main_task', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task_to_user'
