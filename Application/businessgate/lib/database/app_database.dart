

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
  String nationValue = '' ;

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
  String newTrainees = '';
  Future<String> registerTrainees(
      String fName, String lName, String phoneNumber ,String email, String gender, String nationality,
      String password, String id) async {
    try {
      await connection!.open();
      await connection!.transaction((newTraineesConnection) async {
        //Stage 1 : Make sure email or mobile not registered.
        alreadyRegistered = await newTraineesConnection.query(
          'select * from public."Trainees" where email = @emailValue',
          substitutionValues: {
            'emailValue': email, 
            },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (alreadyRegistered!.affectedRowCount > 0) {
          // alr means already registered
          newTrainees = 'alr';
        } else {
          //Stage 2 : If user not already registered then we start the registration
          newRegisterResult = await newTraineesConnection.query(
            'INSERT INTO public."Trainees"("password","firstName","lastName","email", "certifications","phoneNumber","Gender", "Nationality","AdminEmail","NationalID") '
            'VALUES (@passwordValue,@fNameValue,@lNameValue,@emailValue,Null, @phoneNumberValue,@genderValue, @nationValue, @adminEmailValue, @idValue )',
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
              'nationValue' : 'nation',
              // do i keep it ?
              'registrationValue': DateTime.now(),
            },
            allowReuse: true,
            timeoutInSeconds: 30,
          );
          newTrainees =
          // reg means registration is succesfull , nop means registration failed
              (newRegisterResult!.affectedRowCount > 0 ? 'reg' : 'nop');
        }
      });
    } catch (exc) {
      // exc means an exception happened
      newTrainees = 'exc';
      exc.toString();
    }
    return newTrainees;
  }


  //Login Database Section
  String userLoginFuture = '';
  Future<String> loginUser(String email, String password) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'SELECT * FROM public."Trainees" WHERE "email" = @emailValue AND "password" = @passwordValue',
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

String updatePassword = '';
  UpdatePassword (String email, String password) async{
     try {
      await connection!.open();
      await connection!.transaction((UpdateConnection) async {
        //Check email registered or no
        loginResult = await UpdateConnection.query(
          'UPDATE public."Trainees" SET "password" = @passwordValue WHERE "email" = @emailValue',
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
    return updatePassword;

  }

  String FName = '' ;
  Future<String> FetchFName(String email) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'SELECT "firstName" FROM public."Trainees" WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (loginResult != null && loginResult!.isNotEmpty) {
        // Assuming the query returns a single row, you can get the first name like this
        FName = loginResult![0][0].toString();
      }
      });
    } catch (exc) {
      exc.toString();
    }
    return FName;
  }

String updatefname = '';
  Future<String> UpdateFName(String email, String NameF) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'UPDATE public."Trainees" SET "firstName" = @fNameValue WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
        'fNameValue': NameF
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (loginResult!.affectedRowCount > 0) {
          //emailAddress = loginResult!.first
              //.elementAt(0); //This to use when update seller details
              updatefname = 'ok';
        } else {
          updatefname = 'not';
        }
      });
    } catch (exc) {
      exc.toString();
    }
    return updatefname ;
  }

  String LName = '' ;
  Future<String> FetchLName(String email) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'SELECT "lastName" FROM public."Trainees" WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (loginResult!.isNotEmpty) {
        // Assuming the query returns a single row, you can get the first name like this
        LName = loginResult![0][0].toString();
      }
      });
    } catch (exc) {
      userLoginFuture = 'exc';
      exc.toString();
    }
    return LName;
  }

 String updatelname = '';
  Future<String> UpdateLName(String email, String NameL) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'UPDATE public."Trainees" SET "lastName" = @lNameValue WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
        'lNameValue': NameL
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
      if (loginResult!.affectedRowCount > 0) {
          //emailAddress = loginResult!.first
              //.elementAt(0); //This to use when update seller details
              updatelname = 'ok';
        } else {
          updatelname = 'not';
        }
      });
    } catch (exc) {
      exc.toString();
    }
    return updatelname ;
  }

  String PhoneNum = '' ;
  Future<String> FetchPHone(String email) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'SELECT "phoneNumber" FROM public."Trainees" WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (loginResult!.isNotEmpty) {
        // Assuming the query returns a single row, you can get the first name like this
        PhoneNum = loginResult![0][0].toString();
      }
      });
    } catch (exc) {
      userLoginFuture = 'exc';
      exc.toString();
    }
    return PhoneNum;
  }

 String updatephonenum = '';
  Future<String> UpdatePhone(String email, String phone) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'UPDATE public."Trainees" SET "phoneNumber" = @phoneNumberValue WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
        'phoneNumberValue': phone
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
       if (loginResult!.affectedRowCount > 0) {
          //emailAddress = loginResult!.first
              //.elementAt(0); //This to use when update seller details
              updatephonenum = 'ok';
        } else {
          updatephonenum = 'not';
        }
      });
    } catch (exc) {
      exc.toString();
    }
    return updatephonenum;
  }

  String Pass = '' ;
  Future<String> FetchPass(String email) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'SELECT "password" FROM public."Trainees" WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        if (loginResult!.isNotEmpty) {
        // the query returns a single row, you can get the first name like this
        Pass = loginResult![0][0].toString();
      }
      });
    } catch (exc) {
      userLoginFuture = 'exc';
      exc.toString();
    }
    return Pass;
  }

 String updateppass= '';
  Future<String> UpdatePass(String email, String pass) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'UPDATE public."Trainees" SET "password" = @passwordValue WHERE "email" = @emailValue',
      substitutionValues: {
        'emailValue': email,
        'passwordValue': pass
      },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
       if (loginResult!.affectedRowCount > 0) {
          //emailAddress = loginResult!.first
              //.elementAt(0); //This to use when update seller details
              updateppass = 'ok';
        } else {
          updateppass = 'not';
        }
      });
    } catch (exc) {
      exc.toString();
    }
    return updatephonenum;
  }
  
}
