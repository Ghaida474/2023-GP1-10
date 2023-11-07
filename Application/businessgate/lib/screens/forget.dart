import 'package:businessgate/screens/reset.dart';
import 'package:flutter/material.dart';

import '../localization/localization_const.dart';
import '../myservice.dart';
import '../utils/colors.dart';

import 'package:email_otp/email_otp.dart';

class Forget extends StatefulWidget {
  const Forget({super.key});

  @override
  State<Forget> createState() => _ForgetState();
}

class _ForgetState extends State<Forget> {

  TextEditingController _emailTextController = TextEditingController() ;

  MyService _myEmail = MyService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
      backgroundColor: Colors.transparent,
      elevation: 0,
      title:  Text(getTranslate(context, 'otp.forgot'),
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
                  Text(getTranslate(context, 'otp.enter_email'),
                  style: TextStyle(color: Color.fromARGB(217, 0, 29, 103),
                  fontWeight: FontWeight.bold),),
                  const SizedBox(
                    height: 20,
                  ),
                  textField(getTranslate(context, 'login.email_address'), Icons.person, false, _emailTextController),
                  const SizedBox(
                    height: 20,
                  ),
                  MaterialButton(
                  onPressed: () async{ 
                    _myEmail.myVariable = _emailTextController.text ;
                    EmailOTP myauth = EmailOTP();
        myauth.setConfig(
        appEmail: "businessgate@gmail.com",
        appName: "Business Gate OTP",
        userEmail: _emailTextController.text,
        otpLength: 6,
        otpType: OTPType.digitsOnly
        );

        await myauth.sendOTP();

                    Navigator.push(context, MaterialPageRoute(
                      builder: (context) => Reset(),
                  settings: RouteSettings(arguments: myauth ))); },
                  child: Text(getTranslate(context, 'otp.send_otp'),
                  style: TextStyle(color: Colors.white),),
                  color: hexStringColor("#095590"),
                  minWidth: 200,
                  height: 50
                  ,)
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

}