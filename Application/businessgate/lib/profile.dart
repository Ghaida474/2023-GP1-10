import 'package:businessgate/localization/localization_const.dart';
import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';

import '../../myservice.dart';

class Profile extends StatelessWidget {
   Profile({Key? key}) : super(key: key);
  
 @override
Widget build(BuildContext context) {

  final size = MediaQuery.of(context).size;
  return Scaffold(
    extendBodyBehindAppBar: true,
    appBar: AppBar(
      backgroundColor: Colors.transparent,
      elevation: 0,
      title: Text(
        getTranslate(context, 'profile.profile'),
        style: const TextStyle(fontWeight: FontWeight.bold),
      ),
      automaticallyImplyLeading: false,
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
              ProfileWidget("assets/images/Profile.png"),
               SizedBox(height: 30),
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
  return SizedBox(height: height * 3);
}

widthbox(double width) {
  return SizedBox(width: width);
}

  profileList(Size size, BuildContext context) {
    return Container(
      height: 300,
      width: 400,
      margin: const EdgeInsets.symmetric(horizontal: 10 * 2),
      decoration: BoxDecoration(
        color: hexStringColor("#095590"),
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
            getTranslate(context, 'profile.edit_profile'),
            () {
              Navigator.pushNamed(context, '/editprofile');
            },
          ),
          devider(),
          imageIconListTile(
            context,
            "assets/profile/Shopicons_Filled_World.png",
            getTranslate(context, 'profile.languages'),
            () {
              Navigator.pushNamed(context, '/languages');
            },
          ),
          devider(),
          profilelistTile(
            () {},
            Icons.document_scanner,
            Colors.white,
            getTranslate(context, 'profile.certificates'),
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
            Color.fromARGB(255, 101, 215, 247),
            getTranslate(context, 'profile.logout'),
          )
        ],
      ),
    );
  }

  Image ProfileWidget(String imageName) {
    return Image.asset(
      imageName,
      color: hexStringColor("#095590"),
      fit: BoxFit.fitWidth,
      width: 100,
      height: 100,
    );
  }

  imageIconListTile(
      BuildContext context, String image, String title, Function() onTap) {
    return ListTile(
      onTap: onTap,
      leading: Image.asset(
        color: Colors.white ,
        image,
        height: 22,
        width: 22,
      ),
      minLeadingWidth: 0,
      title: Text(
        title,
        style:  TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600).copyWith(fontWeight: FontWeight.w500),
      ),
      trailing: const Icon(
        Icons.arrow_forward_ios,
        size: 18,
        color: Colors.white,
      ),
    );
  }

  signoutDialog(BuildContext context, Size size) {
    return AlertDialog(
      backgroundColor: Color.fromARGB(255, 162, 211, 246),
      titlePadding: const EdgeInsets.all(10 * 3),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
      ),
      title: Column(
        children: [
          Text(
            getTranslate(context, 'profile.logout_que'),
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black),
          ),
          SizedBox(height: 10),
          SizedBox(height: 10),
          SizedBox(height: 10),
          Row(
            children: [
              SizedBox(width: 0),
              Expanded(
                child: InkWell(
                  onTap: () {
                    Navigator.pop(context);
                  },
                  child: Container(
                    height: 30,
                    width: 30,
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
                      getTranslate(context, 'profile.cancel'),
                      style: TextStyle(fontSize: 17, color: Color.fromARGB(255, 107, 105, 105), fontWeight: FontWeight.w400),
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
                    height: 30,
                    width: 30,
                    decoration: BoxDecoration(
                      color: hexStringColor("#095590"),
                      borderRadius: BorderRadius.circular(10),
                      boxShadow: [
                        BoxShadow(
                          color: Color.fromARGB(255, 250, 0, 0).withOpacity(0.5),
                          blurRadius: 5,
                        )
                      ],
                    ),
                    alignment: Alignment.center,
                    child: Text(
                      getTranslate(context, 'profile.logout'),
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
        style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600).copyWith(
            color: color, fontWeight: FontWeight.w500),
      ),
      trailing: const Icon(
        Icons.arrow_forward_ios,
        size: 18,
        color: Colors.white,
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

  MyService _myEmail = MyService();

  profileinfo(Size size, context) {
    return Column(
      children: [
        Text(
          _myEmail.myVariable,
          style: TextStyle(color: Colors.black, fontSize: 20, fontWeight: FontWeight.w600),
        ),
        heightbox(10 / 3),
      ],
    );
  }
}