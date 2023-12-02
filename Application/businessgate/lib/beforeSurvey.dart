import 'package:businessgate/models/model_user.dart';
import 'package:businessgate/myservice.dart';
import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';
import 'localization/localization_const.dart';

class bSurvey extends StatefulWidget {
  const bSurvey({super.key});

  @override
  State<bSurvey> createState() => _bSurveyState();
}

enum Choice { yes, no }

class _bSurveyState extends State<bSurvey> {
  final formkey = GlobalKey<FormState>();

  Choice selectedChoice1 = Choice.yes;
  Choice selectedChoice2 = Choice.yes;
  Choice selectedChoice5 = Choice.yes;

  // Value received from the route
  int? receivedValue;

  TextEditingController _q3TextController = TextEditingController();
  TextEditingController _q4TextController = TextEditingController();

  MyService _myEmail = MyService();

  @override
  Widget build(BuildContext context) {
    
    receivedValue = ModalRoute.of(context)?.settings.arguments as int?;

    return Scaffold(
        extendBodyBehindAppBar: true,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          title: Text(
            getTranslate(context, 'survey.before'),
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
                                getTranslate(context, 'survey.BQ1'),
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
                                  groupValue: selectedChoice1,
                                  onChanged: (value) {
                                    setState(() {
                                      selectedChoice1 = value!;
                                    });
                                  },
                                ),
                                RadioListTile(
                                  title:
                                      Text(getTranslate(context, 'survey.no')),
                                  value: Choice.no,
                                  groupValue: selectedChoice1,
                                  onChanged: (value) {
                                    setState(() {
                                      selectedChoice1 = value!;
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
                        height: 215,
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
                              getTranslate(context, 'survey.BQ2'),
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
                                  groupValue: selectedChoice2,
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
                                  groupValue: selectedChoice2,
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
                        width:
                            500, 
                        height: 190,
                        decoration: BoxDecoration(
                          border: Border.all(
                            color:
                                Colors.black, 
                          ),
                          borderRadius: BorderRadius.circular(
                              10.0), 
                        ),
                        padding: EdgeInsets.all(
                            10.0), 
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              getTranslate(context, 'survey.BQ3'),
                              style: TextStyle(
                                fontSize: 18,
                                color: Color.fromARGB(217, 0, 29, 103),
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(
                              height: 20,
                            ),
                            textField(
                              getTranslate(context, 'survey.answer'),
                              _q3TextController,
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(
                        height: 20,
                      ),
                      Container(
                        width:
                            500, 
                        height: 170,
                        decoration: BoxDecoration(
                          border: Border.all(
                            color:
                                Colors.black, 
                          ),
                          borderRadius: BorderRadius.circular(
                              10.0), 
                        ),
                        padding: EdgeInsets.all(10.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              getTranslate(context, 'survey.BQ4'),
                              style: TextStyle(
                                fontSize: 18,
                                color: Color.fromARGB(217, 0, 29, 103),
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(
                              height: 20,
                            ),
                            textField(
                              getTranslate(context, 'survey.answer'),
                              _q4TextController,
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(
                        height: 20,
                      ),
                      Container(
                        width:
                            500, 
                        height: 190,
                        decoration: BoxDecoration(
                          border: Border.all(
                            color:
                                Colors.black, 
                          ),
                          borderRadius: BorderRadius.circular(
                              10.0), 
                        ),
                        padding: EdgeInsets.all(10.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Text(
                              getTranslate(context, 'survey.BQ5'),
                              style: TextStyle(
                                fontSize: 18,
                                color: Color.fromARGB(217, 0, 29, 103),
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            RadioListTile(
                              title: Text(getTranslate(context, 'survey.yes')),
                              value: Choice.yes,
                              groupValue: selectedChoice5,
                              onChanged: (value) {
                                setState(() {
                                  selectedChoice5 = value!;
                                });
                              },
                            ),
                            RadioListTile(
                              title: Text(getTranslate(context, 'survey.no')),
                              value: Choice.no,
                              groupValue: selectedChoice5,
                              onChanged: (value) {
                                setState(() {
                                  selectedChoice5 = value!;
                                });
                              },
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(
                        height: 20,
                      ),
                      Register(context, () {
                        processAnswers(context);
                        Navigator.pushReplacementNamed(context, '/regConfirm');
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

  Future<void> processAnswers(BuildContext context) async {

    List<String> parts1 = selectedChoice1.toString().split('.');
    String choice1String = parts1.last;

    List<String> parts2 = selectedChoice2.toString().split('.');
    String choice2String = parts2.last;

    List<String> parts5 = selectedChoice5.toString().split('.');
    String choice5String = parts5.last;
  
      ModelsUsers()
          .Register(
            choice1String, 
            choice2String,
            _q3TextController.text,
            _q4TextController.text,
            choice5String,
            _myEmail.myVariable,
            receivedValue)
          .then((register) {
         if (register.toString().contains('not')) {
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
            _q3TextController.clear();
            _q4TextController.clear();

            Navigator.pushNamed(context, '/bfSurvey'); 
          });
        } 
  });
}
}
