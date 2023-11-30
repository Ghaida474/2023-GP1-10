import 'package:businessgate/database/app_database.dart';
import 'package:businessgate/theme.dart';
import 'package:flutter/material.dart';

import '../localization/localization_const.dart';
import '../models/model_user.dart';
import '../myservice.dart';
import '../utils/colors.dart';

class Home extends StatefulWidget {
  const Home({Key? key}) : super(key: key);

  @override
  State<Home> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<Home> {
  final category = [
    {
      "image": "assets/category/bussiness.png",
      "name": "Business",
      "icon": Icons.add_business_outlined,
      "isimage": false,
      "color": Color.fromARGB(255, 21, 82, 213),
    },
    {
      "image": "assets/category/design.png",
      "name": "Architecture",
      "icon": Icons.design_services_outlined,
      "isimage": false,
      "color": const Color(0xff15A812),
    },
    {
      "image": "assets/category/helth.png",
      "name": "Medicine",
      "icon": Icons.medical_services_rounded,
      "isimage": false,
      "color": Color.fromARGB(255, 173, 159, 92),
    },
  ];

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return Scaffold(
      appBar: AppBar(
        centerTitle: false,
        automaticallyImplyLeading: false,
        backgroundColor: Color.fromARGB(255, 149, 202, 242),
        toolbarHeight: size.height * 0.085,
        elevation: 3,
        shadowColor: Colors.grey.withOpacity(0.3),
        title: Row(
          children: [
            widthSpace,
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  getTranslate(context, 'home.hello'),
                  style: black18Style,
                ),
                heightbox(2),
              ],
            )
          ],
        ),
        actions: [
          SizedBox(
            height: 50,
            width: 50,
            child: Stack(
              children: [
                IconButton(
                  onPressed: () {
                    showDialog(
                      barrierColor: Colors.black.withOpacity(0.3),
                      context: context,
                      builder: (context) {
                        return signoutDialog(context, size);
                      },
                    );
                  },
                  icon: const Icon(
                    Icons.logout,
                    color: Colors.black,
                  ),
                ),
                Positioned(
                  right: 18,
                  top: 15,
                  child: Container(
                    height: 6,
                    width: 6,
                  ),
                ),
              ],
            ),
          )
        ],
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
              colors: [hexStringColor("#6FBCF6"), hexStringColor("#E3E0D2")],
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter),
        ),
        child: ListView(
          children: [
            topContainer(size),
            categorytext(),
            categoryList(size),
            height5Space,
            popularText(),
            FutureBuilder<List<Widget>>(
              future: GetRecentCourses(context),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return CircularProgressIndicator(); // Placeholder for loading state
                } else if (snapshot.hasError) {
                  return Text('Error: ${snapshot.error}');
                } else {
                  // Display the list of widgets
                  List<Widget> courseWidgets = snapshot.data ?? [];
                  return Column(children: courseWidgets);
                }
              },
            ),
          ],
        ),
      ),
    );
  }

  poularlist(Size size, String name, double? price, String coach, int? id) {
    return Column(
      children: [
        GestureDetector(
          onTap: () {
            Navigator.pushNamed(context, '/course', arguments: id);
          },
          child: Container(
            margin: const EdgeInsets.only(
                left: fixPadding * 2,
                right: fixPadding * 2,
                bottom: fixPadding * 2,
                top: fixPadding),
            height: size.height * 0.15,
            decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(10),
                color: whiteColor,
                boxShadow: [
                  BoxShadow(
                    color: grey94Color.withOpacity(0.5),
                    blurRadius: 5,
                  )
                ]),
            child: Column(
              children: [
                ClipRRect(
                  borderRadius: const BorderRadius.vertical(
                    top: Radius.circular(10),
                  ),
                ),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(fixPadding),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              name,
                              style: black16Stylew600,
                              overflow: TextOverflow.ellipsis,
                            ),
                            Row(
                              children: [
                                const Padding(
                                  padding:
                                      EdgeInsets.only(right: fixPadding / 5),
                                ),
                              ],
                            ),
                          ],
                        ),
                        Text(
                          coach,
                          style: grey14Style,
                        ),
                        Text(
                          price.toString(),
                          style: primary16Style,
                        )
                      ],
                    ),
                  ),
                )
              ],
            ),
          ),
        ),
      ],
    );
  }

  poularIcon2(Size size, String image, String name) {
    return Expanded(
      child: GestureDetector(
        onTap: () {
          Navigator.pushNamed(context, '/home');
        },
        child: Container(
          margin: const EdgeInsets.symmetric(horizontal: fixPadding),
          height: size.height * 0.32,
          decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(10),
              color: whiteColor,
              boxShadow: [
                BoxShadow(
                  color: grey94Color.withOpacity(0.5),
                  blurRadius: 5,
                )
              ]),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              ClipRRect(
                borderRadius: const BorderRadius.vertical(
                  top: Radius.circular(10),
                ),
                child: Image.asset(
                  image,
                  height: size.height * 0.16,
                  width: double.infinity,
                  fit: BoxFit.cover,
                ),
              ),
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.all(fixPadding),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        name,
                        style: black16Stylew600,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const Text(
                        "Saad",
                        style: grey14Style,
                      ),
                      Row(
                        children: [
                          for (int i = 0; i < 5; i++)
                            ShaderMask(
                              shaderCallback: (Rect bounds) {
                                return const LinearGradient(
                                  colors: gradient,
                                  begin: Alignment.topCenter,
                                  end: Alignment.bottomCenter,
                                ).createShader(bounds);
                              },
                              child: const Padding(
                                padding: EdgeInsets.only(right: fixPadding / 5),
                                child: Icon(
                                  Icons.star,
                                  size: 15,
                                  color: whiteColor,
                                ),
                              ),
                            ),
                          const Text(
                            "(125)",
                            style: grey14Style,
                          ),
                        ],
                      ),
                      const Text(
                        "200 SR",
                        style: primary16Style,
                      )
                    ],
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }

  popularText() {
    return Padding(
      padding: const EdgeInsets.symmetric(
        vertical: fixPadding,
        horizontal: fixPadding * 2,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            getTranslate(context, 'home.recent'),
            style: black18Style,
          ),
          GestureDetector(
            onTap: () {
              Navigator.pushNamed(context, '/allCourses');
            },
            child: Text(getTranslate(context, 'home.see_all_P'),
                style: primary14Style),
          )
        ],
      ),
    );
  }

  categoryList(Size size) {
    return SizedBox(
      height: size.height * 0.055,
      child: ListView.builder(
        padding: const EdgeInsets.symmetric(horizontal: fixPadding * 1.5),
        scrollDirection: Axis.horizontal,
        itemCount: category.length,
        shrinkWrap: true,
        physics: const BouncingScrollPhysics(),
        itemBuilder: (BuildContext context, int index) {
          return Container(
            alignment: Alignment.center,
            padding: const EdgeInsets.symmetric(
                horizontal: fixPadding * 1.5, vertical: fixPadding),
            margin: const EdgeInsets.symmetric(horizontal: fixPadding / 2),
            decoration: BoxDecoration(
              color: category[index]['color'] as Color,
              borderRadius: BorderRadius.circular(10),
              boxShadow: [
                BoxShadow(
                  color: grey94Color.withOpacity(0.3),
                  blurRadius: 5,
                )
              ],
            ),
            child: Row(
              children: [
                category[index]['isimage'] == false
                    ? Icon(
                        category[index]['icon'] as IconData,
                        size: 20,
                        color: whiteColor,
                      )
                    : Image.asset(
                        category[index]['iconimage'].toString(),
                        height: 20,
                        width: 20,
                        color: whiteColor,
                      ),
                width5Space,
                Text(
                  category[index]['name'].toString(),
                  style: white16Stylew500,
                )
              ],
            ),
          );
        },
      ),
    );
  }

  categorytext() {
    return Padding(
      padding: const EdgeInsets.symmetric(
        vertical: fixPadding,
        horizontal: fixPadding * 2,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            getTranslate(context, 'catergory.catergory'),
            style: black18Style,
          ),
          GestureDetector(
            onTap: () {
              Navigator.pushNamed(context, "/category");
            },
            child: Text(getTranslate(context, 'home.see_all_C'),
                style: primary14Style),
          )
        ],
      ),
    );
  }

  topContainer(Size size) {
    return Stack(
      children: [
        SizedBox(
          height: size.height * 0.22,
          width: double.infinity,
          child: Image.asset(
            "assets/images/Logo2.png",
            fit: BoxFit.cover,
          ),
        ),
        Positioned(
          bottom: 7,
          left: 0,
          right: 0,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: fixPadding * 2),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
            ),
          ),
        )
      ],
    );
  }

  /*Future<List<Widget>> GetRecentCourses(BuildContext context) async {
    final size = MediaQuery.of(context).size;
    List<Widget> courseWidgets = [];
    List<Courses> courses = await ModelsUsers().TrainingPrograms();

    try {
      for (Courses course in courses) {
        Widget courseWidget = poularlist(
          size,
          course.name as String,
          course.price,
          course.instructer as String,
          course.id,
        );
        courseWidgets.add(courseWidget);
      }
    } catch (error) {
      print("Error: $error");
    }

    return courseWidgets;
  }*/

  Future<List<Widget>> GetRecentCourses(BuildContext context) async {
    final size = MediaQuery.of(context).size;
    List<Widget> courseWidgets = [];
    List<Courses> courses = await ModelsUsers().TrainingPrograms();

    try {
      // Take only the last 3 courses from the list
      List<Courses> recentCourses =
          courses.length > 3 ? courses.sublist(courses.length - 3) : courses;

      for (Courses course in recentCourses) {
        Widget courseWidget = poularlist(
          size,
          course.name as String,
          course.price,
          course.instructer as String,
          course.id,
        );
        courseWidgets.add(courseWidget);
      }
    } catch (error) {
      print("Error: $error");
    }

    return courseWidgets;
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
            style: TextStyle(
                fontSize: 18, fontWeight: FontWeight.bold, color: Colors.black),
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
                    height: 40,
                    width: 40,
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
                      style: TextStyle(
                          fontSize: 17,
                          color: Color.fromARGB(255, 107, 105, 105),
                          fontWeight: FontWeight.w400),
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
                    height: 40,
                    width: 40,
                    decoration: BoxDecoration(
                      color: hexStringColor("#095590"),
                      borderRadius: BorderRadius.circular(10),
                      boxShadow: [
                        BoxShadow(
                          color:
                              Color.fromARGB(255, 250, 0, 0).withOpacity(0.5),
                          blurRadius: 5,
                        )
                      ],
                    ),
                    alignment: Alignment.center,
                    child: Text(
                      getTranslate(context, 'profile.logout'),
                      style: TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontWeight: FontWeight.bold),
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
}
