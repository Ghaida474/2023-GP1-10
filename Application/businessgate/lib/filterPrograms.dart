import 'package:businessgate/localization/localization_const.dart';
import 'package:businessgate/theme.dart';
import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';

import 'database/app_database.dart';
import 'models/model_user.dart';
import 'myservice.dart';

class filteredPrograms extends StatefulWidget {
  filteredPrograms({super.key});

  @override
  State<filteredPrograms> createState() => _filteredProgramsState();
}

class _filteredProgramsState extends State<filteredPrograms> {
  MyService filterName = MyService();

  String? categorytName;

  @override
  Widget build(BuildContext context) {
    categorytName = ModalRoute.of(context)?.settings.arguments.toString();
    print("in filtered program page");
    print(categorytName);

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
              future: GetCourses(context, categorytName),
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

  Future<List<Widget>> GetCourses(
      BuildContext context, String? category) async {
    final size = MediaQuery.of(context).size;
    List<Widget> courseWidgets = [];
    List<Courses> courses = await ModelsUsers().filterPrograms(category);

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

        print("in filtered page");

        print(course.name as String);
        print(course.price);
        print(course.instructer as String);
        print(course.id);
      }
    } catch (error) {
      print("Error: $error");
    }

    return courseWidgets;
  }
}
