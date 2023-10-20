//import 'package:flutter_db/database/app_database.dart';

import '../database/app_database.dart';

class ModelsUsers {
  // Register Model Section
  String Trainee = '';
  Future<String> registerTrainee(
      String fName, String lName, String phoneNumber, String email,String password, String id, 
      String gender, String nationality ) async {
    Trainee = await AppDatabase().registerTrainees(fName, lName, phoneNumber, email, gender, nationality, password, id);
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

  String PhoneNumber= '';
  Future<String> FetchPhoneNum(String email) async {
    PhoneNumber = await AppDatabase().FetchPHone(email);
    return PhoneNumber;
  }

  String UpdatePN = '';
  Future<String> updatephonenum(String email, String PhoneNum) async {
    UpdatePN = await AppDatabase().UpdatePhone(email, PhoneNum);
    return UpdatePN;
  }

  String Password= '';
  Future<String> FetchPassword(String email) async {
    Password = await AppDatabase().FetchPass(email);
    return Password;
  }

  String UpdatePass = '';
  Future<String> updatepass(String email, String pass) async {
    UpdatePass = await AppDatabase().UpdatePass(email, pass);
    return UpdatePass;
  }
}
