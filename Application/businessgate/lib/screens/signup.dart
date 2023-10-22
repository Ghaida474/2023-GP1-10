import 'dart:async';
import 'dart:core';

import 'dart:convert';
import 'package:http/http.dart' as http;

import 'package:businessgate/screens/home.dart';
import 'package:flutter/material.dart';

import '../myservice.dart';
import '../models/model_user.dart';
import '../utils/colors.dart';


class SignUp extends StatefulWidget {
  const SignUp({super.key});

  @override
  State<SignUp> createState() => _SignUpState();
}

// Function to fetch nationality data from the API
/*
Future<List<String>> fetchNationalities() async {
  final response = await http.get(Uri.parse(' http://api.worldbank.org/v2/country')); // Replace with your API URL

  if (response.statusCode == 200) {
    final List<dynamic> data = json.decode(response.body);
    return data.map((item) => item.toString()).toList();
  } else {
    throw Exception('Failed to load nationality data');
  }
}*/

enum Genders { male, female, other }

class _SignUpState extends State<SignUp> {

  final formkey = GlobalKey<FormState>() ;

    MyService _myEmail = MyService();

    Genders selectedGender = Genders.male;

    List<String> nationalityOptions = [];

    String selectedNationality = '';

  TextEditingController _FnameTextController = TextEditingController() ;
  TextEditingController _LnameTextController = TextEditingController() ;
  TextEditingController _phoneNumberTextController = TextEditingController() ;
  TextEditingController _emailTextController = TextEditingController() ;
  TextEditingController _passwordTextController = TextEditingController() ;
  TextEditingController _IDTextController = TextEditingController() ;
  TextEditingController _genderTextController = TextEditingController() ;
  TextEditingController _nationTextController = TextEditingController() ;

  String searchedNationName = '';
/*
  @override
  void initState() {
  super.initState();
  fetchNationalities().then((nationalities) {
    setState(() {
      nationalityOptions = nationalities;
    });
  });
  } */


  @override
  Widget build(BuildContext context) {
    return Scaffold(extendBodyBehindAppBar: true, 
    appBar: AppBar(
      backgroundColor: Colors.transparent,
      elevation: 0,
      title: const Text("SIGN UP", 
      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),),
    ),
    body: Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [hexStringColor("#6FBCF6"), 
          hexStringColor("##E3E0D2")
          ], begin: Alignment.topCenter, 
          end: Alignment.bottomCenter ),
    ),child : SingleChildScrollView(child: Padding(
              padding: EdgeInsets.fromLTRB(
                20, MediaQuery.of(context).size.height * 0.2, 20, 400),
    child: Form(
      key: formkey,
                child: Column( children: <Widget>[
                  logoWidgetSignUP("assets/images/Logo.jpg"),
                  const SizedBox(
                    height: 25,
                  ),
                    nameField("Enter First Name", Icons.person, false, _FnameTextController),
                    const SizedBox(
                    height: 20,
                  ),
                  nameField("Enter Last Name", Icons.person, false, _LnameTextController),
                    const SizedBox(
                    height: 20,
                  ),
                    IDField("Enter National ID", Icons.person, false, _IDTextController),
                    const SizedBox(
                    height: 20,
                  ),
                     // Gender selection buttons
                  Text('Select Gender :',
                  style: TextStyle(fontSize: 20,
                  color: Color.fromARGB(217, 0, 29, 103),
                  fontWeight: FontWeight.bold)),
                  Column(
                     children: <Widget>[
                     RadioListTile(
                     title: const Text('Male'),
                     value: Genders.male,
                     groupValue: selectedGender,
                     onChanged: (value) {
                      setState(() {
                        selectedGender = value!;
                      });
                     },
                    ),
                    RadioListTile(
                     title: const Text('Female'),
                     value: Genders.female,
                     groupValue: selectedGender,
                     onChanged: (value) {
                      setState(() {
                        selectedGender = value!;
                      });
                      },
                    ),
                   ],
                  ),
                    const SizedBox(
                    height: 20,
                  ),
                  mobileField("Enter Mobile Number", Icons.phone, false, _phoneNumberTextController),
                    const SizedBox(
                    height: 20,
                  ),
                  /*DropdownButtonFormField<String>(
  decoration: InputDecoration(
    labelText: 'Nationality',
  labelStyle: TextStyle(
    color: Color.fromARGB(217, 0, 29, 103), 
    fontWeight: FontWeight.bold)),
  value: selectedNationality,
  items: nationalityOptions.map((String option) {
    return DropdownMenuItem<String>(
      value: option,
      child: Text(option),
    );
  }).toList(),
  onChanged: (newValue) {
    setState(() {
      selectedNationality = newValue.toString();
    });
  },
),*/
/*const SizedBox(
                    height: 10,
                  ),*/
                  emailField("Enter Email", Icons.email, false, _emailTextController),
                  const SizedBox(
                    height: 20,
                  ),
                  PasswordField("Enter Password", Icons.lock, true, _passwordTextController),
                  const SizedBox(
                    height: 20,
                  ),
                  SignUpButton(context, () {
                   registerMethod(context);
                  })
                ],),),
                
    )
     ) ));
  }

  Image logoWidgetSignUP(String imageName) {
    return Image.asset(
      imageName,
      fit: BoxFit.fitWidth,
      width: 180,
      height: 180,
    );
  }

  TextFormField nameField (String text, IconData icon, bool isPasswordType, 
  TextEditingController controller) {
    return TextFormField( controller: controller,
    cursorColor: Colors.white,
    style: TextStyle(color: Colors.white.withOpacity(0.9)),
    decoration: InputDecoration(
      focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(30),
                borderSide: const BorderSide(
                  color: Color.fromARGB(255, 2, 14, 52),
                )),
      prefixIcon: Icon(
        icon,
        color: const Color.fromARGB(179, 255, 255, 255),
      ),
      labelText: text,
      labelStyle: TextStyle( color: Colors.white.withOpacity(0.9)),
      filled: true,
      floatingLabelBehavior: FloatingLabelBehavior.never,
      fillColor: hexStringColor("#095590").withOpacity(0.45),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(30.0),
        borderSide: const BorderSide(width: 0, style: BorderStyle.none))
      ),
      validator: (value) {
        if(value!.isEmpty || !RegExp(r'^[a-z A-Z]+$').hasMatch(value!)){
          return "Enter a Correct Name";
        } else
        return null ;
      },
    );

  } 

  TextFormField IDField (String text, IconData icon, bool isPasswordType, 
  TextEditingController controller) {
    return TextFormField( controller: controller,
    cursorColor: Colors.white,
    style: TextStyle(color: Colors.white.withOpacity(0.9)),
    decoration: InputDecoration(
      focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(30),
                borderSide: const BorderSide(
                  color: Color.fromARGB(255, 2, 14, 52),
                )),
      prefixIcon: Icon(
        icon,
        color: const Color.fromARGB(179, 255, 255, 255),
      ),
      labelText: text,
      labelStyle: TextStyle( color: Colors.white.withOpacity(0.9)),
      filled: true,
      floatingLabelBehavior: FloatingLabelBehavior.never,
      fillColor: hexStringColor("#095590").withOpacity(0.45),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(30.0),
        borderSide: const BorderSide(width: 0, style: BorderStyle.none))
      ),
      validator: (value) {
        if(value!.isEmpty || !RegExp(r'^\d{10}$').hasMatch(value!)){
          return "Enter a Correct ID";
        } else
        return null ;
      },
    );

  } 

  TextFormField emailField (String text, IconData icon, bool isPasswordType, 
  TextEditingController controller) {
    return TextFormField( controller: controller,
    cursorColor: Colors.white,
    style: TextStyle(color: Colors.white.withOpacity(0.9)),
    decoration: InputDecoration(
      focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(30),
                borderSide: const BorderSide(
                  color: Color.fromARGB(255, 2, 14, 52),
                )),
      prefixIcon: Icon(
        icon,
        color: const Color.fromARGB(179, 255, 255, 255),
      ),
      labelText: text,
      labelStyle: TextStyle( color: Colors.white.withOpacity(0.9)),
      filled: true,
      floatingLabelBehavior: FloatingLabelBehavior.never,
      fillColor: hexStringColor("#095590").withOpacity(0.45),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(30.0),
        borderSide: const BorderSide(width: 0, style: BorderStyle.none))
      ),
      validator: (value) {
        if(value!.isEmpty || !RegExp(r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$').hasMatch(value!)){
          return "Enter a Correct Email";
        } else
        return null ;
      },
    );

  } 

  TextFormField mobileField (String text, IconData icon, bool isPasswordType, 
  TextEditingController controller) {
    return TextFormField( controller: controller,
    cursorColor: Colors.white,
    style: TextStyle(color: Colors.white.withOpacity(0.9)),
    decoration: InputDecoration(
      focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(30),
                borderSide: const BorderSide(
                  color: Color.fromARGB(255, 2, 14, 52),
                )),
      prefixIcon: Icon(
        icon,
        color: const Color.fromARGB(179, 255, 255, 255),
      ),
      labelText: text,
      labelStyle: TextStyle( color: Colors.white.withOpacity(0.9)),
      filled: true,
      floatingLabelBehavior: FloatingLabelBehavior.never,
      fillColor: hexStringColor("#095590").withOpacity(0.45),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(30.0),
        borderSide: const BorderSide(width: 0, style: BorderStyle.none))
      ),
      validator: (value) {
        if(value!.isEmpty || !RegExp(r'^05\d{8}$').hasMatch(value!)){
          return "Enter a Correct Mobile Number";
        } else
        return null ;
      },
    );

  } 

  TextFormField PasswordField (String text, IconData icon, bool isPasswordType, 
  TextEditingController controller) {
    return TextFormField( controller: controller,
    obscureText: isPasswordType,
    enableSuggestions: !isPasswordType,
    cursorColor: Colors.white,
    style: TextStyle(color: Colors.white.withOpacity(0.9)),
    decoration: InputDecoration(
      focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(30),
                borderSide: const BorderSide(
                  color: Color.fromARGB(255, 2, 14, 52),
                )),
      prefixIcon: Icon(
        icon,
        color: const Color.fromARGB(179, 255, 255, 255),
      ),
      suffixIcon: GestureDetector(
              onTap: () {
                 setState(() {
                  isPasswordType = !isPasswordType;
                });
              },
              child: Icon(
                isPasswordType ? Icons.visibility_off : Icons.visibility,
                size: 16,
              ),
            ),
            hintText: 'Must be 8 character long',
            hintStyle: TextStyle(color: Color.fromARGB(156, 0, 0, 0).withOpacity(0.9)) ,
      labelText: text,
      labelStyle: TextStyle( color: Colors.white.withOpacity(0.9)),
      filled: true,
      floatingLabelBehavior: FloatingLabelBehavior.never,
      fillColor: hexStringColor("#095590").withOpacity(0.45),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(30.0),
        borderSide: const BorderSide(width: 0, style: BorderStyle.none))
      ),
      validator: (value) {
        if(value!.isEmpty || !RegExp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',).hasMatch(value!)){
          return "Enter a Correct Password Must contain : \n Capital letter \n Small letter \n Number and special character";
        } else
        return null ;
      },
     keyboardType: isPasswordType
      ? TextInputType.visiblePassword
      : TextInputType.none
    );

  }

  Container SignUpButton (BuildContext context, Function onTap) {
    return Container(width: MediaQuery.of(context).size.width,
    height: 50,
    margin: const EdgeInsets.fromLTRB(0, 10, 0, 20),
    decoration: BoxDecoration(borderRadius: BorderRadius.circular(90)),
    child: ElevatedButton(onPressed: () { 
      if(formkey.currentState!.validate()) {
       onTap();  
      }}, 
      child: Text ('SIGN UP', 
      style: const TextStyle(
        color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
        ),
        style: ButtonStyle(backgroundColor: MaterialStateProperty.resolveWith((states) {
          if (states.contains(MaterialState.pressed)) {
            return hexStringColor("#01253D");
          }
          return hexStringColor("#095590") ;
        }),
        shape: MaterialStateProperty.all<RoundedRectangleBorder>(
          RoundedRectangleBorder(borderRadius: BorderRadius.circular(30))
        )
        ),
    )
    ); 
  }

  void registerMethod(BuildContext context) {

    String Fname = _FnameTextController.text;
    String Lname = _LnameTextController.text;
    String ID = _IDTextController.text;
    String PhoneNumber = _phoneNumberTextController.text;
    String Email = _emailTextController.text;
    String Password = _passwordTextController.text;
    String Gender = selectedGender.toString();
  
  List<String> parts = Gender.split('.');
  String genderString = parts.last;

      ModelsUsers()
          .registerTrainee(
        Fname, Lname, PhoneNumber,Email,
        // hash the password !!!
        Password,ID,genderString,selectedNationality)
          .then((Trainee) { // open then
        if (Trainee.toString().contains('reg')) { // first if
          setState(() { // state open
            ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              backgroundColor: Colors.blue[100],
              elevation: 10.0,
              shape: Border.all(
                  color: Colors.green, width: 0.5, style: BorderStyle.solid),
              content: Text(
                "Register Successful",
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 18.0,
                  fontStyle: FontStyle.italic,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2.0,
                ),
                textAlign: TextAlign.center,
              ),
            ));
            _myEmail.myVariable = _emailTextController.text;

            _FnameTextController.clear();
            _LnameTextController.clear();
            _phoneNumberTextController.clear();
            _emailTextController.clear();
            _passwordTextController.clear();
            _IDTextController.clear();
            _genderTextController.clear();
            _nationTextController.clear;
  
            Timer(Duration(seconds: 2), () {
              Navigator.pushNamed(context, '/home');
            });
          });
        } else 
        if (Trainee.toString().contains('nop')) { // second if
          setState(() {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                backgroundColor: Colors.blue[100],
                elevation: 10.0,
                shape: Border.all(
                    color: Colors.red, width: 0.5, style: BorderStyle.solid),
                content: Text(
                  "Register Failed",
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 18.0,
                    fontStyle: FontStyle.italic,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 2.0,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            );
            _FnameTextController.clear();
            _LnameTextController.clear();
            _phoneNumberTextController.clear();
            _emailTextController.clear();
            _passwordTextController.clear();
            _IDTextController.clear();
            _genderTextController.clear();
            _nationTextController.clear;

            Timer(Duration(seconds: 2), () {
              Navigator.pushNamed(context, '/signup');
            });
          });
        } else 
        if (Trainee.toString().contains('alr')) {
          setState(() {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                backgroundColor: Colors.blue[100],
                elevation: 10.0,
                shape: Border.all(
                    color: Colors.yellow, width: 0.5, style: BorderStyle.solid),
                content: Text(
                  "Email Already Registered",
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 18.0,
                    fontStyle: FontStyle.italic,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 2.0,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            );
            _FnameTextController.clear();
            _LnameTextController.clear();
            _phoneNumberTextController.clear();
            _emailTextController.clear();
            _passwordTextController.clear();
            _IDTextController.clear();
            _genderTextController.clear();
            _nationTextController.clear;

            Timer(Duration(seconds: 2), () {
              Navigator.pushNamed(context, '/signin');
            });
          });
        } else {
          setState(() {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                backgroundColor: Colors.white,
                elevation: 10.0,
                shape: Border.all(
                  color: Colors.red,
                  width: 0.5,
                  style: BorderStyle.solid,
                ),
                content: Text(
                  "Something Went Wrong",
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 18.0,
                    fontStyle: FontStyle.italic,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.0,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            );
            _FnameTextController.clear();
            _LnameTextController.clear();
            _phoneNumberTextController.clear();
            _emailTextController.clear();
            _passwordTextController.clear();
            _IDTextController.clear();
        _genderTextController.clear();
        _nationTextController.clear;

            Timer(Duration(seconds: 2), () {
              Navigator.pushNamed(context, '/signup');
            });
          });
        }
      }).catchError((err) {
        setState(() {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              backgroundColor: Colors.blue[100],
              elevation: 10.0,
              shape: Border.all(
                  color: Colors.red, width: 0.5, style: BorderStyle.solid),
              content: Text(
                "Something Went Wrong",
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 18.0,
                  fontStyle: FontStyle.italic,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2.0,
                ),
                textAlign: TextAlign.center,
              ),
            ),
          );
          _FnameTextController.clear();
            _LnameTextController.clear();
            _phoneNumberTextController.clear();
            _emailTextController.clear();
            _passwordTextController.clear();
            _IDTextController.clear();
        _genderTextController.clear();
        _nationTextController.clear;

          Timer(Duration(seconds: 2), () {
            Navigator.pushNamed(context, '/signup');
          });
        });
      }).whenComplete(() => null);
      }
     
  }



