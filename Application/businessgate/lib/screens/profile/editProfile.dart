import 'package:businessgate/models/model_user.dart';
import 'package:flutter/material.dart';

import '../../myservice.dart';
import '../../utils/colors.dart';

class EditProfile extends StatefulWidget {
  const EditProfile({super.key});

  @override
  State<EditProfile> createState() => _EditProfileState();
}

class _EditProfileState extends State<EditProfile> {

  MyService _myEmail = MyService();

  TextEditingController nameController = TextEditingController();
  TextEditingController lastNameController = TextEditingController();
  TextEditingController phoneController = TextEditingController();
  TextEditingController passwordController = TextEditingController();

  @override
  void initState() {
    super.initState();
    nameController.text = ModelsUsers().FetchFirstName(_myEmail.myVariable).toString();
    lastNameController.text = ModelsUsers().FetchLastName(_myEmail.myVariable).toString();
    phoneController.text = ModelsUsers().FetchPhoneNum(_myEmail.myVariable).toString();
    passwordController.text = ModelsUsers().FetchPassword(_myEmail.myVariable).toString();
  }

    @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text(
          "Edit Profile",
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              hexStringColor("#6FBCF6"),
              hexStringColor("#E3E0D2"),
            ],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SingleChildScrollView(
          child: Padding(
            padding: EdgeInsets.fromLTRB(20, size.height * 0.2, 20, 400),
            child: Column(
              children: <Widget>[
                SizedBox(height: 10),
                SizedBox(height: 10),
                SizedBox(height: 10 / 2),
                profileContainer(size),
                SizedBox(height: 10),
                userinfo(),
                SizedBox(height: 10),
                SizedBox(height: 10 / 2),
                nameField(size, context),
                SizedBox(height: 8),
                emailField(size, context),
                SizedBox(height: 8),
                phoneField(size, context),
                SizedBox(height: 8),
                passField(size, context),
                SizedBox(height: size.height * 0.05),
                updateButton(
                    size,
                    nameController.text,
                    lastNameController.text,
                    phoneController.text,
                    passwordController.text),
              ],
            ),
          ),
        ),
      ),
    );
  }

  updateButton(Size size,String fname,String lname,String phone, String pass ) {
    return Center(
      child: GestureDetector(
        onTap: () {
          ModelsUsers().updatefname(_myEmail.myVariable, fname);
          ModelsUsers().updatelname(_myEmail.myVariable, lname);
          ModelsUsers().updatephonenum(_myEmail.myVariable, phone);
          ModelsUsers().updatepass(_myEmail.myVariable, pass);
        },
        child: Container(
          alignment: Alignment.center,
          height: 50,
          width:  MediaQuery.of(context).size.width,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(70),
            color: hexStringColor("#095590"),
          ),
          child: Text(
            "Update",
            style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
          ),
        ),
      ),
    );
  }

  nameField(Size size, BuildContext context) {
    return TextField(controller: nameController,
    cursorColor: Colors.white,
    style: TextStyle(color: Colors.white.withOpacity(0.9)),
    decoration: InputDecoration(
      focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(30),
                borderSide: const BorderSide(
                  color: Color.fromARGB(255, 2, 14, 52),
                )),
      prefixIcon: Icon(
        Icons.person,
        color: const Color.fromARGB(179, 255, 255, 255),
      ),
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

  emailField(Size size, BuildContext context) {
    return TextField(controller: lastNameController,
    cursorColor: Colors.white,
    style: TextStyle(color: Colors.white.withOpacity(0.9)),
    decoration: InputDecoration(
      focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(30),
                borderSide: const BorderSide(
                  color: Color.fromARGB(255, 2, 14, 52),
                )),
      prefixIcon: Icon(
        Icons.person,
        color: const Color.fromARGB(179, 255, 255, 255),
      ),
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

  phoneField(Size size, BuildContext context) {
    return TextField(controller: phoneController,
    cursorColor: Colors.white,
    style: TextStyle(color: Colors.white.withOpacity(0.9)),
    decoration: InputDecoration(
      focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(30),
                borderSide: const BorderSide(
                  color: Color.fromARGB(255, 2, 14, 52),
                )),
      prefixIcon: Icon(
        Icons.person,
        color: const Color.fromARGB(179, 255, 255, 255),
      ),
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

  passField(Size size, BuildContext context) {
    return TextField(controller: passwordController,
    cursorColor: Colors.white,
    style: TextStyle(color: Colors.white.withOpacity(0.9)),
    decoration: InputDecoration(
      focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(30),
                borderSide: const BorderSide(
                  color: Color.fromARGB(255, 2, 14, 52),
                )),
      prefixIcon: Icon(
        Icons.person,
        color: const Color.fromARGB(179, 255, 255, 255),
      ),
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

  

  userinfo() {
  return Column(
    children: [
      Text(
        "Edit User Name",
        style: TextStyle(color: Colors.black, fontSize: 18, fontWeight: FontWeight.w600),
      ),
      SizedBox(height: 10 / 2),
      Text(
        _myEmail.myVariable,
        style: TextStyle(fontSize: 14, color: Colors.black),
      )
    ],
  );
}



  profileContainer(Size size) {
    return Center(
      child: SizedBox(
        height: size.height * 0.155,
        width: size.height * 0.15,
        child: Stack(
          children: [
            Container(
              height: size.height * 0.15,
              width: size.height * 0.15,
              child: ClipRRect(
                child: Image.asset(
                  "assets/images/Profile.png",
                  fit: BoxFit.cover,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  bottonsheetIcon(Size size, IconData icon, Color color, String text) {
    return GestureDetector(
      onTap: () {
        Navigator.pop(context);
      },
      child: Column(
        children: [
          Container(
            height: size.height * 0.07,
            width: size.height * 0.07,
            decoration: BoxDecoration(
              color: Colors.white,
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: Colors.grey.withOpacity(0.3),
                  blurRadius: 10,
                ),
              ],
            ),
            child: Icon(
              icon,
              color: color,
            ),
          ),
          SizedBox(height: 10 / 2),
          Text(text.toString(),
              style: TextStyle(color: Colors.black, fontSize: 16, fontWeight: FontWeight.w400).copyWith(fontSize: 15),
              textAlign: TextAlign.center)
        ],
      ),
    );
  }
}