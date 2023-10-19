import 'package:businessgate/models/model_user.dart';
import 'package:flutter/material.dart';

import '../../globals.dart';
import '../../utils/colors.dart';

class EditProfile extends StatefulWidget {
  const EditProfile({super.key});

  @override
  State<EditProfile> createState() => _EditProfileState();
}

class _EditProfileState extends State<EditProfile> {

  
  TextEditingController nameController = TextEditingController();
  TextEditingController emailController = TextEditingController();
  TextEditingController phoneController = TextEditingController();
  TextEditingController passwordController = TextEditingController();

  @override
  void initState() {
    super.initState();
    nameController.text = '';
    emailController.text = '';
    phoneController.text = '';
    passwordController.text = '';
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return Scaffold(
      backgroundColor: hexStringColor("#6FBCF6"),
      appBar: AppBar(
        centerTitle: false,
        leading: IconButton(
          icon: const Icon(
            Icons.arrow_back_ios,
            size: 22,
          ),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        titleSpacing: 0,
        title: Text(
          "Edit Profile",
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
      body: ListView(
        children: [
          SizedBox(height: 10),
          SizedBox(height: 10),
          SizedBox(height: 10 / 2),
          profileContainer(size),
          SizedBox(height: 10),
          userinfo(),
          SizedBox(height: 10),
          SizedBox(height: 10 / 2),
          nameField(size, context),
          emailField(size, context),
          phoneField(size, context),
          passField(size, context),
          SizedBox(height: size.height * 0.05),
          updateButton(size,nameController.text,emailController.text,phoneController.text,passwordController.text),
        ],
      ),
    );
  }

  updateButton(Size size,String fname,String lname,String phone, String pass ) {
    return Center(
      child: GestureDetector(
        onTap: () {
          ModelsUsers().updatefname(myGlobalEmail, fname);
          ModelsUsers().updatelname(myGlobalEmail, lname);
          ModelsUsers().updatephonenum(myGlobalEmail, phone);
          ModelsUsers().updatepass(myGlobalEmail, pass);
        },
        child: Container(
          alignment: Alignment.center,
          height: size.height * 0.068,
          width: size.width * 0.65,
          decoration: BoxDecoration(
            color: Color(0xffE6482C),
            borderRadius: BorderRadius.circular(10),
            boxShadow: [
              BoxShadow(
                color: Color(0xffE6482C).withOpacity(0.3),
                blurRadius: 5,
              ),
            ],
          ),
          child: Text(
            "Update",
            style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
          ),
        ),
      ),
    );
  }

  nameField(Size size, BuildContext context) {
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.symmetric(
        horizontal: 10 * 2,
        vertical: 10,
      ),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(color: Colors.grey.withOpacity(0.5), blurRadius: 5),
        ],
      ),
      child: Theme(
        data: Theme.of(context).copyWith(
          colorScheme: const ColorScheme.light(primary: Color(0xffE6482C)),
        ),
        child: TextField(
          controller: nameController,
          keyboardType: TextInputType.name,
          style: const TextStyle(
            fontSize: 15.5,
          ),
          decoration: InputDecoration(
            border: InputBorder.none,
            errorBorder: OutlineInputBorder(
                borderSide: BorderSide.none,
                borderRadius: BorderRadius.circular(10)),
            focusedBorder: OutlineInputBorder(
              borderSide: const BorderSide(
                color: Color(0xffE6482C),
              ),
              borderRadius: BorderRadius.circular(10),
            ),
            hintText: "Edit First Name",
            hintStyle: TextStyle(fontSize: 16, color: Colors.grey, fontWeight: FontWeight.w600).copyWith(height: 0.5),
            prefixIcon: const Icon(
              Icons.person_outline,
              size: 17,
            ),
          ),
        ),
      ),
    );
  }

  emailField(Size size, BuildContext context) {
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.symmetric(
        horizontal: 10 * 2,
        vertical: 10,
      ),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(color: Colors.grey.withOpacity(0.5), blurRadius: 5),
        ],
      ),
      child: Theme(
        data: Theme.of(context).copyWith(
          colorScheme: const ColorScheme.light(primary: Color(0xffE6482C)),
        ),
        child: TextField(
          controller: emailController,
          style: const TextStyle(fontSize: 15.5),
          keyboardType: TextInputType.emailAddress,
          decoration: InputDecoration(
            border: InputBorder.none,
            errorBorder: OutlineInputBorder(
                borderSide: BorderSide.none,
                borderRadius: BorderRadius.circular(10)),
            focusedBorder: OutlineInputBorder(
              borderSide: const BorderSide(
                color: Color(0xffE6482C),
              ),
              borderRadius: BorderRadius.circular(10),
            ),
            hintText: "Edit Last Name",
            hintStyle: TextStyle(fontSize: 14, color: Colors.grey).copyWith(height: 0.5),
            prefixIcon: const Icon(
              Icons.mail_outline,
              size: 16,
            ),
          ),
        ),
      ),
    );
  }

  phoneField(Size size, BuildContext context) {
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.symmetric(
        horizontal: 10 * 2,
        vertical: 10,
      ),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(color: Colors.grey.withOpacity(0.5), blurRadius: 5),
        ],
      ),
      child: Theme(
        data: Theme.of(context).copyWith(
          colorScheme: const ColorScheme.light(primary: Color(0xffE6482C)),
        ),
        child: TextField(
          controller: phoneController,
          style: const TextStyle(fontSize: 15.5),
          keyboardType: TextInputType.phone,
          decoration: InputDecoration(
            border: InputBorder.none,
            errorBorder: OutlineInputBorder(
                borderSide: BorderSide.none,
                borderRadius: BorderRadius.circular(10)),
            focusedBorder: OutlineInputBorder(
              borderSide: const BorderSide(
                color: Color(0xffE6482C),
              ),
              borderRadius: BorderRadius.circular(10),
            ),
            hintText: "Edit Phone Number",
            hintStyle: TextStyle(fontSize: 14, color: Colors.grey).copyWith(height: 0.5),
            prefixIcon: const Icon(
              Icons.mail_outline,
              size: 16,
            ),
          ),
        ),
      ),
    );
  }

  passField(Size size, BuildContext context) {
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.symmetric(
        horizontal: 10 * 2,
        vertical: 10,
      ),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(color: Colors.grey.withOpacity(0.5), blurRadius: 5),
        ],
      ),
      child: Theme(
        data: Theme.of(context).copyWith(
          colorScheme: const ColorScheme.light(primary: Color(0xffE6482C)),
        ),
        child: TextField(
          controller: nameController,
          keyboardType: TextInputType.name,
          style: const TextStyle(
            fontSize: 15.5,
          ),
          decoration: InputDecoration(
            border: InputBorder.none,
            errorBorder: OutlineInputBorder(
                borderSide: BorderSide.none,
                borderRadius: BorderRadius.circular(10)),
            focusedBorder: OutlineInputBorder(
              borderSide: const BorderSide(
                color: Color(0xffE6482C),
              ),
              borderRadius: BorderRadius.circular(10),
            ),
            hintText: "Edit New Password",
            hintStyle: TextStyle(fontSize: 16, color: Colors.grey, fontWeight: FontWeight.w600).copyWith(height: 0.5),
            prefixIcon: const Icon(
              Icons.person_outline,
              size: 17,
            ),
          ),
        ),
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
        myGlobalEmail,
        style: TextStyle(fontSize: 14, color: Colors.grey),
      )
    ],
  );
}

String myGlobalEmail = Globals.globalEmailString;


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
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(100),
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(100),
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