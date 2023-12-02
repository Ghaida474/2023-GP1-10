import 'dart:async';
import 'package:businessgate/screens/forget.dart';
import 'package:businessgate/screens/signup.dart';
import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';
import '../localization/localization_const.dart';
import '../myservice.dart';
import '../models/model_user.dart';

class SignIn extends StatefulWidget {
  const SignIn({super.key});

  @override
  State<SignIn> createState() => _SignInState();
}

class _SignInState extends State<SignIn> {
  final formkey = GlobalKey<FormState>();

  MyService _myEmail = MyService();

  TextEditingController _passwordTextController = TextEditingController();
  TextEditingController _emailTextController = TextEditingController();

  bool passToggle = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
            colors: [hexStringColor("#6FBCF6"), hexStringColor("#E3E0D2")],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter),
      ),
      child: SingleChildScrollView(
        child: Padding(
            padding: EdgeInsets.fromLTRB(
                20, MediaQuery.of(context).size.height * 0.18, 20, 280),
            child: Form(
              key: formkey,
              //autovalidateMode: AutovalidateMode.onUserInteraction,
              child: Column(
                children: [
                  logoWidgetSignIN("assets/images/Logo.jpg"),
                  const SizedBox(
                    height: 50,
                  ),
                  emailField(getTranslate(context, 'login.email_address'),
                      Icons.person, false, _emailTextController),
                  const SizedBox(
                    height: 30,
                  ),
                  PasswordField(getTranslate(context, 'signup.password'),
                      Icons.lock, _passwordTextController),
                  const SizedBox(
                    height: 6,
                  ),
                  forgotText(),
                  const SizedBox(
                    height: 30,
                  ),
                  signInButton(context, () {
                    processLoginData(context);
                  }),
                  const SizedBox(
                    height: 10,
                  ),
                  SignUpOption()
                ],
              ),
            )),
      ),
    ));
  }

  Image logoWidgetSignIN(String imageName) {
    return Image.asset(
      imageName,
      fit: BoxFit.fitWidth,
      width: 270,
      height: 300,
    );
  }

  TextFormField emailField(String text, IconData icon, bool isPasswordType,
      TextEditingController controller) {
    return TextFormField(
      controller: controller,
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
        if (value!.isEmpty ||
            !RegExp(r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$')
                .hasMatch(value!)) {
          return getTranslate(context, 'signup.CE');
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
          hintText: '8 character long',
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
      /*validator: (value) {
          return getTranslate(context, 'signup.CP');
      },*/
    );
  }

  forgotText() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 25),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          GestureDetector(
            child: Text(
              getTranslate(context, 'login.forget'),
              style: TextStyle(
                  color: Color.fromARGB(217, 0, 29, 103),
                  fontWeight: FontWeight.bold),
            ),
            onTap: () {
              Navigator.push(
                  context, MaterialPageRoute(builder: (context) => Forget()));
            },
          )
        ],
      ),
    );
  }

  Row SignUpOption() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          getTranslate(context, "login.account"),
          style: TextStyle(color: Color.fromARGB(217, 0, 29, 103)),
        ),
        GestureDetector(
            onTap: () {
              Navigator.push(
                  context, MaterialPageRoute(builder: (context) => SignUp()));
            },
            child: Text(
              getTranslate(context, 'login.up'),
              style: TextStyle(
                  color: Color.fromARGB(217, 0, 29, 103),
                  fontWeight: FontWeight.bold),
            ))
      ],
    );
  }

  Container signInButton(BuildContext context, Function onTap) {
    return Container(
        width: MediaQuery.of(context).size.width,
        height: 50,
        margin: const EdgeInsets.fromLTRB(0, 10, 0, 20),
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(70)),
        child: ElevatedButton(
          onPressed: () {
            if (formkey.currentState!.validate()) {
              onTap();
            }
          },
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
          child: Text(
            getTranslate(context, 'login.login'),
            style: const TextStyle(
                color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
          ),
        ));
  }

  Future<void> processLoginData(BuildContext context) async {
    ModelsUsers()
        .userLoginModel(_emailTextController.text, _passwordTextController.text)
        .then((login) {
      _myEmail.myVariable = _emailTextController.text;
      if (login.toString().contains('not')) {
        setState(() {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              backgroundColor: Colors.white,
              elevation: 10.0,
              shape: Border.all(
                  color: Colors.red, width: 0.5, style: BorderStyle.solid),
              content: Text(
                getTranslate(context, 'login.email_not'),
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 16.0,
                  fontWeight: FontWeight.bold,
                  fontStyle: FontStyle.italic,
                  letterSpacing: 1.0,
                ),
                textAlign: TextAlign.center,
              ),
            ),
          );
          _emailTextController.clear();
          _passwordTextController.clear();
          Timer(Duration(seconds: 3), () {
            Navigator.pushNamed(context, '/signin');
          });
        });
      } else if (login.toString().contains('ok')) {
        Timer(Duration(seconds: 3), () {
          Navigator.of(context).pushReplacementNamed('/bottomNavi');
        });
      }
    });
  }
}
