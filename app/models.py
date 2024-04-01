
from django.db import models
from django.contrib.auth.models import AbstractUser , Group, Permission , UserManager
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import ArrayField

class Admin(AbstractUser):
    email = models.CharField(primary_key=True, max_length=130)
    password = models.CharField(max_length=130)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True)
    first_name = models.CharField(max_length=130, blank=True, null=True)
    last_name = models.CharField(max_length=130, blank=True, null=True)
    is_active = models.BooleanField( blank=True, null=True)
    date_joined = models.DateTimeField(max_length=130, blank=True, null=True)
    is_staff = models.BooleanField(blank=True, null=True)
    username = models.CharField(max_length=130, blank=True, null=True) 
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='admin_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='admin_permissions'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

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
    buemail = models.CharField(db_column='BUemail', max_length=130)  # Field name made lowercase.
    userid = models.ForeignKey('FacultyStaff', models.DO_NOTHING, db_column='userid')
    buphonenumber = models.CharField(db_column='BUphoneNumber', max_length=130)  # Field name made lowercase.
    password = models.CharField( max_length=130)
    domain = ArrayField(models.TextField(blank=True, null=True) ,db_column='domain',default=list )
    nobuilding = models.IntegerField(db_column='Nobuilding', blank=True, null=True) 
    nofloor = models.CharField( blank=True, null=True , max_length=130)
    nodisk = models.IntegerField(db_column='Nodisk', blank=True, null=True) 
    last_update = models.DateTimeField(blank=True, null=True)
    new_user = models.BooleanField(blank=True, null=True)

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
    adminemail = models.CharField(db_column='AdminEmail', blank=True, null=True, max_length=130)  
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
    department_field = models.CharField(db_column='Department', max_length=130)
    rank = models.CharField(blank=True, null=True, max_length=130)
    first_nameeng = models.CharField(db_column='first_nameEng', blank=True, null=True, max_length=130)  # Field name made lowercase.
    last_nameeng = models.CharField(db_column='last_nameEng', blank=True, null=True, max_length=130) 
    bu_assistant = models.BooleanField(blank=True, null=True)
    new_user = models.BooleanField(blank=True, null=True)
    sendnotificationbyemail = models.BooleanField(default=False, db_column='sendnotificationbyemail')

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='Faculty_Staff_groups'  
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='faculty_staff_permissions'  
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
    adminemail = models.CharField(db_column='AdminEmail', blank=True, null=True, max_length=130)  
    kaiemployeeid = models.CharField(db_column='KAIEmployeeID', max_length=130) 
    position = models.CharField(db_column='Position', max_length=130) 
    is_staff = models.BooleanField(blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    new_user = models.BooleanField(blank=True, null=True)
    id_departmenthead = models.BooleanField(default=False, null=False , db_column= 'iid_departmenthead')
    sendnotificationbyemail = models.BooleanField(default=False, db_column='sendnotificationbyemail')
    

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
    certifications_ext = models.CharField(blank=True, null=True , db_column='certifications_ext', max_length=130)
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
    adminemail = models.CharField(db_column='AdminEmail', blank=True, null=True, max_length=130)
    nationalid = models.CharField(db_column='NationalID', blank=True, null=True, max_length=130)
    fullnamearabic = models.CharField(db_column='fullNameArabic', blank=True, null=True, max_length=130)

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
    initiatedby = models.CharField(db_column='initiatedby',choices=INITIATED_BY_CHOICES,blank=True,null=True, max_length=130)
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
  
    class Meta:
        managed = False
        db_table = 'TrainingProgram'


class IdStatusDate(models.Model):
    instructor = models.ForeignKey('FacultyStaff', on_delete=models.CASCADE, db_column='instructorid', null=True)
    status = models.CharField(max_length=130, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    training_program = models.ForeignKey('TrainingProgram', on_delete=models.CASCADE, db_column='training_program')
    rejectionresons = models.CharField(max_length=500, blank=True, null=True)
    project =models.ForeignKey('Project', on_delete=models.CASCADE, db_column='project')

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


class Files(models.Model) :
    fileid = models.AutoField(db_column='file_id', primary_key=True)
    taskid = models.ForeignKey('Task', on_delete=models.CASCADE, db_column='task_ID')
    training_program = models.ForeignKey('TrainingProgram', on_delete=models.CASCADE, db_column='training_program')
    attachment = models.BinaryField(db_column='Attachment', blank=True, null=True)
    attachment_name = models.CharField(db_column='Attachment_name', max_length=130, blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, db_column='project')

    class Meta:
        managed = False
        db_table = 'Files'


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.TextField()
    task_type = models.TextField()
    task_description = models.TextField(max_length=1000)
    is_classified = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(max_length=1000)
    necessary_procedure = models.TextField()
    priority = models.TextField()
    faculty_initiation = models.ForeignKey('FacultyStaff', on_delete=models.CASCADE)
    kai_initiation = models.ForeignKey('Kaibuemployee', on_delete=models.CASCADE, related_name='kaibuemployee_initiated_tasks', null=True, blank=True)
    faculty_ids = ArrayField(models.IntegerField(), default=list, blank=True, null=True)  # Assuming PostgreSQL is being used
    kai_ids = ArrayField(models.IntegerField(), default=list, blank=True, null=True)  # Also assuming PostgreSQL is being used
    status = models.TextField()
    main_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_tasks')
    statusarray = ArrayField(models.TextField(), blank=True, default=list)
    datearray = ArrayField(models.DateField(), blank=True, default=list)
    is_main_task = models.BooleanField(default=False)
    attachment = models.BinaryField(db_column='attacment', blank=True, null=True)
    countrejection = models.IntegerField(default=0)
    toall = models.BooleanField(default=False)
    full_accomplishment = models.CharField(db_column='fullaccomplishment', max_length=255)
    retrivaldate = models.DateField()
    pending_status=models.TextField()
    pending_reasons = ArrayField(models.TextField(blank=True, default=list), default=list, null=True)
    pending_rquestids = ArrayField(models.TextField(blank=True, default=list), default=list, null=True)
    

    def __str__(self):
        return self.task_name

    class Meta:
        managed = False
        db_table = 'task'


class TaskToUser(models.Model):
    status = models.TextField()
    kai_user = models.ForeignKey('Kaibuemployee', on_delete=models.CASCADE, db_column='kai_user')
    faculty_user = models.ForeignKey('FacultyStaff', on_delete=models.CASCADE, db_column='faculty_user')
    main_task = models.ForeignKey('Task', on_delete=models.CASCADE, db_column='main_task') 
    attachment = models.BinaryField(db_column='attachment', blank=True, null=True) # Optional field for binary data
    addedtext = models.TextField(blank=True)  # Optional field for large text data
    addeddate = models.DateField(auto_now_add=False, blank=True, null=True)  # Optional field for date
    date_time = models.DateTimeField(blank=True, null=True)
   
    class Meta:
        managed = False
        db_table = 'task_to_user'

from django.db import models

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    faculty_target = models.ForeignKey('FacultyStaff', on_delete=models.CASCADE, db_column='faculty_target_id', null=True)
    kaitarget = models.ForeignKey('Kaibuemployee', on_delete=models.CASCADE, db_column='kai_target_id')
    training_program = models.ForeignKey('Trainingprogram', on_delete=models.CASCADE, db_column='training_program_id')
    taskid = models.ForeignKey('Task', on_delete=models.CASCADE, db_column='task_id')
    notification_message = models.TextField(db_column='notificationmessage')
    TimeOfCreation = models.DateTimeField(auto_now_add=True, db_column='timeofcreation')
    isread = models.BooleanField(default=False, db_column='isread')
    isopened = models.BooleanField(default=False, db_column='isopened')
    need_to_be_opened = models.BooleanField(default=False, db_column='needtobeOpened')
    function_indicator = models.IntegerField(null=True, blank=True)
    faculty_staff_ids = ArrayField(models.IntegerField(), blank=True, null=True)
    kai_ids = ArrayField(models.IntegerField(), blank=True, null=True)
    target_indicator = models.IntegerField(null=True, blank=True)
    need_to_be_shown = models.BooleanField(default=False, db_column='needtobeshown')
    class Meta:
        db_table = 'notification'


class Project(models.Model):
    Name = models.CharField(db_column='Name', max_length=130)
    totalcost = models.FloatField(db_column='TotalCost', blank=True, null=True)  
    taxpercentage = models.FloatField(db_column='TaxPercentage', blank=True, null=True)  
    kaipercentage = models.FloatField(db_column='KAIPercentage', blank=True, null=True) 
    acceptanceStatus = models.CharField(db_column='acceptanceStatus',  max_length=130) 
    programtype = models.CharField(db_column='programType', max_length=130) 
    collageid = models.IntegerField(db_column='Collage')
    programleader = models.IntegerField(db_column='LeaderID',blank=True, null=True)  
    startdate = models.DateField(db_column='startDate')  
    enddate = models.DateField(db_column='TeamEndDate') 
    status = models.CharField(db_column='programStatus', max_length=130, blank=True, null=True)
    CompanyName = models.CharField(db_column='companyName',  max_length=130)
    OfferingDate = models.DateField(db_column='offeringDate')
    AcceptanceDeadline = models.DateField(db_column='AcceptanceDeadline')
    QuestionDeadline = models.DateField(db_column='QuestionDeadline') 
    EtimadDeadline = models.DateField(db_column='EtimadDeadline')  
    ProposalSubmissionDeadline = models.DateField(db_column='ProposalSubmissionDeadline') 
    contractDuration = models.IntegerField(db_column='contractDuration')
    EnvelopeOpening =  models.DateField(db_column='EnvelopeOpening')
    rejectionresons = models.CharField(db_column='RejectionReason',max_length=500, blank=True, null=True)
    TechnicalProposalStatus = models.CharField(db_column='TechnicalProposalStatus', max_length=130, blank=True, null=True)
    FinancialProposalStatus = models.CharField(db_column='FinancialProposalStatus', max_length=130, blank=True, null=True)
    programid = models.AutoField(db_column='programID', primary_key=True) 
    isteamfound = models.BooleanField(db_column='isTeamFound',blank=True, null=True)
    isSubmittedtoKAI = models.BooleanField(db_column='isSubmittedtoKAI',blank=True, null=True) 
    isAccepted = models.BooleanField(db_column='isAccepted',blank=True, null=True) 
    Teamid = ArrayField(models.IntegerField(), default=list, blank=True, null=True , db_column='teamID')
    num_ofTeam = models.IntegerField(db_column='num_ofTeam', blank=True, null=True)
    appourtunityopentoall = models.BooleanField(blank=True, null=True,db_column='appourtunityopentoall')
    durationType = models.CharField(db_column='durationType', max_length=100)
    description = models.CharField(db_column='descrription', max_length=200)
    chatgroup_id = models.CharField(db_column='chatgroup_id', max_length=200)
    chat_access_key = models.CharField(db_column='chat_access_key', max_length=200)
    
    class Meta:
        managed = False
        db_table = 'Project'


class StatusDateCheckProject(models.Model):
    status = models.CharField(max_length=130, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    indicator = models.CharField(max_length=1, blank=True, null=True)
    project =models.ForeignKey('Project', on_delete=models.CASCADE, db_column='project')

    class Meta:
        managed = False
        db_table = 'Project_status'


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

