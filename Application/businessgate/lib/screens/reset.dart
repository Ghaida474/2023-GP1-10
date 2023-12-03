import 'dart:async';
import 'package:businessgate/models/model_user.dart';
import 'package:flutter/material.dart';
import 'package:flutter_pw_validator/flutter_pw_validator.dart';
import '../localization/localization_const.dart';
import '../myservice.dart';
import '../utils/colors.dart';
import 'package:email_otp/email_otp.dart';


class Reset extends StatefulWidget {
  const Reset({super.key});

  @override
  State<Reset> createState() => _ResetState();
}

class _ResetState extends State<Reset> {
  final formkey = GlobalKey<FormState>();

  TextEditingController _otpTextController = TextEditingController();
  TextEditingController _passwordTextController = TextEditingController();
  TextEditingController _confirmPasswordTextController = TextEditingController();

  bool success = false;

  bool passToggle = true;

  @override
  Widget build(BuildContext context) {
    final EmailOTP auth =
        ModalRoute.of(context)!.settings.arguments as EmailOTP;

    return Scaffold(
        extendBodyBehindAppBar: true,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          title: Text(
            getTranslate(context, 'otp.reset'),
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
        ),
        body: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
                colors: [hexStringColor("#6FBCF6"), hexStringColor("##E3E0D2")],
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter),
          ),
          child: SingleChildScrollView(
            child: Padding(
                padding: EdgeInsets.fromLTRB(
                    70, MediaQuery.of(context).size.height * 0.18, 70, 400),
                child: Form(
                  key: formkey,
                  child: Column(
                    children: [
                      logoWidget("assets/images/Logo.jpg"),
                      const SizedBox(
                        height: 40,
                      ),
                      textField(getTranslate(context, 'otp.otp_num'),
                          Icons.person, false, _otpTextController),
                      const SizedBox(
                        height: 20,
                      ),
                      PasswordField(getTranslate(context, 'signup.password'),
                        Icons.lock, _passwordTextController),
                    const SizedBox(
                      height: 5,
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
                      height: 20,
                    ),
                      ResetButton(context, () {
                        PasswordReset(auth);
                      })
                    ],
                  ),
                )),
          ),
        ));
  }

  Image logoWidget(String imageName) {
    return Image.asset(
      imageName,
      fit: BoxFit.fitWidth,
      width: 270,
      height: 300,
    );
  }

  TextField textField(String text, IconData icon, bool isPasswordType,
      TextEditingController controller) {
    return TextField(
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
        if (_confirmPasswordTextController.text != _passwordTextController.text) {
          return getTranslate(context, 'signup.CconfirmP');
        }else
          return null;
      },
    );
  }

  Container ResetButton(BuildContext context, Function onTap) {
    return Container(
        width: MediaQuery.of(context).size.width,
        height: 50,
        margin: const EdgeInsets.fromLTRB(0, 10, 0, 20),
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(70)),
        child: ElevatedButton(
          onPressed: () {
            onTap();
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
            getTranslate(context, 'otp.reset_pass'),
            style: const TextStyle(
                color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
          ),
        ));
  }

  MyService _myEmail = MyService();

  Future<void> PasswordReset(EmailOTP myauth) async {
    var inputOTP = _otpTextController.text;
    await myauth.verifyOTP(otp: inputOTP);

    ModelsUsers()
        .updatePassword(_myEmail.myVariable, _passwordTextController.text)
        .then((Update) {
      if (Update.toString().contains('not')) {
        setState(() {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              backgroundColor: hexStringColor("##E3E0D2"),
              elevation: 10.0,
              shape: Border.all(
                  color: Colors.red, width: 0.5, style: BorderStyle.solid),
              content: Text(
                getTranslate(context, 'otp.not_suc'),
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
          _otpTextController.clear();
          _passwordTextController.clear();

            Navigator.pushNamed(context, '/signin');
        });
      } else if (Update.toString().contains('ok')) {

          Navigator.pushNamed(context, '/signin');
      }
    });
  }
}
