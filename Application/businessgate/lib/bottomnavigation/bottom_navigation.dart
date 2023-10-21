import 'dart:io';

import 'package:businessgate/localization/localization_const.dart';
import 'package:businessgate/profile/profile.dart';
import 'package:businessgate/theme.dart';
import 'package:flutter/material.dart';
import 'package:businessgate/home/home.dart';
//import 'package:businessgate/profile/editProfile.dart';
class BottomNaviScreen extends StatefulWidget {
  const BottomNaviScreen({Key? key}) : super(key: key);

  @override
  State<BottomNaviScreen> createState() => _BottomNaviScreenState();
}

class _BottomNaviScreenState extends State<BottomNaviScreen> {
  int selectedIndex = 0;

  int categoryIndex = 0;
  int priceIndex = 0;
  int levelIndex = 0;

  List bodyItems = [
    const HomeScreen(),
    const ProfileScreen()
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
        backgroundColor: whiteColor,
        endDrawer: drawer(size, context),
        body: bodyItems.elementAt(selectedIndex),
        bottomNavigationBar: Container(
          height: size.height * 0.085,
          width: double.infinity,
          decoration: BoxDecoration(color: whiteColor, boxShadow: [
            BoxShadow(
              color: grey94Color.withOpacity(0.4),
              blurRadius: 4,
            )
          ]),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              firstItem(size),
              fiveItem(size),
            ],
          ),
        ),
      ),
    );
  }

  drawer(Size size, BuildContext context) {
    return Drawer(
      width: size.width * 0.7,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          InkWell(
            onTap: () {
              Navigator.pop(context);
            },
            child: Container(
              height: size.height * 0.1,
              width: double.infinity,
              color: grey94Color.withOpacity(0.3),
              alignment: Alignment.center,
              child: Padding(
                padding: const EdgeInsets.only(top: fixPadding),
                child: Text(
                  getTranslate(context, 'bottom_navi.reset'),
                  style: primary18Style,
                ),
              ),
            ),
          ),
          Expanded(
            child: ListView(
              physics: const BouncingScrollPhysics(),
              children: [
                Padding(
                  padding: const EdgeInsets.symmetric(
                      horizontal: fixPadding * 2, vertical: fixPadding),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        getTranslate(context, 'bottom_navi.categories'),
                        style: black18Stylew600,
                      ),
                      height5Space,
                      categroyListTile(
                          size, 0, getTranslate(context, 'bottom_navi.design')),
                      categroyListTile(size, 1,
                          getTranslate(context, 'bottom_navi.marketing')),
                      categroyListTile(
                          size, 2, getTranslate(context, 'bottom_navi.helth')),
                      categroyListTile(
                          size, 3, getTranslate(context, 'bottom_navi.music')),
                      categroyListTile(size, 4,
                          getTranslate(context, 'bottom_navi.photography')),
                      categroyListTile(size, 5,
                          getTranslate(context, 'bottom_navi.programmimg')),
                      categroyListTile(
                          size, 6, getTranslate(context, 'bottom_navi.art')),
                      height5Space,
                      Text(
                        getTranslate(context, 'bottom_navi.price'),
                        style: black18Stylew600,
                      ),
                      height5Space,
                      priceListTile(
                          size, 0, getTranslate(context, 'bottom_navi.paid')),
                      priceListTile(
                          size, 1, getTranslate(context, 'bottom_navi.free')),
                      priceListTile(
                          size, 2, getTranslate(context, 'bottom_navi.both')),
                      height5Space,
                      Text(
                        getTranslate(context, 'bottom_navi.level'),
                        style: black18Stylew600,
                      ),
                      height5Space,
                      levelListTile(size, 0,
                          getTranslate(context, 'bottom_navi.all_level')),
                      levelListTile(size, 1,
                          getTranslate(context, 'bottom_navi.beginner')),
                      levelListTile(size, 2,
                          getTranslate(context, 'bottom_navi.intermediate')),
                      levelListTile(size, 3,
                          getTranslate(context, 'bottom_navi.advance')),
                      levelListTile(
                          size, 4, getTranslate(context, 'bottom_navi.other')),
                    ],
                  ),
                ),
              ],
            ),
          ),
          GestureDetector(
            onTap: () {
              Navigator.pop(context);
            },
            child: Container(
              height: size.height * 0.07,
              width: double.infinity,
              decoration: const BoxDecoration(
                color: primaryColor,
              ),
              alignment: Alignment.center,
              child: Text(
                getTranslate(context, 'bottom_navi.filter'),
                style: white18Style,
              ),
            ),
          ),
        ],
      ),
    );
  }

  levelListTile(Size size, int index, String text) {
    return GestureDetector(
      onTap: () {
        setState(() {
          levelIndex = index;
        });
      },
      child: Padding(
        padding: const EdgeInsets.symmetric(
            horizontal: fixPadding, vertical: fixPadding / 2),
        child: Row(
          children: [
            levelIndex == index
                ? Container(
                    height: size.height * 0.028,
                    width: size.height * 0.028,
                    padding: const EdgeInsets.all(fixPadding / 1.7),
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        colors: gradient,
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      shape: BoxShape.circle,
                    ),
                    child: Container(
                      decoration: const BoxDecoration(
                        color: whiteColor,
                        shape: BoxShape.circle,
                      ),
                    ),
                  )
                : Container(
                    height: size.height * 0.028,
                    width: size.height * 0.028,
                    padding: const EdgeInsets.all(fixPadding / 1.7),
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: greyb7Color),
                    ),
                  ),
            widthbox(fixPadding * 2),
            Text(
              text,
              style: black16Stylew400,
            ),
          ],
        ),
      ),
    );
  }

  priceListTile(Size size, int index, String text) {
    return GestureDetector(
      onTap: () {
        setState(() {
          priceIndex = index;
        });
      },
      child: Padding(
        padding: const EdgeInsets.symmetric(
            horizontal: fixPadding, vertical: fixPadding / 2),
        child: Row(
          children: [
            priceIndex == index
                ? Container(
                    height: size.height * 0.028,
                    width: size.height * 0.028,
                    padding: const EdgeInsets.all(fixPadding / 1.7),
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        colors: gradient,
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      shape: BoxShape.circle,
                    ),
                    child: Container(
                      decoration: const BoxDecoration(
                        color: whiteColor,
                        shape: BoxShape.circle,
                      ),
                    ),
                  )
                : Container(
                    height: size.height * 0.028,
                    width: size.height * 0.028,
                    padding: const EdgeInsets.all(fixPadding / 1.7),
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: greyb7Color),
                    ),
                  ),
            widthbox(fixPadding * 2),
            Text(
              text,
              style: black16Stylew400,
            ),
          ],
        ),
      ),
    );
  }

  categroyListTile(Size size, int index, String text) {
    return GestureDetector(
      onTap: () {
        setState(() {
          categoryIndex = index;
        });
      },
      child: Padding(
        padding: const EdgeInsets.symmetric(
            horizontal: fixPadding, vertical: fixPadding / 2),
        child: Row(
          children: [
            categoryIndex == index
                ? Container(
                    height: size.height * 0.028,
                    width: size.height * 0.028,
                    padding: const EdgeInsets.all(fixPadding / 1.7),
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        colors: gradient,
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      shape: BoxShape.circle,
                    ),
                    child: Container(
                      decoration: const BoxDecoration(
                        color: whiteColor,
                        shape: BoxShape.circle,
                      ),
                    ),
                  )
                : Container(
                    height: size.height * 0.028,
                    width: size.height * 0.028,
                    padding: const EdgeInsets.all(fixPadding / 1.7),
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: greyb7Color),
                    ),
                  ),
            widthbox(fixPadding * 2),
            Text(
              text,
              style: black16Stylew400,
            ),
          ],
        ),
      ),
    );
  }

  fiveItem(Size size) {
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
                  colors: selectedIndex == 4
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
                                colors: selectedIndex == 4
                                    ? gradient
                                    : <Color>[
                                        greyb7Color,
                                        greyb7Color,
                                      ])
                            .createShader(bounds);
                      },
                      child: Container(
                        height: 26,
                        width: 26,
                        padding: const EdgeInsets.all(fixPadding / 5),
                        child: Image.asset(
                          "assets/profile/Shopicons_Filled_Account.png",
                          color: whiteColor,
                          fit: BoxFit.cover,
                        ),
                      )),
                  Text(
                    getTranslate(context, 'bottom_navi.profile'),
                    style: TextStyle(
                      foreground: Paint()
                        ..shader = selectedIndex == 4
                            ? const LinearGradient(
                                begin: Alignment.topLeft,
                                end: Alignment.topRight,
                                colors: gradient,
                              ).createShader(
                                const Rect.fromLTRB(350, 0, 400, 0))
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
                                      greyb7Color,
                                      greyb7Color,
                                    ])
                          .createShader(bounds);
                    },
                    child: const Icon(
                      Icons.home_rounded,
                      size: 26,
                      color: Colors.white,
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
