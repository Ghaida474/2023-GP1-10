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

  String UpdateFN = 'OK';
  Future<String> updatefname(String email, String fname) async {
    await AppDatabase().UpdateFName(email, fname);
    return UpdateFN;
  }

  String lastName = '';
  Future<String> FetchLastName(String email) async {
    lastName = await AppDatabase().FetchLName(email);
    return lastName;
  }

  String PhoneNumber= '';
  Future<String> FetchPhoneNum(String email) async {
    PhoneNumber = await AppDatabase().FetchPHone(email);
    return PhoneNumber;
  }

  String Password= '';
  Future<String> FetchPassword(String email) async {
    Password = await AppDatabase().FetchPass(email);
    return Password;
  }
}
