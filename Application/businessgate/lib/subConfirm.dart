import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';
import 'localization/localization_const.dart';

class SubConformation extends StatefulWidget {
  const SubConformation({super.key});

  @override
  State<SubConformation> createState() => _SubConformationState();
}

class _SubConformationState extends State<SubConformation> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
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
            child: Column(
              children: [
                SizedBox(
                  height: 400,
                ),
                Text(
                  getTranslate(context, "survey.sub_que"),
                  style: TextStyle(
                    fontSize: 16,
                    color: Color.fromARGB(217, 0, 29, 103),
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(
                  height: 390,
                ),
                Container(
                    width: 460,
                    height: 70,
                    margin: const EdgeInsets.fromLTRB(0, 10, 0, 20),
                    decoration:
                        BoxDecoration(borderRadius: BorderRadius.circular(70)),
                    child: ElevatedButton(
                      onPressed: () {
                        Navigator.pushReplacementNamed(context, '/home');
                        Navigator.of(context)
                            .pushReplacementNamed('/bottomNavi');
                      },
                      style: ButtonStyle(
                          backgroundColor:
                              MaterialStateProperty.resolveWith((states) {
                            if (states.contains(MaterialState.pressed)) {
                              return hexStringColor("#01253D");
                            }
                            return hexStringColor("#095590");
                          }),
                          shape:
                              MaterialStateProperty.all<RoundedRectangleBorder>(
                                  RoundedRectangleBorder(
                                      borderRadius:
                                          BorderRadius.circular(30)))),
                      child: Text(
                        getTranslate(context, 'survey.close'),
                        style: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 16),
                      ),
                    )),
                SizedBox(
                  height: 20,
                ),
              ],
            ),
          )),
    );
  }
}