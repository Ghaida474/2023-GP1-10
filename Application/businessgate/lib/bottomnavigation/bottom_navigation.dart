import 'dart:io';
import 'package:businessgate/localization/localization_const.dart';
import 'package:businessgate/myCourses.dart';
import 'package:businessgate/profile.dart';
import 'package:businessgate/theme.dart';
import 'package:flutter/material.dart';
import 'package:businessgate/screens/home.dart';

class BottomNaviScreen extends StatefulWidget {
  const BottomNaviScreen({Key? key}) : super(key: key);

  @override
  State<BottomNaviScreen> createState() => _BottomNaviScreenState();
}

class _BottomNaviScreenState extends State<BottomNaviScreen> {
  int selectedIndex = 0;

  List bodyItems = [
    const Home(),
    myCoursesNavigationMenu(),
    Profile()
  ];

  final Shader linearGradient = const LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.topRight,
    colors: gradient,
  ).createShader(const Rect.fromLTRB(10, 0, 50, 0));

  final Shader linearGradient2 = const LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.topRight,
    colors: <Color>[greyb7Color, greyb7Color],
  ).createShader(const Rect.fromLTRB(10, 0, 50, 0));

  DateTime? backpressTime;

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return WillPopScope(
      onWillPop: () async {
        bool backStatus = onWillPop();
        if (backStatus) {
          exit(0);
        } else {
          return false;
        }
      },
      child: Scaffold(
        drawerEnableOpenDragGesture: false,
        endDrawerEnableOpenDragGesture: false,
        backgroundColor: Color.fromARGB(255, 208, 231, 249),
        body: bodyItems.elementAt(selectedIndex),
        bottomNavigationBar: Container(
          height: size.height * 0.085,
          width: double.infinity,
          decoration: BoxDecoration(
              color: Color.fromARGB(255, 209, 231, 248),
              boxShadow: [
                BoxShadow(
                  color: grey94Color.withOpacity(0.4),
                  blurRadius: 4,
                )
              ]),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              firstItem(size),
              thirdItem(size),
              fiveItem(size),
            ],
          ),
        ),
      ),
    );
  }


  fiveItem(Size size) {
    return GestureDetector(
      onTap: () {
        setState(() {
          selectedIndex = 2;
        });
      },
      child: SizedBox(
        height: size.height * 0.085,
        width: size.width / 5,
        child: Column(
          children: [
            Container(
              height: 2,
              width: double.maxFinite,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: selectedIndex == 2
                      ? gradient
                      : [Colors.transparent, Colors.transparent],
                  begin: Alignment.topLeft,
                  end: Alignment.topRight,
                ),
              ),
            ),
            Expanded(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ShaderMask(
                      shaderCallback: (Rect bounds) {
                        return LinearGradient(
                                begin: Alignment.topCenter,
                                end: Alignment.bottomRight,
                                colors: selectedIndex == 2
                                    ? gradient
                                    : <Color>[
                                        Color.fromARGB(255, 189, 29, 29),
                                        Color.fromARGB(255, 72, 196, 124),
                                      ])
                            .createShader(bounds);
                      },
                      child: Container(
                        height: 26,
                        width: 26,
                        padding: const EdgeInsets.all(fixPadding / 5),
                        child: Image.asset(
                          "assets/profile/Shopicons_Filled_Account.png",
                          color: Color.fromARGB(255, 31, 30, 30),
                          fit: BoxFit.cover,
                        ),
                      )),
                  Text(
                    getTranslate(context, 'bottom_navi.profile'),
                    style: TextStyle(
                      foreground: Paint()
                        ..shader = selectedIndex == 2
                            ? linearGradient
                            : linearGradient2,
                    ),
                  )
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  thirdItem(Size size) {
    return GestureDetector(
      onTap: () {
        setState(() {
          selectedIndex = 1;
        });
      },
      child: SizedBox(
        height: size.height * 0.085,
        width: size.width / 5,
        child: Column(
          children: [
            Container(
              height: 2,
              width: double.maxFinite,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: selectedIndex == 1
                      ? gradient
                      : [Colors.transparent, Colors.transparent],
                  begin: Alignment.topLeft,
                  end: Alignment.topRight,
                ),
              ),
            ),
            Expanded(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ShaderMask(
                    shaderCallback: (Rect bounds) {
                      return LinearGradient(
                              begin: Alignment.topCenter,
                              end: Alignment.bottomRight,
                              colors: selectedIndex == 1
                                  ? gradient
                                  : <Color>[
                                      Color.fromARGB(255, 31, 30, 30),
                                      Color.fromARGB(255, 31, 30, 30),
                                    ])
                          .createShader(bounds);
                    },
                    child: const Icon(
                      Icons.play_arrow_sharp,
                      size: 26,
                      color: Color.fromARGB(255, 31, 30, 30),
                    ),
                  ),
                  Text(
                    getTranslate(context, 'bottom_navi.courses'),
                    style: TextStyle(
                      foreground: Paint()
                        ..shader = selectedIndex == 1
                            ? const LinearGradient(
                                begin: Alignment.topLeft,
                                end: Alignment.topRight,
                                colors: gradient,
                              ).createShader(
                                const Rect.fromLTRB(180, 0, 220, 0))
                            : linearGradient2,
                    ),
                  )
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  firstItem(Size size) {
    return GestureDetector(
      onTap: () {
        setState(() {
          selectedIndex = 0;
        });
      },
      child: SizedBox(
        height: size.height * 0.085,
        width: size.width / 5,
        child: Column(
          children: [
            Container(
              height: 2,
              width: double.maxFinite,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: selectedIndex == 0
                      ? gradient
                      : [Colors.transparent, Colors.transparent],
                  begin: Alignment.topLeft,
                  end: Alignment.topRight,
                ),
              ),
            ),
            Expanded(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ShaderMask(
                    shaderCallback: (Rect bounds) {
                      return LinearGradient(
                              begin: Alignment.topCenter,
                              end: Alignment.bottomRight,
                              colors: selectedIndex == 0
                                  ? gradient
                                  : <Color>[
                                      Color.fromARGB(255, 31, 30, 30),
                                      Color.fromARGB(255, 31, 30, 30),
                                    ])
                          .createShader(bounds);
                    },
                    child: const Icon(
                      Icons.home_rounded,
                      size: 26,
                      color: Color.fromARGB(255, 31, 30, 30), 
                    ),
                  ),
                  Text(
                    getTranslate(context, 'bottom_navi.home'),
                    style: TextStyle(
                      foreground: Paint()
                        ..shader = selectedIndex == 0
                            ? linearGradient
                            : linearGradient2,
                    ),
                  )
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  onWillPop() {
    DateTime now = DateTime.now();

    if (backpressTime == null ||
        now.difference(backpressTime!) > const Duration(seconds: 2)) {
      backpressTime = now;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
            backgroundColor: blackColor,
            content: Text(
              getTranslate(context, 'app_exit.exit_app'),
              style: white14Style,
            ),
            duration: const Duration(milliseconds: 1500),
            behavior: SnackBarBehavior.floating),
      );
      return false;
    } else {
      return true;
    }
  }
}
