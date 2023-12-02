import 'dart:async';
import 'package:businessgate/database/app_database.dart';
import 'package:businessgate/theme.dart';
import 'package:flutter/material.dart';
import 'package:carousel_slider/carousel_slider.dart';
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
 
  List<String> imageAssets = [
    "assets/home/Rectangle 14 (9).png",
    "assets/home/web.jpg",
    "assets/home/Rectangle 14.png",
  ];

  List<String> imageTexts = [
    "Marketing using social media course",
    "How to build a website",
    "Full UI and UX designs",
  ];

  MyService _myEmail = MyService();

  String Name = "";

  String dropdownValue = "Languages";

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    Name = await ModelsUsers().FetchFirstName(_myEmail.myVariable);
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return Scaffold(
      appBar: AppBar(
        centerTitle: false,
        automaticallyImplyLeading: false,
        backgroundColor: Color.fromARGB(255, 177, 211, 237),
        toolbarHeight: size.height * 0.085,
        elevation: 3,
        shadowColor: Colors.grey.withOpacity(0.3),
        title: Row(
  children: [
    widthSpace,
    Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        FutureBuilder<void>(
          future: fetchData(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              // If the Future is still running, show a loading indicator or placeholder
              return CircularProgressIndicator();
            } else if (snapshot.hasError) {
              // If an error occurs, handle it here
              return Text('Error: ${snapshot.error}');
            } else {
              // If the Future is complete, display the fetched data
              return Text(
                getTranslate(context, 'home.hello') + ' ' + Name,
                style: black18Style,
              );
            }
          },
        ),
        heightbox(2),
      ],
    )
  ],
),
        actions: [
          SizedBox(
            height: 50,
            width: 160,
            child: 
                DropdownButton(
            dropdownColor: hexStringColor("#E3E0D2"),
            icon: Icon(Icons.menu,
            color: Colors.black),
            style: TextStyle(color: Colors.black),
            onChanged: (String? newValue) {
              if (newValue == 'Languages') {
          Navigator.pushNamed(context, '/languages');
        } else if (newValue == 'Sign Out') {
          showSignOutDialog(context, size);
        }
            },
            items: [
        DropdownMenuItem(
          value: 'Languages',
          child: buildDropdownItem('Languages', Icons.language_outlined),
        ),
        DropdownMenuItem(
          value: 'Sign Out',
          child: buildDropdownItem('Sign Out', Icons.exit_to_app),
        ),
      ],
    ),
  ),
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
            soonText(),
            topContainer(size),
            categorytext(),
            categoryList(size),
            height5Space,
            recentText(),
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

  Widget buildDropdownItem(String text, IconData icon) {
  return Row(
    children: [
      Icon(icon), // Add your desired icon here
      SizedBox(width: 8), // Adjust the spacing between the icon and text
      Text(text),
    ],
  );
}

void showSignOutDialog(BuildContext context, Size size) {
  showDialog(
    context: context,
    builder: (context) {
      return signoutDialog(context, size);
    },
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
                              style: black18Stylew600,
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

  recentText() {
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

  soonText() {
    return Padding(
      padding: const EdgeInsets.symmetric(
        vertical: fixPadding,
        horizontal: fixPadding * 2,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            getTranslate(context, 'home.soon'),
            style: black18Style,
          ),
        ],
      ),
    );
  }

  categoryList(Size size) {
         final category = [
    {
      "image": "assets/category/bussiness.png",
      "name": getTranslate(context, 'catergory.buss'),
      "icon": Icons.add_business_outlined,
      "isimage": false,
      "color": Color.fromARGB(255, 43, 74, 143),
      "prefix": "Business"
    },
    {
      "image": "assets/category/design.png",
      "name": getTranslate(context, 'catergory.arch'),
      "icon": Icons.design_services_outlined,
      "isimage": false,
      "color": Color.fromARGB(255, 47, 81, 157),
      "prefix": "Architecture"
    },
    {
      "image": "assets/category/helth.png",
      "name": getTranslate(context, 'catergory.helth'),
      "icon": Icons.medical_services_rounded,
      "isimage": false,
      "color": Color.fromARGB(255, 58, 99, 189),
      "prefix": "Health"
    },
  ];
    return SizedBox(
      height: size.height * 0.055,
      child: ListView.builder(
        padding: const EdgeInsets.symmetric(horizontal: fixPadding * 1.5),
        scrollDirection: Axis.horizontal,
        itemCount: category.length,
        
        shrinkWrap: true,
        physics: const BouncingScrollPhysics(),
        itemBuilder: (BuildContext context, int index) {
            return GestureDetector(
                onTap: () {
                  Navigator.pushNamed(context, '/filteredPrograms', arguments: category[index]['prefix'].toString());
                },
          child: Container(
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
             ) );
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
    return CarouselSlider(
      items: imageAssets.asMap().entries.map((entry) {
        int index = entry.key;
        String image = entry.value;
        String text = imageTexts[index];

        return Container(
          width: size.width * 0.9,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10.0),
            image: DecorationImage(
              image: AssetImage(image),
              fit: BoxFit.cover,
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 10.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                height5Space,
                Text(
                  text,
                  style: white18Style,
                ),
              ],
            ),
          ),
        );
      }).toList(),
      options: CarouselOptions(
        height: size.height * 0.22,
        viewportFraction: 1,
        enlargeCenterPage: true,
        autoPlay: true,
        autoPlayInterval: const Duration(seconds: 4),
        autoPlayAnimationDuration: const Duration(milliseconds: 800),
        autoPlayCurve: Curves.fastOutSlowIn,
      ),
    );
  }

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
