import 'package:businessgate/localization/localization_const.dart';
import 'package:businessgate/myservice.dart';
import 'package:businessgate/theme.dart';
import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';

class CategoryScreen extends StatelessWidget {
  CategoryScreen({Key? key}) : super(key: key);

  MyService filterName = MyService();

  final categorylist = [
    {
      "image": "assets/category/bussiness.png",
      "name": "Business",
      "icon": Icons.add_business_outlined,
      "isimage": false,
    },
    {
      "image": "assets/category/design.png",
      "name": "Architecture",
      "icon": Icons.design_services_outlined,
      "isimage": false,
    },
    {
      "image": "assets/category/helth.png",
      "name": "Health",
      "icon": Icons.medical_services_rounded,
      "isimage": false,
    },
    {
      "image": "assets/category/Rectangle 22.png",
      "name": "Computer",
      "icon": Icons.add_business_outlined,
      "isimage": true,
      "iconimage": "assets/category/window 1.png"
    },
    {
      "image": "assets/category/design.png",
      "name": "Language",
      "icon": Icons.language_outlined,
      "isimage": false,
    },
    {
      "image": "assets/category/design.png",
      "name": "Art",
      "icon": Icons.brush_rounded,
      "isimage": false,
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        extendBodyBehindAppBar: true,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          foregroundColor: blackColor,
          title: Text(
            getTranslate(context, 'catergory.catergory'),
            style: const TextStyle(fontWeight: FontWeight.bold),
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
          child: GridView.builder(
            itemCount: categorylist.length,
            padding: const EdgeInsets.only(top: 160, right: 18, left: 18),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                mainAxisSpacing: fixPadding * 1.5,
                crossAxisSpacing: fixPadding * 1.5,
                childAspectRatio: 2),
            itemBuilder: (context, index) {
              return GestureDetector(
                onTap: () {
                  Navigator.pushNamed(context, '/filteredPrograms', arguments: categorylist[index]['name'].toString());
                },
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Stack(
                    children: [
                      Positioned.fill(
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),
                      Positioned.fill(
                        child: Container(
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(10),
                            color: hexStringColor("#095590"),
                          ),
                        ),
                      ),
                      Center(
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            categorylist[index]['isimage'] == false
                                ? Icon(
                                    categorylist[index]['icon'] as IconData,
                                    color: whiteColor,
                                    size: 18,
                                  )
                                : Image.asset(
                                    categorylist[index]['iconimage'].toString(),
                                    height: 18,
                                    width: 18,
                                  ),
                            width5Space,
                            Text(
                              categorylist[index]['name'].toString(),
                              style: white16Stylew500,
                            )
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
        ));
  }
}
