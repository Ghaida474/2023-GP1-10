import 'dart:async';

import 'package:businessgate/models/model_user.dart';
import 'package:flutter/material.dart';

import '../utils/colors.dart';

import 'package:email_otp/email_otp.dart';

import 'package:businessgate/screens/forget.dart';

class Reset extends StatefulWidget {
  const Reset({super.key});

  @override
  State<Reset> createState() => _ResetState();
}

class _ResetState extends State<Reset> {

  TextEditingController _otpTextController = TextEditingController() ;
  TextEditingController _emailTextController = TextEditingController() ;
  TextEditingController _passwordTextController = TextEditingController() ;

  @override
  Widget build(BuildContext context) {

    final EmailOTP auth = ModalRoute.of(context)!.settings.arguments as EmailOTP;

    return Scaffold(
      appBar: AppBar(
      backgroundColor: Colors.transparent,
      elevation: 0,
      title: const Text("Reset Password", 
      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),),
    ),
      body: Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
          hexStringColor("#6FBCF6"), 
          hexStringColor("##E3E0D2")
          ], begin: Alignment.topCenter, 
          end: Alignment.bottomCenter ),
          ),
          child: SingleChildScrollView(
            child: Padding(
              padding: EdgeInsets.fromLTRB(
                70, MediaQuery.of(context).size.height * 0.18, 70, 400),
              child: Column(
                children: [ 
                  logoWidget("assets/images/Logo.jpg"),
                  const SizedBox(
                    height: 40,
                  ),
                  textField("Enter Your OTP", Icons.person, false, _otpTextController),
                  const SizedBox(
                    height: 10,
                  ),
                  textField("Enter Your Email", Icons.person, false, _emailTextController),
                  const SizedBox(
                    height: 10,
                  ),
                  PasswordField("Enter Your New Password", Icons.person, true, _passwordTextController),
                  const SizedBox(
                    height: 10,
                  ),
                  ResetButton(context, () {
                    PasswordReset(auth);
                  })
                ],
              ),)),
          ),
          );
  }

  Image logoWidget(String imageName) {
    return Image.asset(
      imageName,
      fit: BoxFit.fitWidth,
      width: 270,
      height: 300,
    );
  }

  TextField textField (String text, IconData icon, bool isPasswordType, 
  TextEditingController controller) {
    return TextField( controller: controller,
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
    );

  } 

  TextField PasswordField (String text, IconData icon, bool isPasswordType, 
  TextEditingController controller) {
    return TextField( controller: controller,
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
            hintText: 'The password must be of 8 character long',
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
     keyboardType: isPasswordType
      ? TextInputType.visiblePassword
      : TextInputType.none
    );

  }

  Container ResetButton (BuildContext context, Function onTap) {
    return Container(width: 100,
    height: 80,
    margin: const EdgeInsets.fromLTRB(0, 10, 0, 20),
    decoration: BoxDecoration(borderRadius: BorderRadius.circular(70)),
    child: ElevatedButton(onPressed: () { 
      onTap(); }, 
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
        child: Text ('Reset Password', 
      style: const TextStyle(
        color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
        ),
    )
    ); 

  }
  
  Future<void> PasswordReset(EmailOTP myauth) async {


        var inputOTP = _otpTextController.text; 
        await myauth.verifyOTP(
        otp: inputOTP
        );

            ModelsUsers()
          .updatePassword(
            _emailTextController.text, _passwordTextController.text)
          .then((Update) {
         if (Update.toString().contains('not')) {
          setState(() {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                backgroundColor: Colors.white,
                elevation: 10.0,
                shape: Border.all(
                    color: Colors.red, width: 0.5, style: BorderStyle.solid),
                content: Text(
                  "Reset is not Successfull",
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
            Timer(Duration(seconds: 2), () {
              Navigator.pushNamed(context, '/signin');
            });
          });
        } else if(Update.toString().contains('ok')){
          Timer(Duration(seconds: 2), () {
              Navigator.pushNamed(context, '/signin');
            });
        }
  });
    
  }
}