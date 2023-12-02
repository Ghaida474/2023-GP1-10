import 'package:businessgate/localization/localization_const.dart';
import 'package:businessgate/theme.dart';
import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../main.dart';

// Declare a variable to hold the selected language
String? languageValue;

class Languages extends StatefulWidget {
  const Languages({Key? key}) : super(key: key);

  @override
  State<Languages> createState() => _LanguagesState();
}

class _LanguagesState extends State<Languages> {
  SharedPreferences? prefs;
  final key = "value";

  @override
  void initState() {
    super.initState();
    _read(); // Read the saved language preference when the widget is initialized
  }

  // Function to read the saved language preference from SharedPreferences
  _read() async {
    prefs = await SharedPreferences.getInstance();
    setState(() {
      languageValue = prefs!.getString(key) ?? "English";
    });
  }

  // Function to change the language and update the UI
  void _changeLanguges(String languageCode) async {
    Locale temp = await setLocales(languageCode);
    // Set the locale for the entire app
    MyApp.setLocale(context, temp);
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return Scaffold(
        extendBodyBehindAppBar: true,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          foregroundColor: blackColor,
          title: Text(
            getTranslate(context, 'languages'),
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
          child: ListView.builder(
            itemCount: LanguagesList.languageList.length,
            padding: const EdgeInsets.only(top: 190, right: 18, left: 18),
            physics: const BouncingScrollPhysics(),
            itemBuilder: (context, index) {
              return Container(
                height: size.height * 0.07,
                width: double.infinity,
                margin: const EdgeInsets.only(bottom: 25),
                decoration: BoxDecoration(
                  color: hexStringColor("#095590").withOpacity(0.40),
                  borderRadius: BorderRadius.circular(10),
                  boxShadow: [
                    BoxShadow(
                      color: grey94Color.withOpacity(0.5),
                      blurRadius: 5,
                    ),
                  ],
                ),
                alignment: Alignment.center,
                child: ListTile(
                  onTap: () {
                    // Change the language when a language is tapped
                    _changeLanguges(
                        LanguagesList.languageList[index].languageCode!);
                    setState(() {
                      languageValue = LanguagesList.languageList[index].name;
                    });
                    // Save the selected language to SharedPreferences
                    prefs?.setString(key, languageValue!);
                  },
                  leading:
                      languageValue == LanguagesList.languageList[index].name
                          ? Container(
                              height: size.height * 0.028,
                              width: size.height * 0.028,
                              padding: const EdgeInsets.all(fixPadding / 2),
                              decoration: const BoxDecoration(
                                  shape: BoxShape.circle, color: Colors.black),
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
                              decoration: BoxDecoration(
                                color: whiteColor,
                                shape: BoxShape.circle,
                                border: Border.all(
                                  color: greyb7Color,
                                ),
                              ),
                            ),
                  minLeadingWidth: 0,
                  title: Text(
                    LanguagesList.languageList[index].name.toString(),
                    style: black16Stylew400.copyWith(
                        fontWeight: FontWeight.w500, height: 0.7),
                  ),
                ),
              );
            },
          ),
        ));
  }
}

// Class to represent the list of supported languages
class LanguagesList {
  final int? id;
  final String? name;
  final String? languageCode;

  LanguagesList({this.id, this.languageCode, this.name});
  // List of supported languages
  static List<LanguagesList> languageList = [
    LanguagesList(id: 1, name: "English", languageCode: 'en'),
    LanguagesList(id: 5, name: "عربي", languageCode: 'ar'),
  ];
}
