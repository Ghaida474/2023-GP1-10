import 'package:businessgate/theme.dart';
import 'package:flutter/material.dart';
import 'database/app_database.dart';
import 'localization/localization_const.dart';
import 'package:businessgate/utils/colors.dart';
import '../../myservice.dart';
import 'models/model_user.dart';

class myCoursesNavigationMenu extends StatelessWidget {
  const myCoursesNavigationMenu({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
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
                SizedBox(height: 30),
                List(size, context),
              ],
            ),
          ),
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

  List(Size size, BuildContext context) {
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
          listTile(
            () {
              navigateTomyCourses(context, 1);
            },
            getTranslate(context, 'Course.coming'),
          ),
          devider(),
          listTile(
            () {
              navigateTomyCourses(context, 2);
            },
            getTranslate(context, 'Course.running'),
          ),
          devider(),
          listTile(
            () {
              navigateTomyCourses(context, 3);
            },
            getTranslate(context, 'Course.complete'),
          ),
        ],
      ),
    );
  }

  listTile(Function() onTap, String title) {
    return ListTile(
      onTap: onTap,
      minLeadingWidth: 0,
      title: Text(
        title,
        style: TextStyle(
                color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600)
            .copyWith(color: Colors.white, fontWeight: FontWeight.w500),
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
}

class myCourses extends StatefulWidget {
  final int sectionIndex;
  const myCourses({Key? key, required this.sectionIndex}) : super(key: key);

  @override
  State<myCourses> createState() => _myCoursesState();
}

class _myCoursesState extends State<myCourses> {
  String? status;
  MyService _myID = MyService();
  MyService _myEmail = MyService();
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
        child: ListView(
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

  poularlist(Size size, String name, double? price, String date, int? id) {
    return GestureDetector(
      onTap: () {
        Navigator.pushNamed(context, '/course', arguments: id);
      },
      child: Container(
        margin: const EdgeInsets.only(
          left: fixPadding * 2,
          right: fixPadding * 2,
          bottom: fixPadding * 2,
          top: fixPadding,
        ),
        height: size.height * 0.15,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10),
          color: whiteColor,
          boxShadow: [
            BoxShadow(
              color: grey94Color.withOpacity(0.5),
              blurRadius: 5,
            ),
          ],
        ),
        child: Column(
          children: [
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
                              padding: EdgeInsets.only(right: fixPadding / 5),
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
                          date ,
                      style: grey14Style,
                    ),
                    Text(
                      getTranslate(context, 'detail.price') +
                          ' : ' +
                          price.toString(),
                      style: primary16Style,
                    ),
                    Visibility(
                      visible: (widget.sectionIndex == 1 && status == "cancel"),
                      child: Text(
                        getTranslate(context, 'detail.StatCanc'),
                        style: primary16Style2,
                      ),
                    ),
                    Visibility(
                      visible: (widget.sectionIndex == 3 && status == "review"),
                      child: Text(
                        getTranslate(context, 'detail.StatRw'),
                        style: primary16Style2,
                      ),
                    )
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<List<Widget>> getRegisteredCourses(BuildContext context) async {
    final size = MediaQuery.of(context).size;
    List<Widget> courseWidgets1 = [];
    List<Courses> courses1 = [];
    if (widget.sectionIndex == 1)
      courses1 = await ModelsUsers().getRegisteredCoursesM(_myID.myVariable2);
    if (widget.sectionIndex == 2)
      courses1 = await ModelsUsers().getRunningCoursesM(_myID.myVariable2);
    if (widget.sectionIndex == 3)
      courses1 = await ModelsUsers().getCompletedCoursesM(_myID.myVariable2);
    try {
      for (Courses course in courses1) {
        status = await ModelsUsers().fetchStat(course.id, _myEmail.myVariable);

        Widget courseWidget = poularlist(
          size,
          course.name as String,
          course.price,
          course.startDate as String,
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
