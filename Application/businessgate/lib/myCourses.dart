import 'package:businessgate/theme.dart';
import 'package:flutter/material.dart';

import 'database/app_database.dart';
import 'localization/localization_const.dart';
import 'package:businessgate/localization/localization_const.dart';
import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';

import '../../myservice.dart';
import 'models/model_user.dart';




class myCoursesNavigationMenu extends StatelessWidget {
  const myCoursesNavigationMenu({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('myCourses'),
      ),
      body: Container(
        padding: EdgeInsets.all(20),
        alignment: Alignment.center,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                navigateTomyCourses(context, 1);
              },
              child: Text('Upcoming'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                navigateTomyCourses(context, 2);
              },
              child: Text('Running'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                navigateTomyCourses(context, 3);
              },
              child: Text('Completed'),
            ),
          ],
        ),
      ),
    );
  }

  void navigateTomyCourses(BuildContext context, int choice) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => myCourses(sectionIndex: choice),
      ),
    );
  }
}




class myCourses extends StatefulWidget {
   final int sectionIndex;
  const myCourses({Key? key, required this.sectionIndex}) : super(key: key);

  @override
  State<myCourses> createState() => _myCoursesState();
}

class _myCoursesState extends State<myCourses> {
  MyService _myID = MyService();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
    extendBodyBehindAppBar: true,
    appBar: AppBar(
      backgroundColor: Colors.transparent,
      elevation: 0,
      title: Text(
        getTranslate(context, 'myCourses.my_courses'),
        style: const TextStyle(fontWeight: FontWeight.bold),
      ),
      automaticallyImplyLeading: false,
      leading: IconButton(
              onPressed: () {
                Navigator.pop(context);
              },
              icon: const Icon(
                Icons.arrow_back_ios,
                size: 22,
                color: Colors.black,
              ),
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
            child : ListView(
        children: [
          FutureBuilder<List<Widget>>(
              future: getRegisteredCourses(context),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return CircularProgressIndicator(); // Placeholder for loading state
                } else if (snapshot.hasError) {
                  return Text('Error: ${snapshot.error}');
                } else {
                  // Display the list of widgets
                  List<Widget> courseWidgets1 = snapshot.data ?? [];
                  return Column(children: courseWidgets1);
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
            Navigator.pushNamed(context, '/course', arguments:id);
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


  Future<List<Widget>> getRegisteredCourses(BuildContext context) async {
    final size = MediaQuery.of(context).size;
    List<Widget> courseWidgets1 = [];
   List<Courses> courses1=[];
   if (widget.sectionIndex == 1)
     courses1 = await ModelsUsers().getRegisteredCoursesM(_myID.myVariable2);
  if (widget.sectionIndex == 2)
     courses1 = await ModelsUsers().getRunningCoursesM(_myID.myVariable2);
  if (widget.sectionIndex == 3)
     courses1 = await ModelsUsers().getCompletedCoursesM(_myID.myVariable2);

    try {

      for (Courses course in courses1) {

        Widget courseWidget = poularlist(
          size,
          course.name as String,
          course.price,
          course.instructer as String,
          course.id,
        );

        courseWidgets1.add(courseWidget);
      }
    } catch (error) {
      print("Error: $error");
    }

    return courseWidgets1;
  }
}