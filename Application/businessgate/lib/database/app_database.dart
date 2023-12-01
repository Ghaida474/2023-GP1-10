import 'package:postgres/postgres.dart';
import 'dart:ffi';
import 'dart:async';
import 'package:postgres/postgres.dart';
import 'package:intl/intl.dart';
import 'dart:convert';

import 'dart:ffi';
import 'dart:typed_data';
import 'package:intl/intl.dart';
import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:postgres/postgres.dart';
import '../myservice.dart';


import 'package:shared_preferences/shared_preferences.dart';

class AppDatabase {
  String emailValue = '';
  String passwordValue = '';
  String phoneNumberValue = '';
  String fNameValue = '';
  String lNameValue = '';
  String nationalityValue = '';
  String idValue = '';
  String genderValue = '';
  String adminEmailValue = '';
  String nationValue = '';

  SharedPreferences? prefs;
  String? languageValue ;
  final key = "value";

  PostgreSQLConnection? connection;
  PostgreSQLResult? newRegisterResult,loginResult;
  PostgreSQLResult? alreadyRegistered;

  PostgreSQLResult?  userRegisteredResult;

  PostgreSQLResult? updateTraineeResult;
  MyService _myID = MyService();

  //MyService capacity = MyService();
  static String? emailAddress;

  AppDatabase() {
    connection = PostgreSQLConnection(
      'localhost',
      5432,
      'btest',
      username: 'postgres',
      password: 'Lina1234',
    );
  }

  _read() async {
    prefs = await SharedPreferences.getInstance();
      languageValue = prefs!.getString(key) ?? "English";
  }

  // Register Database Section
  String newTrainees = '';
  Future<String> registerTrainees(
      String fName,
      String lName,
      String phoneNumber,
      String email,
      String gender,
      String nationality,
      String password,
      String id) async {
    try {
      await connection!.open();
      await connection!.transaction((newTraineesConnection) async {
        //Stage 1 : Make sure email or mobile not registered.
        alreadyRegistered = await newTraineesConnection.query(
          'select * from public."Trainees" where email = @emailValue ',
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
            'INSERT INTO public."Trainees"("password","firstName","lastName","email","phoneNumber","Gender","AdminEmail","NationalID") '
            'VALUES (@passwordValue,@fNameValue,@lNameValue,@emailValue,@phoneNumberValue,@genderValue, @adminEmailValue, @idValue )RETURNING id',
            substitutionValues: {
              'emailValue': email,
              'passwordValue': password,
              'phoneNumberValue': phoneNumber,
              'fNameValue': fName,
              'lNameValue': lName,
              'idValue': id,
              'genderValue': gender,
              'adminEmailValue': 'businessgate.ksu@gmail.com',
            },
            allowReuse: true,
            timeoutInSeconds: 10,
          );
          if (newRegisterResult!.isNotEmpty) {
       _myID.myVariable2  = newRegisterResult![0][0] as int;
      
            }
          newTrainees =
              // reg means registration is succesfull , nop means registration failed
              (newRegisterResult!.affectedRowCount > 0 ? 'reg' : 'nop');
        }
      });
    } catch (exc) {
      // exc means an exception happened
      newTrainees = 'exc';
      exc.toString();
    } finally {
      await connection!.close();
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
          timeoutInSeconds: 10,
        );
        if (loginResult!.affectedRowCount > 0) {
         _myID.myVariable2 = loginResult![0][0] as int;
      
              userLoginFuture = 'ok';
        }  else {
          userLoginFuture = 'not';
        }
      });
    } catch (exc) {
      userLoginFuture = 'exc';
      exc.toString();
    } finally {
      await connection!.close();
    }
    return userLoginFuture;
  }

  String updatePassword = '';
  UpdatePassword(String email, String password) async {
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
          timeoutInSeconds: 10,
        );
        if (loginResult!.affectedRowCount > 0) {
          updatePassword = 'ok';
        } else {
          updatePassword = 'not';
        }
      });
    } catch (exc) {
      updatePassword = 'exc';
      exc.toString();
    } finally {
      await connection!.close();
    }
    return updatePassword;
  }

  String FName = '';
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
          timeoutInSeconds: 10,
        );
        if (loginResult != null && loginResult!.isNotEmpty) {
          FName = loginResult![0][0].toString();
        }
      });
    } catch (exc) {
      exc.toString();
    } finally {
      await connection!.close();
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
          substitutionValues: {'emailValue': email, 'fNameValue': NameF},
          allowReuse: true,
          timeoutInSeconds: 10,
        );
        if (loginResult!.affectedRowCount > 0) {
          updatefname = 'ok';
        } else {
          updatefname = 'not';
        }
      });
    } catch (exc) {
      exc.toString();
    } finally {
      await connection!.close();
    }
    return updatefname;
  }

  String LName = '';
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
          timeoutInSeconds: 10,
        );
        if (loginResult!.isNotEmpty) {
          LName = loginResult![0][0].toString();
        }
      });
    } catch (exc) {
      userLoginFuture = 'exc';
      exc.toString();
    } finally {
      await connection!.close();
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
          substitutionValues: {'emailValue': email, 'lNameValue': NameL},
          allowReuse: true,
          timeoutInSeconds: 10,
        );
        if (loginResult!.affectedRowCount > 0) {
          updatelname = 'ok';
        } else {
          updatelname = 'not';
        }
      });
    } catch (exc) {
      exc.toString();
    } finally {
      await connection!.close();
    }
    return updatelname;
  }

  String PhoneNum = '';
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
          timeoutInSeconds: 10,
        );
        if (loginResult!.isNotEmpty) {
          PhoneNum = loginResult![0][0].toString();
        }
      });
    } catch (exc) {
      userLoginFuture = 'exc';
      exc.toString();
    } finally {
      await connection!.close();
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
          substitutionValues: {'emailValue': email, 'phoneNumberValue': phone},
          allowReuse: true,
          timeoutInSeconds: 10,
        );
        if (loginResult!.affectedRowCount > 0) {
          updatephonenum = 'ok';
        } else {
          updatephonenum = 'not';
        }
      });
    } catch (exc) {
      exc.toString();
    } finally {
      await connection!.close();
    }
    return updatephonenum;
  }

  String Pass = '';
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
          timeoutInSeconds: 10,
        );
        if (loginResult!.isNotEmpty) {
          Pass = loginResult![0][0].toString();
        }
      });
    } catch (exc) {
      userLoginFuture = 'exc';
      exc.toString();
    } finally {
      await connection!.close();
    }
    return Pass;
  }

  String updateppass = '';
  Future<String> UpdatePass(String email, String pass) async {
    try {
      await connection!.open();
      await connection!.transaction((loginConnection) async {
        //Check email registered or no
        loginResult = await loginConnection.query(
          'UPDATE public."Trainees" SET "password" = @passwordValue WHERE "email" = @emailValue',
          substitutionValues: {'emailValue': email, 'passwordValue': pass},
          allowReuse: true,
          timeoutInSeconds: 10,
        );
        if (loginResult!.affectedRowCount > 0) {
          updateppass = 'ok';
        } else {
          updateppass = 'not';
        }
      });
    } catch (exc) {
      exc.toString();
    } finally {
      await connection!.close();
    }
    return updateppass;
  }

  String stat = '';
  Future<String> fetchStatus(int? pID, String tEmail) async {
    try {
      await connection!.open();
      await connection!.transaction((statConnection) async {
          var traineeIdResult = await statConnection.query(
          'SELECT id FROM public."Trainees" WHERE email = @email',
          substitutionValues: {'email': tEmail},
        );

        if (traineeIdResult.isEmpty) {
          // Trainee not found for the provided email
          newRegiter = 'nop';
          return;
        }

        int traineeId = traineeIdResult[0][0] as int;
        //Check email registered or no
        final statResult = await statConnection.query(
          'SELECT "hasRegistered","haspaid","hasAttended","postAnswers" FROM public."Register" WHERE "ProgramID" = @pid AND "id" = "id"',
          substitutionValues: {'pid': pID, 'id': traineeId},
          allowReuse: true,
        );
          bool? hasReg ;
          bool? hasP ;
          bool? hasAT ;
          String? post ;
        if (statResult!.affectedRowCount > 0) {
        for (final row in statResult) {
          hasReg = row[0] as bool? ;
          hasP = row[1] as bool? ;
          hasAT = row[2] as bool? ;
          post = row[3] as String? ;
        }
        } 
        if (hasReg == false || hasReg == null) {
          stat = "register";
        }
        if (hasReg == true && (hasP == false || hasP == null)) {
          stat = "cancel";
        }
        if (hasReg == true && hasP == true && post == null) {
          stat = "review";
        }
      });
    } catch (exc) {
      exc.toString();
    } finally {
      await connection!.close();
    }
    return stat;
  }


  Future<List<Courses>> getAcceptedTrainingPrograms() async {
    _read();
    
    List<Courses> courses = [];
    try {
      await connection!.open();
      await connection!.transaction((queryConnection) async {
        // Query the "TrainingProgram" table for accepted programs
        final result = await queryConnection.query(
          '''
      SELECT
        "Topic",
        "TotalCost",
        "programID",
      


        array_to_string(
          ARRAY(
            SELECT first_name || ' ' || last_name
            FROM public."Faculty_Staff"
            WHERE id = ANY("InstructorID")
          ),
          ', '
        ) AS instructors,
         TO_CHAR(tp."time", 'HH24:MI:SS'),
        tp."programDescription"
      FROM public."TrainingProgram" tp
      JOIN public."Register" r ON r."ProgramID" = tp."programID"
      WHERE @currentCapacity < tp."capacity" AND tp."isreleased" = @released AND CURRENT_DATE < tp."startDate" AND r."hasRegistered" = @register ;
      ''',
          substitutionValues: {
            'register':false,
            'released': true,
            'currentCapacity': _myID.myVariable3,
          }, // Replace with actual values
          allowReuse: true,
        );
        // Process the result and create Course instances
        for (final row in result) {
          Courses course = Courses(
            row[0] as String?,
            (row[1] as num?)?.toDouble(),
            (row[2] as num?)?.toInt(),
            row[3] as String?,
            row[5] as String?,
             "","","","");
          // Add the created course to the list
          courses.add(course);
        }
      });
    } catch (exc) {
      // Handle exceptions (exc)
      print(exc.toString());
    } finally {
      await connection!.close();
    }
    return courses;
  }

  Future<List<Courses>> getRegisteredCourses(int? id) async {
    List<Courses> courses = [];
    try {
      await connection!.open();
      await connection!.transaction((queryConnection) async {
        // Query the "TrainingProgram" table for accepted programs
        final result = await queryConnection.query(
           '''
 SELECT tp."Topic", tp."TotalCost", tp."programID",         array_to_string(
          ARRAY(
            SELECT first_name || ' ' || last_name
            FROM public."Faculty_Staff"
            WHERE id = ANY("InstructorID")
          ),
          ', '
        ) AS instructors, tp."programDescription",tp."startDate",tp."endDate"
FROM public."TrainingProgram" tp
JOIN public."Register" r ON r."ProgramID" = tp."programID"
WHERE r."id" = @id AND tp."isreleased" = @release AND r."hasRegistered" = @register AND CURRENT_DATE < tp."startDate";

''',

          substitutionValues: {
            'release': true,
           'register':true,
         'id': id,
          },
          allowReuse: true,
          timeoutInSeconds: 2,
        );

        
        // Process the result and create Course instances
        for (final row in result) {
           String formattedDate1 = DateFormat('dd-MM-yyyy').format(row[5]);
           String formattedDate2 = DateFormat('dd-MM-yyyy').format(row[6]);
/*
          Courses course = Courses(
            row[0] as String?,
            (row[1] as num?)?.toDouble(),
            (row[2] as num?)?.toInt(),
            row[3] as String?,
            row[4] as String?,
            formattedDate1,
           formattedDate2,
          "",
          "",);*/
          // Add the created course to the list
          courses.add(course);
        }
      });
    } catch (exc) {
      // Handle exceptions (exc)
      print(exc.toString());
    }finally {
      await connection!.close();
    }
    return courses;
  }

Future<List<Courses>> getRunningCourses(int? id) async {
    List<Courses> courses = [];
    try {
      await connection!.open();
      await connection!.transaction((queryConnection) async {
        // Query the "TrainingProgram" table for accepted programs
        final result = await queryConnection.query(
           '''
 SELECT tp."Topic", tp."TotalCost", tp."programID",         array_to_string(
          ARRAY(
            SELECT first_name || ' ' || last_name
            FROM public."Faculty_Staff"
            WHERE id = ANY("InstructorID")
          ),
          ', '
        ) AS instructors, tp."programDescription",tp."startDate",tp."endDate"
FROM public."TrainingProgram" tp
JOIN public."Register" r ON r."ProgramID" = tp."programID"
WHERE  r."id" = @id AND tp."isreleased" = @release AND r."hasRegistered" = @register AND r."haspaid" = @paid AND CURRENT_DATE <= tp."endDate" AND tp."startDate" <= CURRENT_DATE;

''',

          substitutionValues: {
            'release': true,
           'register':true,
         'paid':true,
         'id': id,
          },
          allowReuse: true,
          timeoutInSeconds: 2,
        );

        
        // Process the result and create Course instances
        for (final row in result) {
           String formattedDate1 = DateFormat('dd-MM-yyyy').format(row[5]);
           String formattedDate2 = DateFormat('dd-MM-yyyy').format(row[6]);
/*
          Courses course = Courses(
            row[0] as String?,
            (row[1] as num?)?.toDouble(),
            (row[2] as num?)?.toInt(),
            row[3] as String?,
            row[4] as String?,
            formattedDate1,
           formattedDate2,
          "",
          "",);*/
          // Add the created course to the list
          courses.add(course);
        }
      });
    } catch (exc) {
      // Handle exceptions (exc)
      print(exc.toString());
    }finally {
      await connection!.close();
    }
    return courses;
  }

Future<List<Courses>> getCompletedCourses(int? id) async {
    List<Courses> courses = [];
    try {
      await connection!.open();
      await connection!.transaction((queryConnection) async {
        // Query the "TrainingProgram" table for accepted programs
        final result = await queryConnection.query(
           '''
 SELECT tp."Topic", tp."TotalCost", tp."programID",         array_to_string(
          ARRAY(
            SELECT first_name || ' ' || last_name
            FROM public."Faculty_Staff"
            WHERE id = ANY("InstructorID")
          ),
          ', '
        ) AS instructors, tp."programDescription",tp."startDate",tp."endDate", TO_CHAR(tp."time", 'HH24:MI:SS')
FROM public."TrainingProgram" tp
JOIN public."Register" r ON r."ProgramID" = tp."programID"
WHERE  r."id" = @id  AND r."hasRegistered" = @register AND r."haspaid" = @paid AND r."hasAttended" = @attend AND CURRENT_DATE > tp."endDate" ;

''',

          substitutionValues: {
            'attend': true,
           'register':true,
         'paid':true,
         'id': id,
          },
          allowReuse: true,
          timeoutInSeconds: 2,
        );

        
        // Process the result and create Course instances
        for (final row in result) {
           String formattedDate1 = DateFormat('dd-MM-yyyy').format(row[5]);
           String formattedDate2 = DateFormat('dd-MM-yyyy').format(row[6]);

          Courses course = Courses(
            row[0] as String?,
            (row[1] as num?)?.toDouble(),
            (row[2] as num?)?.toInt(),
            row[3] as String?,
            row[4] as String?,
            formattedDate1,
           formattedDate2,
          "",
          row[7] as String,);
          print( row[7] as String);
        //  print( row[8] as String);
          // Add the created course to the list
          courses.add(course);
        }
      });
    } catch (exc) {
      // Handle exceptions (exc)
      print(exc.toString());
    }finally {
      await connection!.close();
    }
    return courses;
  }

  bool cancel=false;
 
    Future<bool> cancelCourse(int? proid) async {
      print(proid);
     //proid=1;
      try {
    await connection!.open();
    loginResult = await connection!.query(
      'UPDATE public."Register" SET "hasRegistered" = @register WHERE "ProgramID" = @proid RETURNING "haspaid"',
      substitutionValues: {
        'proid': proid,
        'register': false,
      },
      allowReuse: true,
      timeoutInSeconds: 30,
    );
 

bool hasPaid = false; 

if (loginResult!.isNotEmpty) {
hasPaid = loginResult![0][0]as bool; 


 // hasPaid = payStatus['haspaid'] as bool;
}
/*
  if (newRegisterResult!.isNotEmpty) {
       _myID.myVariable2  = newRegisterResult![0][0] as int;
            }*/
if (hasPaid) {
  await connection!.query(
    'UPDATE public."Register" SET "refundRequsted" = @refund WHERE "ProgramID" = @proid',
    substitutionValues: {
      'proid': proid,
      'refund': true,
    },
    allowReuse: true,
    timeoutInSeconds: 2,
  );
}

 if (loginResult!.affectedRowCount > 0) {
  cancel = true;
  }

      
    } catch (exc) {
      exc.toString();
    }

    return cancel;

  }

  Future<List<CertificateData>> fetchCertifications(int id1) async {
 List<CertificateData> certificateDataList = [];

  try {
    await connection!.open();
    await connection!.transaction((loginConnection) async {
       loginResult = await loginConnection.query(
        '''
        SELECT r."certifications", tp."subject"
        FROM public."Register" r
        JOIN public."TrainingProgram" tp ON r."ProgramID" = tp."programID"
       WHERE  r."id" = @id1  AND r."hasRegistered" = @register AND r."haspaid" = @paid AND r."hasAttended" = @attend AND CURRENT_DATE > tp."endDate" ;
        ''',
        substitutionValues: {
          'id1': id1,
          'attend':true,
        },
        allowReuse: true,
        timeoutInSeconds: 30,
      );
 
      if (loginResult != null && loginResult is PostgreSQLResult) {
        // Iterate through the rows and add each certification to the list
        for (final row in loginResult!) {
         
         
       final String certificate = row[0].toString();
    
       final String programName = row[1].toString();
     
        final CertificateData certificateData1 = CertificateData(
          certificate: certificate,
         
          programName: programName,
        );

        certificateDataList.add(certificateData1);
      }
      // certificates.add(row[0].toString());
        }  
    });
  } catch (exc) {
    print(exc.toString());
  } finally {
    await connection!.close();
  }
   return certificateDataList;
}

  
Courses course = Courses("", 0.0, 0, "", "", "", "", "", "");
Future<Courses> Program(int? id) async {
  _read();
  try {
    await connection!.open();
    await connection!.transaction((courseConnection) async {
      // Query the "TrainingProgram" table for accepted programs
      final result = await courseConnection.query(
        '''
        SELECT
          "Topic",
          "TotalCost",
          array_to_string(
            ARRAY(
              SELECT first_name || ' ' || last_name
              FROM public."Faculty_Staff"
              WHERE id = ANY("InstructorID")
            ),
            ', '
          ) AS instructors,
          "programDescription",
          "startDate",
          "endDate"
        FROM public."TrainingProgram"
        WHERE "isreleased" = @released AND "programID" = @id
      ''',
        substitutionValues: {
          'released': true,
          'id': id
        },
        allowReuse: true,
      );
      // Process the result and create Course instances
      for (final row in result) {
        String formattedDate1 = DateFormat('dd-MM-yyyy').format(row[4]);
        String formattedDate2 = DateFormat('dd-MM-yyyy').format(row[5]);
        //DateTime startTime = row[6] as DateTime;
        //DateTime endTime = row[7] as DateTime;

        //print(startTime);
        //print(endTime);
        Courses currentCourse = Courses(
          row[0] as String?,
          (row[1] as num?)?.toDouble(),
          id,
          row[2] as String?,
          row[3] as String,
          formattedDate1,
          formattedDate2,
          "",
          "",
        );

        // Check if the current course has the desired ID
        if (currentCourse.id == id) {
          course = currentCourse;
          break; // Break out of the loop once the course is found
        }
      }
    });
  } catch (exc) {
    // Handle exceptions (exc)
    print(exc.toString());
  } finally {
    await connection!.close();
  }
  return course;
}


  String newRegiter = '';
  Future<String> RegisterToProgram(String q1, String q2, String q3, String q4,
      String q5, String email, int? PID) async {
    List<String> preAnswers = [q1, q2, q3, q4, q5];
    String preAnswersAsString = "{'${preAnswers.join("','")}'";
    preAnswersAsString += "}";

    try {
      await connection!.open();
      await connection!.transaction((regiterConnection) async {
        // Step 1: Get Trainee ID based on email
        var traineeIdResult = await regiterConnection.query(
          'SELECT id FROM public."Trainees" WHERE email = @email',
          substitutionValues: {'email': email},
        );

        if (traineeIdResult.isEmpty) {
          // Trainee not found for the provided email
          newRegiter = 'nop';
          return;
        }

        int traineeId = traineeIdResult[0][0] as int;

        // Step 2: Insert into "Register" table
        newRegisterResult = await regiterConnection.query(
          'INSERT INTO public."Register"("ProgramID","id","hasRegistered","preAnswers") '
          'VALUES (@programId, @traineeId, @hasR, @preAns)',
          substitutionValues: {
            'programId': PID,
            'traineeId': traineeId,
            'hasR': true,
            'preAns': preAnswersAsString,
          },
          allowReuse: true,
          timeoutInSeconds: 30,
        );

        newRegiter = (newRegisterResult!.affectedRowCount > 0 ? 'reg' : 'nop');
         _myID.myVariable3++;
      });
    } catch (exc) {
      newRegiter = 'exc';
      print(exc.toString());
    } finally {
      await connection!.close();
    }

    return newRegiter;
  }

  String postInsert = '';
  Future<String> enterAFAnswers(String q1, String q2, String q3, String q4,
      String q5, String email, int? PID) async {
    List<String> postAnswers = [q1, q2, q3, q4, q5];
    String postAnswersAsString = "{'${postAnswers.join("','")}'";

    try {
      await connection!.open();
      await connection!.transaction((regiterConnection) async {
        // Step 1: Get Trainee ID based on email
        var traineeIdResult = await regiterConnection.query(
          'SELECT id FROM public."Trainees" WHERE email = @email',
          substitutionValues: {'email': email},
        );

        if (traineeIdResult.isEmpty) {
          // Trainee not found for the provided email
          newRegiter = 'nop';
          return;
        }

        int traineeId = traineeIdResult[0][0] as int;

        // Step 2: Insert into "Register" table

        newRegisterResult = await regiterConnection.query(
          'UPDATE public."Register" '
          'SET "preAnswers" = @postAnswers '
          'WHERE "id" = @id AND "ProgramID" = @programID AND "hasAttended" = @hasAt AND "hasRegistered" = @hasR',
          substitutionValues: {
            'postAnswers': postAnswersAsString,
            'id': traineeId, 
            'programID': PID, 
            'hasAt': true,
            'hasR': true,
          },
          allowReuse: true,
          timeoutInSeconds: 30,
        );
        postInsert = (newRegisterResult!.affectedRowCount > 0 ? 'reg' : 'nop');
      });
    } catch (exc) {
      postInsert = 'exc';
      print(exc.toString());
    } finally {
      await connection!.close();
    }
    return postInsert;
  }

  Future<List<Courses>> filteredPrograms(String? category) async {
    _read();
    List<Courses> courses = [];
    int collegeID = 0;

    if (category == "Business") {
      collegeID = 14;
    } else if (category == "Architecture") {
      collegeID = 10;
    } else if (category == "Health") {
      collegeID = 15;
    } else if (category == "Computer") {
      collegeID = 7;
    } else if (category == "Language") {
      collegeID = 11;
    } else if (category == "Art") {
      collegeID = 12;
    }

    try {
      await connection!.open();
      await connection!.transaction((queryConnection) async {
        // Query the "TrainingProgram" table for accepted programs
        final result = await queryConnection.query(
          '''
      SELECT
        "subject",
        "TotalCost",
        "programID",
        array_to_string(
          ARRAY(
            SELECT first_name || ' ' || last_name
            FROM public."Faculty_Staff"
            WHERE id = ANY("InstructorID")
          ),
          ', '
        ) AS instructors,
        "programDescription"
      FROM public."TrainingProgram"
      WHERE "isreleased" = @released AND "CollageID" = @collegeID
      ''',
          substitutionValues: {
            'released': true,
            'collegeID': collegeID
          }, // Replace with actual values
          allowReuse: true,
        );
        // Process the result and create Course instances
        for (final row in result) {
          Courses course = Courses(
            row[0] as String?,
            (row[1] as num?)?.toDouble(),
            (row[2] as num?)?.toInt(),
            row[3] as String?,
            row[4] as String?,
            "","","","");
          // Add the created course to the list
          courses.add(course);
        }
      });
    } catch (exc) {
      // Handle exceptions (exc)
      print(exc.toString());
    } finally {
      await connection!.close();
    }
    return courses;
  }
}

class Courses {
  String? name;
  double? price;
  int? id;
  String? startDate ;
  String? endDate ;
  String? startTime ;
String endTime ="" ;
  String? instructer;
  String? description;

  Courses(String? name, double? price, int? id, String? instructer,
      String? description, String startDate, String endDate, String startTime, String endTime){
    this.name = name;
    this.price = price;
    this.id = id;
    this.instructer = instructer;
    this.description = description;
    this.startDate = startDate;
    this.endDate = endDate;
    this.startTime = startTime;
    this.endTime = endTime;
  }

  // Getter and setter for the 'name' property
  String? get _name => name;
  set _name(String? value) => name = value;

  // Getter and setter for the 'price' property
  double? get _price => price;
  set _price(double? value) => price = value;

  // Getter and setter for the 'startDate' property
  String? get _startDate => startDate;
  set _startDate(String? value) => startDate = value;

    // Getter and setter for the 'endDate' property
  String? get _endDate => endDate;
  set _endDate(String? value) => endDate = value;

  // Getter and setter for the 'startTime' property
  String? get _startTime => startTime;
  set _startTime(String? value) => startTime = value;

  // Getter and setter for the 'endTime' property
  String get _endTime => endTime;
  set _endTime(String value) => endTime = value;

  // Getter and setter for the 'instructer' property
  String? get _instructer => instructer;
  set _instructer(String? value) => instructer = value;

  // Getter and setter for the 'id' property
  int? get _id => id;
  set _id(int? value) => id = value;

  // Getter and setter for the 'description' property
  String? get _description => description;
  set _description(String? value) => description = value;
}

class CertificateData {
  String certificate;
  String programName;

  CertificateData({required this.certificate, required this.programName});
}
