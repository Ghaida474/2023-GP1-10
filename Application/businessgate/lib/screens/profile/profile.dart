import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';

import '../../globals.dart';

class Profile extends StatefulWidget {
  const Profile({super.key});

  @override
  State<Profile> createState() => _ProfileState();
}

class _ProfileState extends State<Profile> {
  
  String myGlobalEmail = Globals.globalEmailString;
  
 @override
Widget build(BuildContext context) {
  final size = MediaQuery.of(context).size;
  return Scaffold(
    extendBodyBehindAppBar: true,
    appBar: AppBar(
      backgroundColor: Colors.transparent,
      elevation: 0,
      title: Text(
        'Profile',
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
          padding: EdgeInsets.fromLTRB(
            20, MediaQuery.of(context).size.height * 0.2, 20, 400),
          child: Column(
            children: <Widget>[
              heightbox(size.height * 0.03),
              profileinfo(size, context),
              heightbox(size.height * 0.03),
              profileList(size, context),
            ],
          ),
        ),
      ),
    ),
  );
}


  heightbox(double height) {
  return SizedBox(height: height);
}

widthbox(double width) {
  return SizedBox(width: width);
}

  profileList(Size size, BuildContext context) {
    return Container(
      height: size.height * 0.51,
      width: double.infinity,
      margin: const EdgeInsets.symmetric(horizontal: 10 * 2),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.5),
            blurRadius: 5,
          )
        ],
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          imageIconListTile(
            context,
            "assets/images/Profile.png",
            "Edit Profile",
            () {
              Navigator.pushNamed(context, '/editprofile');
            },
          ),
          devider(),
          profilelistTile(
            () {
              //Navigator.pushNamed(context, '/setting');
            },
            Icons.settings,
            Colors.black,
            "Certificates",
          ),
          devider(),
          profilelistTile(
            () {
              showDialog(
                barrierColor: Colors.black.withOpacity(0.3),
                context: context,
                builder: (context) {
                  return signoutDialog(context, size);
                },
              );
            },
            Icons.logout,
            Colors.blue,
            "Sign Out",
          )
        ],
      ),
    );
  }

  imageIconListTile(
      BuildContext context, String image, String title, Function() onTap) {
    return ListTile(
      onTap: onTap,
      leading: Image.asset(
        image,
        height: 22,
        width: 22,
      ),
      minLeadingWidth: 0,
      title: Text(
        title,
        style:  TextStyle(color: Colors.black, fontSize: 16, fontWeight: FontWeight.w600).copyWith(fontWeight: FontWeight.w500),
      ),
      trailing: const Icon(
        Icons.arrow_forward_ios,
        size: 18,
        color: Colors.black,
      ),
    );
  }

  signoutDialog(BuildContext context, Size size) {
    return AlertDialog(
      titlePadding: const EdgeInsets.all(10 * 3),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
      ),
      title: Column(
        children: [
          Text(
            "Siggn Out",
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black),
          ),
          SizedBox(height: 10),
          SizedBox(height: 10),
          SizedBox(height: 10),
          Row(
            children: [
              SizedBox(width: 10),
              Expanded(
                child: InkWell(
                  onTap: () {
                    Navigator.pop(context);
                  },
                  child: Container(
                    height: size.height * 0.065,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(10),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.grey.withOpacity(0.5),
                          blurRadius: 5,
                        )
                      ],
                    ),
                    alignment: Alignment.center,
                    child: Text(
                      "Cancel",
                      style: TextStyle(fontSize: 17, color: Colors.grey, fontWeight: FontWeight.w400),
                    ),
                  ),
                ),
              ),
              SizedBox(width: 10),
              SizedBox(width: 10),
              Expanded(
                child: InkWell(
                  onTap: () {
                    Navigator.pushReplacementNamed(context, '/signin');
                  },
                  child: Container(
                    height: size.height * 0.065,
                    decoration: BoxDecoration(
                      color: Color(0xffE6482C),
                      borderRadius: BorderRadius.circular(10),
                      boxShadow: [
                        BoxShadow(
                          color: Color(0xffE6482C).withOpacity(0.5),
                          blurRadius: 5,
                        )
                      ],
                    ),
                    alignment: Alignment.center,
                    child: Text(
                      "Sign Outt",
                      style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
              ),
              SizedBox(width: 10),
            ],
          )
        ],
      ),
    );
  }

  profilelistTile(Function() onTap, IconData icon, Color color, String title) {
    return ListTile(
      onTap: onTap,
      leading: Icon(
        icon,
        size: 22,
        color: color,
      ),
      minLeadingWidth: 0,
      title: Text(
        title,
        style: TextStyle(color: Colors.black, fontSize: 16, fontWeight: FontWeight.w600).copyWith(
            color: color, fontWeight: FontWeight.w500),
      ),
      trailing: const Icon(
        Icons.arrow_forward_ios,
        size: 18,
        color: Colors.black,
      ),
    );
  }

  devider() {
    return Container(
      height: 2,
      width: double.infinity,
      color: const Color(0xfff0f0f0),
    );
  }

  profileinfo(Size size, context) {
    return Column(
      children: [
        Text(
          "User Name",
          style: TextStyle(color: Colors.black, fontSize: 18, fontWeight: FontWeight.w600),
        ),
        heightbox(10 / 3),
      ],
    );
  }
}