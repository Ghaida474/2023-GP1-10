import 'package:businessgate/models/model_user.dart';
import 'package:businessgate/myservice.dart';
import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';

import 'localization/localization_const.dart';

class aSurvey extends StatefulWidget {
  const aSurvey({super.key});

  @override
  State<aSurvey> createState() => _aSurveyState();
}

enum Choice { yes, no }

class _aSurveyState extends State<aSurvey> {
  final formkey = GlobalKey<FormState>();

  Choice selectedChoice1 = Choice.yes;
  Choice selectedChoice2 = Choice.yes;
  Choice selectedChoice3 = Choice.yes;
  Choice selectedChoice4 = Choice.yes;

  // Value received from the route
  int? receivedValue;

  MyService _myEmail = MyService();

  TextEditingController _q5TextController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    receivedValue = ModalRoute.of(context)?.settings.arguments as int?;

    return Scaffold(
        extendBodyBehindAppBar: true,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          title: Text(
            getTranslate(context, 'survey.after'),
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
        ),
        body: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
                colors: [hexStringColor("#6FBCF6"), hexStringColor("#E3E0D2")],
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter),
          ),
          child: SingleChildScrollView(
            child: Padding(
                padding: EdgeInsets.fromLTRB(
                    20, MediaQuery.of(context).size.height * 0.18, 20, 280),
                child: Form(
                  key: formkey,
                  child: Column(
                    children: [
                      Container(
                        width: 500,
                        height: 210,
                        decoration: BoxDecoration(
                          border: Border.all(
                            color: Colors.black,
                          ),
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                        padding: EdgeInsets.all(10.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Text(
                                getTranslate(context, 'survey.AFQ1'),
                                style: TextStyle(
                                  fontSize: 18,
                                  color: Color.fromARGB(217, 0, 29, 103),
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                            Column(
                              children: <Widget>[
                                RadioListTile(
                                  title:
                                      Text(getTranslate(context, 'survey.yes')),
                                  value: Choice.yes,
                                  groupValue: null,
                                  onChanged: (value) {
                                    setState(() {
                                      selectedChoice1 = value as Choice;
                                    });
                                  },
                                ),
                                RadioListTile(
                                  title:
                                      Text(getTranslate(context, 'survey.no')),
                                  value: Choice.no,
                                  groupValue: null,
                                  onChanged: (value) {
                                    setState(() {
                                      selectedChoice1 = value as Choice;
                                    });
                                  },
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(
                        height: 20,
                      ),
                      Container(
                        width: 500,
                        height: 200,
                        decoration: BoxDecoration(
                          border: Border.all(
                            color: Colors.black,
                          ),
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                        padding: EdgeInsets.all(10.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Text(
                              getTranslate(context, 'survey.AFQ2'),
                              style: TextStyle(
                                fontSize: 18,
                                color: Color.fromARGB(217, 0, 29, 103),
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            Column(
                              children: <Widget>[
                                RadioListTile(
                                  title:
                                      Text(getTranslate(context, 'survey.yes')),
                                  value: Choice.yes,
                                  groupValue: null,
                                  onChanged: (value) {
                                    setState(() {
                                      selectedChoice2 = value!;
                                    });
                                  },
                                ),
                                RadioListTile(
                                  title:
                                      Text(getTranslate(context, 'survey.no')),
                                  value: Choice.no,
                                  groupValue: null,
                                  onChanged: (value) {
                                    setState(() {
                                      selectedChoice2 = value!;
                                    });
                                  },
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(
                        height: 20,
                      ),
                      Container(
                        width: 500,
                        height: 200,
                        decoration: BoxDecoration(
                          border: Border.all(
                            color: Colors.black,
                          ),
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                        padding: EdgeInsets.all(10.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: <Widget>[
                            Text(
                              getTranslate(context, 'survey.AFQ3'),
                              style: TextStyle(
                                fontSize: 18,
                                color: Color.fromARGB(217, 0, 29, 103),
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            RadioListTile(
                              title: Text(getTranslate(context, 'survey.yes')),
                              value: Choice.yes,
                              groupValue: null,
                              onChanged: (value) {
                                setState(() {
                                  selectedChoice3 = value!;
                                });
                              },
                            ),
                            RadioListTile(
                              title: Text(getTranslate(context, 'survey.no')),
                              value: Choice.no,
                              groupValue: null,
                              onChanged: (value) {
                                setState(() {
                                  selectedChoice3 = value!;
                                });
                              },
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(
                        height: 20,
                      ),
                      Container(
                        width: 500,
                        height: 200,
                        decoration: BoxDecoration(
                          border: Border.all(
                            color: Colors.black,
                          ),
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                        padding: EdgeInsets.all(10.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              getTranslate(context, 'survey.AFQ4'),
                              style: TextStyle(
                                fontSize: 18,
                                color: Color.fromARGB(217, 0, 29, 103),
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            Column(
                              children: <Widget>[
                                RadioListTile(
                                  title:
                                      Text(getTranslate(context, 'survey.yes')),
                                  value: Choice.yes,
                                  groupValue: null,
                                  onChanged: (value) {
                                    setState(() {
                                      selectedChoice4 = value!;
                                    });
                                  },
                                ),
                                RadioListTile(
                                  title:
                                      Text(getTranslate(context, 'survey.no')),
                                  value: Choice.no,
                                  groupValue: null,
                                  onChanged: (value) {
                                    setState(() {
                                      selectedChoice4 = value!;
                                    });
                                  },
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(
                        height: 20,
                      ),
                      Container(
                        width: 500,
                        height: 190,
                        decoration: BoxDecoration(
                          border: Border.all(
                            color: Colors.black,
                          ),
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                        padding: EdgeInsets.all(10.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              getTranslate(context, 'survey.AFQ5'),
                              style: TextStyle(
                                fontSize: 18,
                                color: Color.fromARGB(217, 0, 29, 103),
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 20),
                            textField(
                              getTranslate(context, 'survey.answer'),
                              _q5TextController,
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(
                        height: 20,
                      ),
                      Register(context, () {
                        //processAnswers(context);
                        Navigator.pushReplacementNamed(context, '/subConfirm');
                      })
                    ],
                  ),
                )),
          ),
        ));
  }

  TextFormField textField(String text, TextEditingController controller) {
    return TextFormField(
      controller: controller,
      cursorColor: Colors.white,
      style: TextStyle(color: Colors.white.withOpacity(0.9)),
      decoration: InputDecoration(
          focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30),
              borderSide: const BorderSide(
                color: Color.fromARGB(255, 2, 14, 52),
              )),
          labelText: text,
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
      validator: (value) {
        if (value!.isEmpty) {
          return getTranslate(context, 'survey.empty');
        } else
          return null;
      },
    );
  }

  Container Register(BuildContext context, Function onTap) {
    return Container(
        width: MediaQuery.of(context).size.width,
        height: 50,
        margin: const EdgeInsets.fromLTRB(0, 10, 0, 20),
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(70)),
        child: ElevatedButton(
          onPressed: () {
            if (formkey.currentState!.validate()) {
              onTap();
            }
          },
          style: ButtonStyle(
              backgroundColor: MaterialStateProperty.resolveWith((states) {
                if (states.contains(MaterialState.pressed)) {
                  return hexStringColor("#01253D");
                }
                return hexStringColor("#095590");
              }),
              shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                  RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30)))),
          child: Text(
            getTranslate(context, 'survey.submit'),
            style: const TextStyle(
                color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
          ),
        ));
  }

  /* Future<void> processAnswers(BuildContext context) async {

    List<String> parts1 = selectedChoice1.toString().split('.');
    String choice1String = parts1.last;

    List<String> parts2 = selectedChoice2.toString().split('.');
    String choice2String = parts2.last;

    List<String> parts3 = selectedChoice3.toString().split('.');
    String choice3String = parts3.last;

    List<String> parts4 = selectedChoice4.toString().split('.');
    String choice4String = parts4.last;
  
      ModelsUsers()
          .answerModelA(
            choice1String, 
            choice2String,
            choice3String,
            choice4String,
            _q5TextController.text,
            _myEmail.myVariable,
            receivedValue)
          .then((submit) {
         if (submit.toString().contains('not')) {
          setState(() {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                backgroundColor: Colors.white,
                elevation: 10.0,
                shape: Border.all(
                    color: Colors.red, width: 0.5, style: BorderStyle.solid),
                content: Text(
                  getTranslate(context, 'survey.problem'),
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 16.0,
                    fontWeight: FontWeight.bold,
                    fontStyle: FontStyle.italic,
                    letterSpacing: 1.0,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            );

            _q5TextController.clear();

            Navigator.pushNamed(context, '/afSurvey'); 
          });
        }
  });
}*/
}
