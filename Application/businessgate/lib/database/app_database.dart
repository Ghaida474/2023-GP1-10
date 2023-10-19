

import 'dart:ffi';

import 'package:postgres/postgres.dart';

class AppDatabase {

  String emailValue = '';
  String passwordValue = '';
  String phoneNumberValue = '';
  String fNameValue = '';
  String lNameValue = '';
  String nationalityValue = '' ;
  String idValue = '' ;
  String genderValue = '' ;
  String adminEmailValue = '' ;

  PostgreSQLConnection? connection;
  PostgreSQLResult? newRegisterResult ;
  PostgreSQLResult? alreadyRegistered ;

  PostgreSQLResult? loginResult, userRegisteredResult;

  PostgreSQLResult? updateTraineeResult;

  static String? emailAddress;

  PostgreSQLResult? _fetchSellerDataResult;

  AppDatabase() {
 connection = PostgreSQLConnection(
  'localhost',
  5432,
  'businessgate',
  username: 'admina',
  password: 'data12345',

 );
    //fetchDataFuture = [];
  }

  // Register Database Section
  String newTrainee = '';
  Future<String> registerTrainees(
      String fName, String lName, String phoneNumber ,String email, String gender, String nationality,
      String password, String id) async {
    try {
      await connection!.open();
      await connection!.transaction((newTraineeConnection) async {
        //Stage 1 : Make sure email or mobile not registered.
        alreadyRegistered = await newTraineeConnection.query(
          'select * from public."Trainee" where email = @emailValue',
          substitutionValues: {
            'emailValue': email, 
            },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (alreadyRegistered!.affectedRowCount > 0) {
          // alr means already registered
          newTrainee = 'alr';
        } else {
          //Stage 2 : If user not already registered then we start the registration
          newRegisterResult = await newTraineeConnection.query(
            'INSERT INTO public."Trainee"("firstName","lastName","phoneNumber", "email", "Gender", "Nationality","AdminEmail","password","certifications","NationalID") '
            'VALUES (@fNameValue,@lNameValue,@phoneNumberValue, @emailValue, @genderValue, Null, @adminEmailValue, @passwordValue, Null, @idValue )',
            substitutionValues: {
              'emailValue': email,
              'passwordValue': password,
              'phoneNumberValue': phoneNumber,
              'fNameValue': fName,
              'lNameValue': lName,
              'nationalityValue': "Null",
              'idValue' : id,
              'genderValue': gender,
              'adminEmailValue' : 'businessgate.ksu@gmail.com',
              // do i keep it ?
              'registrationValue': DateTime.now(),
            },
            allowReuse: true,
            timeoutInSeconds: 30,
          );
          newTrainee =
          // reg means registration is succesfull , nop means registration failed
              (newRegisterResult!.affectedRowCount > 0 ? 'reg' : 'nop');
        }
      });
    } catch (exc) {
      // exc means an exception happened
      newTrainee = 'exc';
      exc.toString();
    }
    return newTrainee;
  }


  //Login Database Section
  String userLoginFuture = '';
  Future<String> loginUser(String email, String password) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'SELECT * FROM public."Trainee" WHERE "email" = @emailValue AND "password" = @passwordValue',
      substitutionValues: {
        'emailValue': email,
        'passwordValue': password,
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (loginResult!.affectedRowCount > 0) {
          //emailAddress = loginResult!.first
              //.elementAt(0); //This to use when update seller details
              userLoginFuture = 'ok';
        } else {
          userLoginFuture = 'not';
        }
      });
    } catch (exc) {
      userLoginFuture = 'exc';
      exc.toString();
    }
    return userLoginFuture;
  }

String updatePassword = 'ok';
  UpdatePassword (String email, String password) async{
     try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'UPDATE public."Trainee" SET "password" = @passwordValue WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
        'passwordValue': password,
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (loginResult!.affectedRowCount > 0) {
          //emailAddress = loginResult!.first
              //.elementAt(0); //This to use when update seller details
              updatePassword = 'ok';
        } else {
          updatePassword = 'not';
        }
      });
    } catch (exc) {
      updatePassword = 'exc';
      exc.toString();
    }

  }

  String FName = '' ;
  Future<String> FetchFName(String email) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'SELECT "firstName" FROM public."Trainee" WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (loginResult != null && loginResult!.isNotEmpty) {
        // Assuming the query returns a single row, you can get the first name like this
        FName = loginResult![0][0] as String;
      }
      });
    } catch (exc) {
      exc.toString();
    }
    return FName;
  }

  Future<void> UpdateFName(String email, String NameF) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'UPDATE public."Trainee" SET "firstName" = @fNameValue WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
        'fNameValue': NameF
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
      });
    } catch (exc) {
      exc.toString();
    }
  }

  String LName = '' ;
  Future<String> FetchLName(String email) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'SELECT "lastName" FROM public."Trainee" WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (loginResult!.isNotEmpty) {
        // Assuming the query returns a single row, you can get the first name like this
        LName = loginResult![0][0] as String;
      }
      });
    } catch (exc) {
      userLoginFuture = 'exc';
      exc.toString();
    }
    return FName;
  }

  Future<void> UpdateLName(String email, String NameL) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'UPDATE public."Trainee" SET "lastName" = @lNameValue WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
        'lNameValue': NameL
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
      });
    } catch (exc) {
      exc.toString();
    }
  }

  String PhoneNum = '' ;
  Future<String> FetchPHone(String email) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'SELECT "phoneNumber" FROM public."Trainee" WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (loginResult!.isNotEmpty) {
        // Assuming the query returns a single row, you can get the first name like this
        PhoneNum = loginResult![0][0]as String;
      }
      });
    } catch (exc) {
      userLoginFuture = 'exc';
      exc.toString();
    }
    return PhoneNum;
  }

  Future<void> UpdatePhone(String email, String phone) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'UPDATE public."Trainee" SET "phoneNumber" = @phoneNumberValue WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
        'phoneNumberValue': phone
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
      });
    } catch (exc) {
      exc.toString();
    }
  }

  String Pass = '' ;
  Future<String> FetchPass(String email) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'SELECT "password" FROM public."Trainee" WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (loginResult!.isNotEmpty) {
        // the query returns a single row, you can get the first name like this
        Pass = loginResult![0][0] as String;
      }
      });
    } catch (exc) {
      userLoginFuture = 'exc';
      exc.toString();
    }
    return Pass;
  }

  Future<void> UpdatePass(String email, String pass) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'UPDATE public."Trainee" SET "password" = @passwordValue WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
        'passwordValue': pass
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
      });
    } catch (exc) {
      exc.toString();
    }
  }



  
}
