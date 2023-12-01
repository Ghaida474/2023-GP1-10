import '../database/app_database.dart';
import '../database/app_database.dart';
import 'dart:typed_data';

class ModelsUsers {
  String Trainee = '';
  Future<String> registerTrainee(
      String fName,
      String lName,
      String phoneNumber,
      String email,
      String password,
      String id,
      String gender,
      String nationality) async {
    Trainee = await AppDatabase().registerTrainees(
        fName, lName, phoneNumber, email, gender, nationality, password, id);
    return Trainee;
  }

  /// Login Model Section
  String login = '';
  Future<String> userLoginModel(String email, String password) async {
    login = await AppDatabase().loginUser(email, password);
    return login;
  }

  String Update = '';
  Future<String> updatePassword(String email, String password) async {
    Update = await AppDatabase().UpdatePassword(email, password);
    return Update;
  }

  String firstName = '';
  Future<String> FetchFirstName(String email) async {
    firstName = await AppDatabase().FetchFName(email);
    return firstName;
  }

  String UpdateFN = '';
  Future<String> updatefname(String email, String fname) async {
    UpdateFN = await AppDatabase().UpdateFName(email, fname);
    return UpdateFN;
  }

  String lastName = '';
  Future<String> FetchLastName(String email) async {
    lastName = await AppDatabase().FetchLName(email);
    return lastName;
  }

  String UpdateLN = '';
  Future<String> updatelname(String email, String lname) async {
    UpdateLN = await AppDatabase().UpdateLName(email, lname);
    return UpdateLN;
  }

  String PhoneNumber = '';
  Future<String> FetchPhoneNum(String email) async {
    PhoneNumber = await AppDatabase().FetchPHone(email);
    return PhoneNumber;
  }

  String UpdatePN = '';
  Future<String> updatephonenum(String email, String PhoneNum) async {
    UpdatePN = await AppDatabase().UpdatePhone(email, PhoneNum);
    return UpdatePN;
  }

  String Password = '';
  Future<String> FetchPassword(String email) async {
    Password = await AppDatabase().FetchPass(email);
    return Password;
  }

  String UpdatePass = '';
  Future<String> updatepass(String email, String pass) async {
    UpdatePass = await AppDatabase().UpdatePass(email, pass);
    return UpdatePass;
  }

  /*int courseCount = 0;
  Future<int> CourseCount() async {
    courseCount = await AppDatabase().TrainingProgramCount();
    return courseCount;
  }*/

  List<Courses> courses = [];
  Future<List<Courses>> TrainingPrograms() async {
    courses = await AppDatabase().getAcceptedTrainingPrograms();
    return courses;
  }

  Courses thecourse = Courses("", 0.0, 0,"","","","","","");
  Future<Courses> TrainingProgram(int? id) async {
    thecourse = await AppDatabase().Program(id);
    return thecourse;
  }

  List<Courses> filteredcourses = [];
  Future<List<Courses>> filterPrograms(String? name) async {
    filteredcourses = await AppDatabase().filteredPrograms(name);
    return filteredcourses;
  }

  String banswers = '';
  Future<String> Register(String q1, String q2, String q3, String q4, String q5,String email,int? id) async {
    banswers = await AppDatabase().RegisterToProgram(q1, q2, q3, q4, q5,email,id);
    return banswers;
  }

  String afanswers = '';
  Future<String> answerModelA(String q1, String q2, String q3, String q4, String q5,String email,int? id) async {
    afanswers = await AppDatabase().enterAFAnswers(q1, q2, q3, q4, q5,email,id);
    return afanswers;
  }

  bool cancel=false;
   Future<bool> cancelCourseM(int? id) async {
    cancel = await AppDatabase().cancelCourse(id);
    return cancel;
  }

  List<Courses>Rcourses = [];
  Future<List<Courses>> getRegisteredCoursesM(int? id) async {
    Rcourses = await AppDatabase().getRegisteredCourses(id);
    return Rcourses;
  }

 List<Courses>Runcourses = [];
  Future<List<Courses>> getRunningCoursesM(int? id) async {
    Rcourses = await AppDatabase(). getRunningCourses(id);
    return Rcourses;
  }

List<Courses>Comcourses = [];
  Future<List<Courses>> getCompletedCoursesM(int? id) async {
    Rcourses = await AppDatabase(). getCompletedCourses(id);
    return Rcourses;
  }
  Future<List<CertificateData>>fetchCertificationsM(int id) async {
    return await AppDatabase().fetchCertifications(id);
  }

  String status = '';
  Future<String> fetchStat(int? pid, String temail) async {
    status = await AppDatabase().fetchStatus(pid,temail);
    return status;
  }
}
