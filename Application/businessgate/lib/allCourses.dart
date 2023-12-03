import 'package:businessgate/theme.dart';
import 'package:flutter/material.dart';
import 'database/app_database.dart';
import 'localization/localization_const.dart';
import 'package:businessgate/utils/colors.dart';
import 'models/model_user.dart';

class allCourses extends StatefulWidget {
  const allCourses({super.key});

  @override
  State<allCourses> createState() => _allCoursesState();
}

class _allCoursesState extends State<allCourses> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text(
          getTranslate(context, 'Course.all_course'),
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
        child: ListView(
          children: [
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

  poularlist(Size size, String name, double? price, String date, int? id) {
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
            height: size.height * 0.13,
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
                                Container(
                              height: size.height * 0.04,
                              alignment: Alignment.centerRight,
                              child: Icon(
                                Icons.arrow_forward_ios,
                                size: 18,
                                color: Colors.black,
                              ),
                            ),
                              ],
                            ),
                          ],
                        ),
                        Text(
                              getTranslate(context, 'detail.start_date') +
                              ' : ' +
                          date,
                          style: grey14Style,
                        ),
                        Text(
                          getTranslate(context, 'detail.price') +
                              ' : ' +
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

  Future<List<Widget>> GetRecentCourses(BuildContext context) async {
    final size = MediaQuery.of(context).size;
    List<Widget> courseWidgets = [];
    List<Courses> courses = await ModelsUsers().TrainingPrograms();

    try {
      for (Courses course in courses) {
        Widget courseWidget = poularlist(
          size,
          course.name as String,
          course.price,
          course.startDate as String,
          course.id,
        );
        courseWidgets.add(courseWidget);
      }
    } catch (error) {
      print("Error: $error");
    }

    return courseWidgets;
  }
}
