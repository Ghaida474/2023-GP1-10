import 'package:businessgate/localization/localization_const.dart';
import 'package:businessgate/models/model_user.dart';
import 'package:businessgate/database/app_database.dart';
import 'package:businessgate/theme.dart';
import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';
import '../../myservice.dart';

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

  @override
  void initState() {
    super.initState();
    // Initialize the tab controller
    tabController = TabController(length: 1, vsync: this);
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
                  CancelDialog(context,size);
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
            style: black14Style2,
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
                child: breifdetail2(
                  Icons.screenshot_monitor,
                  getTranslate(context, 'detail.kind'),
                  getTranslate(context, 'detail.kind1'), // ret
                ),
              ),),
                Visibility(
                visible: (courseInfo.kind == false ),
                child: Expanded(
                child: breifdetail2(
                  Icons.screenshot_monitor,
                  getTranslate(context, 'detail.kind'),
                  getTranslate(context, 'detail.kind2'), // ret
                ),
              ),),
              Visibility(
                visible: (status == "cancel" && courseInfo.kind && courseInfo.location != null),
                child: Expanded(
                child: breifdetail2(
                  Icons.location_pin,
                  getTranslate(context, 'detail.link'),
                  courseInfo.location.toString(),
                ),
              )),
              Visibility(
                visible: (courseInfo.kind == false),
                child: Expanded(
                child: breifdetail2(
                  Icons.location_pin,
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

  CancelDialog(BuildContext context, Size size) {
  showDialog(
    context: context,
    builder: (BuildContext context) {
      return AlertDialog(
        backgroundColor: Color.fromARGB(255, 162, 211, 246),
        titlePadding: const EdgeInsets.all(10 * 3),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
        ),
        title: Column(
          children: [
            Text(
              getTranslate(context, 'survey.canc_que'),
              style: TextStyle(
                fontSize: 18, 
                fontWeight: FontWeight.bold, 
                color: Colors.black,
              ),
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
                        getTranslate(context, 'survey.no'),
                        style: TextStyle(
                          fontSize: 17,
                          color: Color.fromARGB(255, 107, 105, 105),
                          fontWeight: FontWeight.w400,
                        ),
                      ),
                    ),
                  ),
                ),
                SizedBox(width: 10),
                SizedBox(width: 10),
                Expanded(
                  child: InkWell(
                    onTap: () {
                      cancelCourse(context, receivedValue);
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            backgroundColor: hexStringColor("##E3E0D2"),
            elevation: 10.0,
            shape: Border.all(
                color: const Color.fromARGB(255, 0, 0, 0), width: 0.5, style: BorderStyle.solid),
            content: Text(
              getTranslate(context, 'survey.canc_suc'),
              style: TextStyle(
                color: const Color.fromARGB(255, 58, 58, 58),
                fontSize: 18.0,
                fontStyle: FontStyle.italic,
                fontWeight: FontWeight.bold,
                letterSpacing: 2.0,
              ),
              textAlign: TextAlign.center,
            ),
          ));
                      Navigator.pushNamed(context, '/myCourses');
                      Navigator.of(context).pushReplacementNamed('/bottomNavi');
                    },
                    child: Container(
                      height: 40,
                      width: 40,
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
                        getTranslate(context, 'survey.yes'),
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
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
    },
  );
}


    /*CancelDialog(BuildContext context, Size size) {
    return AlertDialog(
      backgroundColor: Color.fromARGB(255, 162, 211, 246),
      titlePadding: const EdgeInsets.all(10 * 3),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
      ),
      title: Column(
        children: [
          Text(
            getTranslate(context, 'survey.canc_que'),
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
                      getTranslate(context, 'survey.yes'),
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
                    Navigator.pushNamed(context, '/myCourses');
            Navigator.of(context).pushReplacementNamed('/bottomNavi');
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
                      getTranslate(context, 'survey.no'),
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
  }*/
}
