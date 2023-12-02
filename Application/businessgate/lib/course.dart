import 'package:businessgate/localization/localization_const.dart';
import 'package:businessgate/models/model_user.dart';
import 'package:businessgate/database/app_database.dart';
import 'package:businessgate/theme.dart';
import 'package:businessgate/column_builder.dart';
import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';
import 'package:simple_progress_indicators/simple_progress_indicators.dart';
import '../../myservice.dart';
import 'package:intl/intl.dart';

class Course extends StatefulWidget {
  const Course({Key? key}) : super(key: key);

  @override
  State<Course> createState() => _Course();
}

class _Course extends State<Course> with SingleTickerProviderStateMixin {
  // Tab controller for managing tabs
  TabController? tabController;
  // Course information
  Courses courseInfo = Courses("", 0.0,0,"","","","","","","",false,"");
  // Value received from the route
  int? receivedValue;
  // Index of the selected tab
  int selectedindex = 0;
  String? status ;
  MyService _myEmail = MyService();

  final ratingList = <Map<String, dynamic>>[
    {
      "star": "5 star",
      "progress": 0.75,
      "person": "101",
    },
    {
      "star": "4 star",
      "progress": 0.65,
      "person": "12",
    },
    {
      "star": "3 star",
      "progress": 0.55,
      "person": "07",
    },
    {
      "star": "2 star",
      "progress": 0.45,
      "person": "04",
    },
    {
      "star": "1 star",
      "progress": 0.35,
      "person": "02",
    },
  ];

  @override
  void initState() {
    super.initState();
    // Initialize the tab controller
    tabController = TabController(length: 2, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    // Get the received value from the route
    receivedValue = ModalRoute.of(context)?.settings.arguments as int?;
    // Function to asynchronously load course information
    Future<void> loadCourse() async {
      Courses result;
      try {
        result = await GetCourse(context, receivedValue);
      } catch (e) {
        print("Error loading course: $e");
        return;
      }
      // Update the course information if the widget is still mounted
      if (mounted) {
        setState(() {
          courseInfo = result;
        });
      }
      status = await ModelsUsers().fetchStat(courseInfo.id, _myEmail.myVariable);
    }
    // Call the asynchronous function to load course information
    loadCourse();
    // Get the size of the screen
    final size = MediaQuery.of(context).size;
    // Scaffold widget for the course details
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
              colors: [hexStringColor("#6FBCF6"), hexStringColor("#E3E0D2")],
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter),
        ),
        child: CustomScrollView(
          physics: const BouncingScrollPhysics(),
          slivers: [
            // App bar with flexible space
            SliverAppBar(
              centerTitle: false,
              backgroundColor: Colors.transparent,
              expandedHeight: size.height * 0.01,
              leading: IconButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                icon: const Icon(
                  Icons.arrow_back_ios,
                  size: 22,
                  color: whiteColor,
                ),
              ),
              flexibleSpace: FlexibleSpaceBar(),
              pinned: true,
            ),
            // Sliver list for course details
            SliverList(
              delegate: SliverChildListDelegate(
                [
                  // Display course name, tabs, and tab views based on the selected index
                  detailname(),
                  tabs(size),
                  if (selectedindex == 0) firstTabview(),
                  if (selectedindex == 1) secondTabView(size),
                ],
              ),
            )
          ],
        ),
      ),
      // Display the bottom navigation bar
      bottomNavigationBar: bottonContainer(size),
    );
  }

  Future<bool> cancelCourse(BuildContext context, int? receivedValue) async {
     bool cancel = await ModelsUsers().cancelCourseM(receivedValue);
      return cancel ;
}

  // Function to get course information
  Future<Courses> GetCourse(BuildContext context, int? receivedValue) async {
    Courses Info = await ModelsUsers().TrainingProgram(receivedValue);
    return Info;
  }

  // Function for the second tab view
  secondTabView(Size size) {
    return Column(
      children: [
        overallRating(size),
      ],
    );
  }

  // Function for displaying overall rating
  overallRating(Size size) {
    return Container(
      width: double.maxFinite,
      margin: const EdgeInsets.all(fixPadding * 2),
      padding: const EdgeInsets.all(fixPadding * 2),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(color: grey94Color.withOpacity(0.4), blurRadius: 5),
        ],
      ),
      child: Column(
        children: [
          Text(
            getTranslate(context, 'detail.overall_rating'),
            style: black16Stylew600,
          ),
          height5Space,
          Row(
            children: [
              Column(
                children: [
                  const Text(
                    "4.5",
                    style: black16Style,
                  ),
                  height5Space,
                  Row(
                    children: [
                      for (int i = 0; i < 5; i++)
                        const Icon(
                          Icons.star,
                          color: primaryColor,
                          size: 14,
                        )
                    ],
                  ),
                  height5Space,
                  Text("(125 ${getTranslate(context, 'detail.review')})",
                      style: grey14Style)
                ],
              ),
              widthSpace,
              Expanded(
                child: ColumnBuilder(
                    itemBuilder: (context, index) {
                      return Padding(
                        padding: const EdgeInsets.symmetric(
                            vertical: fixPadding / 2),
                        child: Row(
                          children: [
                            Text(
                              ratingList[index]['star'].toString(),
                              style: grey14Style,
                            ),
                            width5Space,
                            Expanded(
                              child: ProgressBar(
                                value: ratingList[index]['progress'],
                                backgroundColor: const Color(0xfff0f0f0),
                                height: 4,
                                gradient: const LinearGradient(
                                  colors: gradient,
                                ),
                              ),
                            ),
                            width5Space,
                            Text(
                              ratingList[index]['person'].toString(),
                              style: grey14Style,
                            )
                          ],
                        ),
                      );
                    },
                    itemCount: ratingList.length),
              ),
            ],
          ),
        ],
      ),
    );
  }
  
  // Define a container with bottom navigation buttons
  bottonContainer(Size size) {
    return Container(
      height: size.height * 0.08,
      width: double.infinity,
      decoration: BoxDecoration(
        color: whiteColor,
        boxShadow: [
          BoxShadow(
            color: grey94Color.withOpacity(0.5),
            blurRadius: 5,
          ),
        ],
      ),
      child: Row(
        children: [

          // Left section with course price
Expanded(
              child: Container(
            alignment: Alignment.center,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Text(
                  getTranslate(context, 'detail.price'),
                  style: grey14Style,
                ),
                Text(
                  courseInfo.price.toString(),
                  style: black18Style,
                )
              ],
            ),
          )),
          // Right section with subscribe button
          Visibility(
            visible: (status == "register"), 
          child: Expanded(
            child: GestureDetector(
              onTap: () {
                setState(() {
                   Navigator.pushNamed(context, '/bfSurvey', arguments: receivedValue);
                });
              },
              child: Container(
                alignment: Alignment.center,
                color: primaryColor,
                child: Text(
                  getTranslate(context, 'detail.subscribe'),
                  style: white18Style,
                ),
              ),
            ),
          )),
          Visibility(
            visible: (status == "cancel"), 
          child: Expanded(
            child: GestureDetector(
              onTap: () {
                setState(() {
                  showCancellationConfirmationDialog();
                });
              },
              child: Container(
                alignment: Alignment.center,
                color: primaryColor,
                child: Text(
                  getTranslate(context, 'detail.cancelReg'),
                  style: white18Style,
                ),
              ),
            ),
          )),
          Visibility(
            visible: (status == "review"), 
          child: Expanded(
            child: GestureDetector(
              onTap: () {
                setState(() {
                   Navigator.pushNamed(context, '/afSurvey', arguments: receivedValue);
                });
              },
              child: Container(
                alignment: Alignment.center,
                color: primaryColor,
                child: Text(
                  getTranslate(context, 'detail.review'),
                  style: white18Style,
                ),
              ),
            ),
          )),
        ],
      ),
    );
  }

    void showCancellationConfirmationDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          content: Text(getTranslate(context, 'detail.canc_que')),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // Close the dialog
              },
              child: Text(getTranslate(context, 'detail.no')),
            ),
            TextButton(
              onPressed: () {
               cancelCourse(context, receivedValue);
                Navigator.of(context).pop(); // Close the dialog
                 Navigator.pushNamed(context, '/myCourses');
                 Navigator.of(context).pushReplacementNamed('/bottomNavi');
              },
              child: Text(getTranslate(context, 'detail.yes')),
            ),
          ],
        );
      },
    );
  }

  // Define a stack of tabs
  tabs(Size size) {
    return Stack(
      children: [
        Container(
          height: size.height * 0.07,
          width: double.infinity,
          decoration: const BoxDecoration(
            color: whiteColor,
            border: Border(
              bottom: BorderSide(
                color: Color(0xffc4c4c4),
                width: 3,
              ),
            ),
          ),
        ),
        SizedBox(
          height: size.height * 0.07,
          child: TabBar(
            onTap: (int index) {
              setState(() {
                selectedindex = index;
              });
            },
            controller: tabController,
            labelColor: primaryColor,
            labelStyle: primary16Style,
            unselectedLabelColor: grey94Color,
            indicatorPadding: const EdgeInsets.all(0.0),
            indicatorWeight: 3.0,
            labelPadding: const EdgeInsets.only(left: 0.0, right: 0.0),
            // Tab indicator with gradient
            indicator: const ShapeDecoration(
                shape: UnderlineInputBorder(
                    borderSide: BorderSide(
                  color: Colors.transparent,
                  width: 0,
                )),
                gradient: LinearGradient(colors: gradient)),
            tabs: <Widget>[
              Container(
                height: size.height * 0.07,
                alignment: Alignment.center,
                color: Colors.white,
                child: Text(getTranslate(context, 'detail.about')),
              ),
              Container(
                height: size.height * 0.07,
                alignment: Alignment.center,
                color: Colors.white,
                child: Text(getTranslate(context, 'detail.review_text')),
              ),
            ],
          ),
        ),
      ],
    );
  }

  // Define the course details section
  detailname() {
    return Padding(
      padding: const EdgeInsets.symmetric(
          horizontal: fixPadding * 2, vertical: fixPadding),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Display the course name
          Text(
            courseInfo.name.toString(), //course name
            style: black22Style,
          ),
          height5Space,
        ],
      ),
    );
  }

  firstTabview() {
    // This function returns a column with three widgets: coursebrief, description, and createby
    return Column(
      children: [
        coursebrief(),
        description(),
        createby(),
      ],
    );
  }

  createby() {
    // This function returns a container with information about the creator of the cours
    return Container(
      width: double.maxFinite,
      margin: const EdgeInsets.symmetric(
          horizontal: fixPadding * 2, vertical: fixPadding * 2),
      padding: const EdgeInsets.all(fixPadding * 2),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(color: grey94Color.withOpacity(0.4), blurRadius: 5),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            getTranslate(context, 'detail.creat_by'),
            style: black16Stylew600,
          ),
          heightSpace,
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              widthSpace,
              widthSpace,
              Expanded(
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Text(
                                courseInfo.instructer.toString(),
                                style: black16Stylew600,
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  description() {
    // This function returns a container with the course description
    return Container(
      width: double.maxFinite,
      margin: const EdgeInsets.symmetric(horizontal: fixPadding * 2),
      padding: const EdgeInsets.all(fixPadding * 2),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(color: grey94Color.withOpacity(0.4), blurRadius: 5),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            getTranslate(context, 'detail.description'),
            style: black16Stylew600,
          ),
          heightSpace,
           Text(
            courseInfo.description.toString(),
            style: grey14Style,
          ),
        ],
      ),
    );
  }

  // Function to display course brief information
  coursebrief() {
    return Container(
      width: double.maxFinite,
      margin: const EdgeInsets.all(fixPadding * 2),
      padding: const EdgeInsets.all(fixPadding * 2),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(color: grey94Color.withOpacity(0.4), blurRadius: 5),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Title: Course Brief
          Text(
            getTranslate(context, 'detail.course_brief'),
            style: black16Stylew600,
          ),
          heightSpace,
          // Row for start and end time
          Row(
            children: [
              Expanded(
                // Display start time
                child: breifdetail(
                    Icons.access_time_filled,
                    getTranslate(context, 'detail.start_time'),
                    "",
                    courseInfo.startTime.toString()), //  courseInfo.startTime.toString() start
              ),
              Expanded(
                // Display end time
                child: breifdetail(
                    Icons.access_time_filled,
                    getTranslate(context, 'detail.end_time'),
                    "",
                    courseInfo.endTime.toString()), //courseInfo.endTime.toString()
              )
            ],
          ),
          heightSpace,
          height5Space,
          // Row for start and end date
          Row(
            children: [
              Expanded(
                // Display start date
                child: breifdetail2(
                  Icons.calendar_today_rounded,
                  getTranslate(context, 'detail.start_date'),
                  courseInfo.startDate.toString(),
                ),
              ),
              Expanded(
                // Display end date
                child: breifdetail2(
                  Icons.calendar_today_rounded,
                  getTranslate(context, 'detail.end_date'),
                  courseInfo.endDate.toString(),
                ),
              )
            ],
          ),
          heightSpace,
          height5Space,
          // Row for start and end date
          Row(
            children: [
              Visibility(
                visible: (courseInfo.kind),
                child: Expanded(
                // Display start date
                child: breifdetail2(
                  Icons.location_city_outlined,
                  getTranslate(context, 'detail.kind'),
                  "online", // ret
                ),
              ),),
                Visibility(
                visible: (courseInfo.kind == false),
                child: Expanded(
                // Display start date
                child: breifdetail2(
                  Icons.location_city_outlined,
                  getTranslate(context, 'detail.kind'),
                  "On Site", // ret
                ),
              ),),
              Visibility(
                visible: (status == "cancel" && courseInfo.kind && courseInfo.location != null),
                child: Expanded(
                // Display end date
                child: breifdetail2(
                  Icons.location_city_outlined,
                  getTranslate(context, 'detail.link'),
                  courseInfo.location.toString(),
                ),
              )),
              Visibility(
                visible: (courseInfo.kind == false),
                child: Expanded(
                // Display end date
                child: breifdetail2(
                  Icons.location_city_outlined,
                  getTranslate(context, 'detail.place'),
                  courseInfo.location.toString(),
                ),
              )),
            ],
          )
        ],
      ),
    );
  }

  // Function to display brief details in a row
  breifdetail(IconData icon, String title, String content, String number) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(
          icon,
          size: 16,
          color: primaryColor,
        ),
        widthSpace,
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: grey14Style,
              ),
              height5Space,
              // Display time content
              Text(
                '$number $content',
                style: black14Stylew600,
              )
            ],
          ),
        )
      ],
    );
  }

  // Function to display brief details in a row with a different format
  breifdetail2(IconData icon, String title, String content) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(
          icon,
          size: 16,
          color: primaryColor,
        ),
        widthSpace,
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: grey14Style,
              ),
              height5Space,
              // Display date content
              Text(
                content,
                style: black14Stylew600,
              )
            ],
          ),
        )
      ],
    );
  }
}
