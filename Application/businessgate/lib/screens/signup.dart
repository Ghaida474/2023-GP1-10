import 'dart:async';
import 'dart:core';
import 'package:flutter/material.dart';
import 'package:flutter_pw_validator/flutter_pw_validator.dart';
import '../localization/localization_const.dart';
import '../myservice.dart';
import '../models/model_user.dart';
import '../utils/colors.dart';

class SignUp extends StatefulWidget {
  const SignUp({super.key});

  @override
  State<SignUp> createState() => _SignUpState();
}

enum Genders { male, female }

class _SignUpState extends State<SignUp> {
  final formkey = GlobalKey<FormState>();

  MyService _myEmail = MyService();

  Genders selectedGender = Genders.male;

  String selectedNationality = '';

  TextEditingController _FnameTextController = TextEditingController();
  TextEditingController _LnameTextController = TextEditingController();
  TextEditingController _fullnameTextController = TextEditingController();
  TextEditingController _phoneNumberTextController = TextEditingController();
  TextEditingController _emailTextController = TextEditingController();
  TextEditingController _passwordTextController = TextEditingController();
  TextEditingController _confirmPasswordTextController = TextEditingController();
  TextEditingController _IDTextController = TextEditingController();
  TextEditingController _genderTextController = TextEditingController();

  bool success = false;

  bool passToggle = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        extendBodyBehindAppBar: true,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          title: Text(
            getTranslate(context, 'signup.sign_up'),
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
        ),
        body: Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(colors: [
                hexStringColor("#6FBCF6"),
                hexStringColor("##E3E0D2")
              ], begin: Alignment.topCenter, end: Alignment.bottomCenter),
            ),
            child: SingleChildScrollView(
                child: Padding(
              padding: EdgeInsets.fromLTRB(
                  20, MediaQuery.of(context).size.height * 0.2, 20, 400),
              child: Form(
                key: formkey,
                child: Column(
                  children: <Widget>[
                    logoWidgetSignUP("assets/images/Logo.jpg"),
                    const SizedBox(
                      height: 25,
                    ),
                    nameField(getTranslate(context, 'signup.firstname'),
                        Icons.person, false, _FnameTextController),
                    const SizedBox(
                      height: 20,
                    ),
                    nameField(getTranslate(context, 'signup.lastname'),
                        Icons.person, false, _LnameTextController),
                    const SizedBox(
                      height: 20,
                    ),
                    nameField(getTranslate(context, 'signup.name'),
                        Icons.person, false, _fullnameTextController),
                    const SizedBox(
                      height: 20,
                    ),
                    IDField(getTranslate(context, 'signup.NID'), Icons.person,
                        false, _IDTextController),
                    const SizedBox(
                      height: 20,
                    ),
                    // Gender selection buttons
                    Text(getTranslate(context, 'signup.Gender'),
                        style: TextStyle(
                            fontSize: 20,
                            color: Color.fromARGB(217, 0, 29, 103),
                            fontWeight: FontWeight.bold)),
                    Column(
                      children: <Widget>[
                        RadioListTile(
                          title: Text(getTranslate(context, 'signup.M')),
                          value: Genders.male,
                          groupValue: selectedGender,
                          onChanged: (value) {
                            setState(() {
                              selectedGender = value!;
                            });
                          },
                        ),
                        RadioListTile(
                          title: Text(getTranslate(context, 'signup.F')),
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
                    mobileField(getTranslate(context, 'signup.mobile_number'),
                        Icons.phone, false, _phoneNumberTextController),
                    const SizedBox(
                      height: 20,
                    ),
                    emailField(getTranslate(context, 'signup.email_address'),
                        Icons.email, false, _emailTextController),
                    const SizedBox(
                      height: 20,
                    ),
                    PasswordField(getTranslate(context, 'signup.password'),
                        Icons.lock, _passwordTextController),
                    const SizedBox(
                      height: 8,
                    ),
                    FlutterPwValidator(
                      defaultColor: Colors.grey.shade300,
                      controller: _passwordTextController,
                      successColor: Colors.green.shade700,
                      minLength: 8,
                      uppercaseCharCount: 1,
                      numericCharCount: 1,
                      specialCharCount: 1,
                      normalCharCount: 1,
                      width: 400,
                      height: 190,
                      onSuccess: () {
                        setState(() {
                          success = true;
                        });
                      },
                      onFail: () {
                        setState(() {
                          success = false;
                        });
                      },
                    ),
                    const SizedBox(
                      height: 40,
                    ),
                    ConfirmField(
                        getTranslate(context, 'signup.confirmPassword'),
                        Icons.lock,
                        _confirmPasswordTextController),
                    const SizedBox(
                      height: 8,
                    ),
                    FlutterPwValidator(
                      defaultColor: Colors.grey.shade300,
                      controller: _confirmPasswordTextController,
                      successColor: Colors.green.shade700,
                      minLength: 8,
                      uppercaseCharCount: 1,
                      numericCharCount: 1,
                      specialCharCount: 1,
                      normalCharCount: 1,
                      width: 400,
                      height: 190,
                      onSuccess: () {
                        setState(() {
                          success = true;
                        });
                      },
                      onFail: () {
                        setState(() {
                          success = false;
                        });
                      },
                    ),
                    const SizedBox(
                      height: 40,
                    ),
                    SignUpButton(context, () {
                      registerMethod(context);
                    })
                  ],
                ),
              ),
            ))));
  }

  Image logoWidgetSignUP(String imageName) {
    return Image.asset(
      imageName,
      fit: BoxFit.fitWidth,
      width: 180,
      height: 180,
    );
  }

  TextFormField nameField(String text, IconData icon, bool isPasswordType,
      TextEditingController controller) {
    return  TextFormField(
      controller: controller,
      autovalidateMode: AutovalidateMode.onUserInteraction,
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
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
      validator: (value) {
        formkey.currentState?.validate();
        if (value!.isEmpty || !RegExp(r'^[a-z A-Z]+$').hasMatch(value)) {
          return getTranslate(context, 'signup.CN');
        } else
          return null;
      },
    );
  }

   TextFormField fullNameField(String text, IconData icon, bool isPasswordType,
      TextEditingController controller) {
    return  TextFormField(
      controller: controller,
      autovalidateMode: AutovalidateMode.onUserInteraction,
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
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
    );
  }

  TextFormField IDField(String text, IconData icon, bool isPasswordType,
      TextEditingController controller) {
    return TextFormField(
      controller: controller,
      autovalidateMode: AutovalidateMode.onUserInteraction,
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
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
      validator: (value) {
        if (value!.isEmpty || !RegExp(r'^\d{10}$').hasMatch(value!)) {
          return getTranslate(context, 'signup.CID');
        } else
          return null;
      },
    );
  }

  TextFormField emailField(String text, IconData icon, bool isPasswordType,
      TextEditingController controller) {
    return TextFormField(
      controller: controller,
      autovalidateMode: AutovalidateMode.onUserInteraction,
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
          hintText: "example@example.com",
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
      validator: (value) {
        if (value!.isEmpty ||
            !RegExp(r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$')
                .hasMatch(value!)) {
          return getTranslate(context, 'signup.CE');
        } else
          return null;
      },
    );
  }

  TextFormField mobileField(String text, IconData icon, bool isPasswordType,
      TextEditingController controller) {
    return TextFormField(
      controller: controller,
      autovalidateMode: AutovalidateMode.onUserInteraction,
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
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
      validator: (value) {
        if (value!.isEmpty || !RegExp(r'^05\d{8}$').hasMatch(value!)) {
          return getTranslate(context, 'signup.CM');
        } else
          return null;
      },
    );
  }

  TextFormField PasswordField(
      String text, IconData icon, TextEditingController controller) {
    return TextFormField(
      controller: controller,
      obscureText: passToggle,
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
          suffixIcon: InkWell(
            onTap: () {
              setState(() {
                passToggle = !passToggle;
              });
            },
            child: Icon(passToggle ? Icons.visibility_off : Icons.visibility),
          ),
          hintStyle:
              TextStyle(color: Color.fromARGB(156, 0, 0, 0).withOpacity(0.9)),
          labelText: text,
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
    );
  }

  TextFormField ConfirmField(
      String text, IconData icon, TextEditingController controller) {
    return TextFormField(
      controller: controller,
      obscureText: passToggle,
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
          suffixIcon: InkWell(
            onTap: () {
              setState(() {
                passToggle = !passToggle;
              });
            },
            child: Icon(passToggle ? Icons.visibility_off : Icons.visibility),
          ),
          hintStyle:
              TextStyle(color: Color.fromARGB(156, 0, 0, 0).withOpacity(0.9)),
          labelText: text,
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
      validator: (value) {
        if (_confirmPasswordTextController != _passwordTextController) {
          return getTranslate(context, 'signup.CconfirmP');
        }else
          return null;
      },
    );
  }

  Container SignUpButton(BuildContext context, Function onTap) {
    return Container(
        width: MediaQuery.of(context).size.width,
        height: 50,
        margin: const EdgeInsets.fromLTRB(0, 10, 0, 20),
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(90)),
        child: ElevatedButton(
          onPressed: () {
            if (formkey.currentState!.validate()) {
              onTap();
            }
          },
          child: Text(
            getTranslate(context, 'signup.sign_up'),
            style: const TextStyle(
                color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
          ),
          style: ButtonStyle(
              backgroundColor: MaterialStateProperty.resolveWith((states) {
                if (states.contains(MaterialState.pressed)) {
                  return hexStringColor("#01253D");
                }
                return hexStringColor("#095590");
              }),
              shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                  RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30)))),
        ));
  }

  void registerMethod(BuildContext context) {
    String Fname = _FnameTextController.text;
    String Lname = _LnameTextController.text;
    String ID = _IDTextController.text;
    String PhoneNumber = _phoneNumberTextController.text;
    String Email = _emailTextController.text;
    String Password = _passwordTextController.text;
    String Gender = selectedGender.toString();
    String fullN = _fullnameTextController.text ;

    List<String> parts = Gender.split('.');
    String genderString = parts.last;

    ModelsUsers()
        .registerTrainee(
            Fname,
            Lname,
            PhoneNumber,
            Email,
            // hash the password !!!
            Password,
            ID,
            genderString,
            fullN)
        .then((Trainee) {
      if (Trainee.toString().contains('reg')) {
        setState(() {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            backgroundColor: Colors.blue[100],
            elevation: 10.0,
            shape: Border.all(
                color: Colors.green, width: 0.5, style: BorderStyle.solid),
            content: Text(
              getTranslate(context, 'signup.register_suc'),
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
          _fullnameTextController.clear();

          Timer(Duration(seconds: 1), () {
            Navigator.pushNamed(context, '/home');
            Navigator.of(context).pushReplacementNamed('/bottomNavi');
          });
        });
      } else if (Trainee.toString().contains('nop')) {
        setState(() {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              backgroundColor: Colors.blue[100],
              elevation: 10.0,
              shape: Border.all(
                  color: Colors.red, width: 0.5, style: BorderStyle.solid),
              content: Text(
                getTranslate(context, 'signup.register_fai'),
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
          _fullnameTextController.clear();

          Timer(Duration(seconds: 1), () {
            Navigator.pushNamed(context, '/signup');
          });
        });
      } else if (Trainee.toString().contains('alr')) {
        setState(() {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              backgroundColor: Colors.blue[100],
              elevation: 10.0,
              shape: Border.all(
                  color: Colors.yellow, width: 0.5, style: BorderStyle.solid),
              content: Text(
                getTranslate(context, 'signup.email_registered'),
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
          _fullnameTextController.clear();
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
                getTranslate(context, 'signup.something_wrong'),
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
          _fullnameTextController.clear();

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
              getTranslate(context, 'signup.something_wrong'),
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
        _fullnameTextController.clear();

      });
    }).whenComplete(() => null);
  }
}
