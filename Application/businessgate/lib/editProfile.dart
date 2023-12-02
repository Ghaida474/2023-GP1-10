import 'package:businessgate/models/model_user.dart';
import 'package:flutter/material.dart';
import 'package:businessgate/localization/localization_const.dart';
import '../../myservice.dart';
import '../../utils/colors.dart';
import 'package:flutter_pw_validator/flutter_pw_validator.dart';

class EditProfile extends StatefulWidget {
  const EditProfile({Key? key}) : super(key: key);

  @override
  State<EditProfile> createState() => _EditProfileState();
}

class _EditProfileState extends State<EditProfile> {
  MyService _myEmail = MyService();

  bool passToggle = true;

  TextEditingController nameController = TextEditingController();
  TextEditingController lastNameController = TextEditingController();
  TextEditingController fullnameController = TextEditingController();
  TextEditingController phoneController = TextEditingController();
  TextEditingController passwordController = TextEditingController();

  bool success = false;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    nameController.text =
        await ModelsUsers().FetchFirstName(_myEmail.myVariable);

    lastNameController.text =
        await ModelsUsers().FetchLastName(_myEmail.myVariable);

    fullnameController.text =
        await ModelsUsers().FetchFullName(_myEmail.myVariable);    

    phoneController.text =
        await ModelsUsers().FetchPhoneNum(_myEmail.myVariable);

    passwordController.text =
        await ModelsUsers().FetchPassword(_myEmail.myVariable);

  }

  final formkey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return Scaffold(
        extendBodyBehindAppBar: true,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          title: Text(
            getTranslate(context, 'editProfile.edit_profile'),
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
          child: SingleChildScrollView(
            child: Padding(
              padding: EdgeInsets.fromLTRB(20, size.height * 0.2, 20, 400),
              child: Form(
                key: formkey,
                autovalidateMode: AutovalidateMode.onUserInteraction,
                child: Column(
                  children: <Widget>[
                    profileContainer(size),
                    SizedBox(height: 10),
                    userinfo(),
                    SizedBox(height: 10),
                    SizedBox(height: 10 / 2),
                    Container(
                      alignment: Alignment.centerLeft,
                      child: Text(getTranslate(context, 'editProfile.FN'),
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          )),
                    ),
                    nameField(size, context),
                    SizedBox(height: 8),
                    Container(
                      alignment: Alignment.centerLeft,
                      child: Text(getTranslate(context, 'editProfile.LN'),
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          )),
                    ),
                    emailField(size, context),
                    SizedBox(height: 8),
                    Container(
                      alignment: Alignment.centerLeft,
                      child: Text(getTranslate(context, 'editProfile.FullN'),
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          )),
                    ),
                    fullnameField(size, context),
                    SizedBox(height: 8),
                    Container(
                      alignment: Alignment.centerLeft,
                      child: Text(getTranslate(context, 'editProfile.mobile'),
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          )),
                    ),
                    phoneField(size, context),
                    SizedBox(height: 8),
                    Container(
                      alignment: Alignment.centerLeft,
                      child: Text(getTranslate(context, 'editProfile.password'),
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          )),
                    ),
                    passField("Enter Password", Icons.lock, passwordController),
                    const SizedBox(
                      height: 12,
                    ),
                    FlutterPwValidator(
                      defaultColor: Colors.grey.shade300,
                      controller: passwordController,
                      successColor: Colors.green.shade700,
                      minLength: 8,
                      uppercaseCharCount: 1,
                      numericCharCount: 1,
                      specialCharCount: 1,
                      normalCharCount: 1,
                      width: 400,
                      height: 190,
                      onSuccess: () {
                        setState(() {
                          success = true;
                        });
                      },
                      onFail: () {
                        setState(() {
                          success = false;
                        });
                      },
                    ),
                    const SizedBox(
                      height: 40,
                    ),
                    updateButton(context, () {
                      processUpdate(
                          context,
                          nameController.text,
                          lastNameController.text,
                          phoneController.text,
                          passwordController.text,
                          fullnameController.text);
                    }),
                  ],
                ),
              ),
            ),
          ),
        ));
  }

  updateButton(BuildContext context, Function onTap) {
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
            getTranslate(context, 'editProfile.update'),
            style: const TextStyle(
                color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
          ),
        ));
  }

  Future<void> processUpdate(BuildContext context, String fname, String lname,
      String phone, String pass, String full) async {
    ModelsUsers().updatefname(_myEmail.myVariable, fname).then((UpdateFN) {
      if (UpdateFN.toString().contains('not')) {
        setState(() {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              backgroundColor: Colors.white,
              elevation: 10.0,
              shape: Border.all(
                  color: Colors.red, width: 0.5, style: BorderStyle.solid),
              content: Text(
                getTranslate(context, 'editProfile.update_not'),
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
          nameController.clear();
          lastNameController.clear();
          phoneController.clear();
          passwordController.clear();
          fullnameController.clear();
        });
      } else if (UpdateFN.toString().contains('ok')) {
        setState(() {
           ModelsUsers().updatelname(_myEmail.myVariable, lname).then((UpdateLN) {
      if (UpdateLN.toString().contains('not')) {
        setState(() {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              backgroundColor: Colors.white,
              elevation: 10.0,
              shape: Border.all(
                  color: Colors.red, width: 0.5, style: BorderStyle.solid),
              content: Text(
                getTranslate(context, 'editProfile.update_not'),
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
          nameController.clear();
          lastNameController.clear();
          phoneController.clear();
          passwordController.clear();
          fullnameController.clear();
        });
      } else if (UpdateLN.toString().contains('ok')) {
        setState(() {
          ModelsUsers().updatephonenum(_myEmail.myVariable, phone).then((UpdatePN) {
      if (UpdatePN.toString().contains('not')) {
        setState(() {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              backgroundColor: Colors.white,
              elevation: 10.0,
              shape: Border.all(
                  color: Colors.red, width: 0.5, style: BorderStyle.solid),
              content: Text(
                getTranslate(context, 'editProfile.update_not'),
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
          nameController.clear();
          lastNameController.clear();
          phoneController.clear();
          passwordController.clear();
          fullnameController.clear();
        });
      } else if (UpdatePN.toString().contains('ok')) {
        setState(() {
          ModelsUsers().updatepass(_myEmail.myVariable, pass).then((UpdatePass) {
      if (UpdatePass.toString().contains('not')) {
        setState(() {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              backgroundColor: Colors.white,
              elevation: 10.0,
              shape: Border.all(
                  color: Colors.red, width: 0.5, style: BorderStyle.solid),
              content: Text(
                getTranslate(context, 'editProfile.update_not'),
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
          nameController.clear();
          lastNameController.clear();
          phoneController.clear();
          passwordController.clear();
          fullnameController.clear();
        });
      } else if (UpdatePass.toString().contains('ok')) {
        ModelsUsers().updatefullname(_myEmail.myVariable, full).then((UpdateFullN) {
      if (UpdateLN.toString().contains('not')) {
        setState(() {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              backgroundColor: Colors.white,
              elevation: 10.0,
              shape: Border.all(
                  color: Colors.red, width: 0.5, style: BorderStyle.solid),
              content: Text(
                getTranslate(context, 'editProfile.update_not'),
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
          nameController.clear();
          lastNameController.clear();
          phoneController.clear();
          passwordController.clear();
          fullnameController.clear();
        });
      }
    });
      }
    });

        });
      }
    });

        });
      }
    });
          Navigator.pushNamed(context, '/profile');
        });
      }
    });
  }

  nameField(Size size, BuildContext context) {
    return TextFormField(
      controller: nameController,
      cursorColor: Colors.white,
      style: TextStyle(color: Colors.white.withOpacity(0.9)),
      decoration: InputDecoration(
          focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30),
              borderSide: const BorderSide(
                color: Color.fromARGB(255, 2, 14, 52),
              )),
          prefixIcon: Icon(
            Icons.person,
            color: const Color.fromARGB(179, 255, 255, 255),
          ),
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
      validator: (value) {
        if (value!.isEmpty || !RegExp(r'^[a-z A-Z]+$').hasMatch(value!)) {
          return getTranslate(context, 'signup.CN');
        } else
          return null;
      },
    );
  }

  fullnameField(Size size, BuildContext context) {
    return TextFormField(
      controller: fullnameController,
      cursorColor: Colors.white,
      style: TextStyle(color: Colors.white.withOpacity(0.9)),
      decoration: InputDecoration(
          focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30),
              borderSide: const BorderSide(
                color: Color.fromARGB(255, 2, 14, 52),
              )),
          prefixIcon: Icon(
            Icons.person,
            color: const Color.fromARGB(179, 255, 255, 255),
          ),
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
              validator: (value) {
              if (value!.isEmpty) 
               return getTranslate(context, 'signup.CFull');

               return null ;
      },
    );
  }

  emailField(Size size, BuildContext context) {
    return TextFormField(
      controller: lastNameController,
      cursorColor: Colors.white,
      style: TextStyle(color: Colors.white.withOpacity(0.9)),
      decoration: InputDecoration(
          focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30),
              borderSide: const BorderSide(
                color: Color.fromARGB(255, 2, 14, 52),
              )),
          prefixIcon: Icon(
            Icons.person,
            color: const Color.fromARGB(179, 255, 255, 255),
          ),
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
      validator: (value) {
        if (value!.isEmpty || !RegExp(r'^[a-z A-Z]+$').hasMatch(value!)) {
          return getTranslate(context, 'signup.CN');
        } else
          return null;
      },
    );
  }

  phoneField(Size size, BuildContext context) {
    return TextFormField(
      controller: phoneController,
      cursorColor: Colors.white,
      style: TextStyle(color: Colors.white.withOpacity(0.9)),
      decoration: InputDecoration(
          focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30),
              borderSide: const BorderSide(
                color: Color.fromARGB(255, 2, 14, 52),
              )),
          prefixIcon: Icon(
            Icons.person,
            color: const Color.fromARGB(179, 255, 255, 255),
          ),
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
      validator: (value) {
        if (value!.isEmpty || !RegExp(r'^05\d{8}$').hasMatch(value!)) {
          return getTranslate(context, 'signup.CM');
        } else
          return null;
      },
    );
  }

  TextFormField passField(
      String text, IconData icon, TextEditingController controller) {
    return TextFormField(
      controller: controller,
      obscureText: passToggle,
      cursorColor: Colors.white,
      style: TextStyle(color: Colors.white.withOpacity(0.9)),
      decoration: InputDecoration(
          focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30),
              borderSide: const BorderSide(
                color: Color.fromARGB(255, 2, 14, 52),
              )),
          prefixIcon: Icon(
            icon,
            color: const Color.fromARGB(179, 255, 255, 255),
          ),
          suffixIcon: InkWell(
            onTap: () {
              setState(() {
                passToggle = !passToggle;
              });
            },
            child: Icon(passToggle ? Icons.visibility_off : Icons.visibility),
          ),
          hintStyle:
              TextStyle(color: Color.fromARGB(156, 0, 0, 0).withOpacity(0.9)),
          labelText: text,
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.9)),
          filled: true,
          floatingLabelBehavior: FloatingLabelBehavior.never,
          fillColor: hexStringColor("#095590").withOpacity(0.45),
          border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(30.0),
              borderSide: const BorderSide(width: 0, style: BorderStyle.none))),
      validator: (value) {
        if (value!.isEmpty ||
            !RegExp(
              r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            ).hasMatch(value!)) {
          return getTranslate(context, 'signup.CP');
        } else
          return null;
      },
    );
  }

  userinfo() {
    return Column(
      children: [
        Text(
          getTranslate(context, 'editProfile.change'),
          style: TextStyle(
              color: Colors.black, fontSize: 18, fontWeight: FontWeight.w600),
        ),
        SizedBox(height: 10 / 2),
        Text(
          _myEmail.myVariable,
          style: TextStyle(fontSize: 14, color: Colors.black),
        )
      ],
    );
  }

  profileContainer(Size size) {
    return Center(
      child: SizedBox(
        height: size.height * 0.155,
        width: size.height * 0.15,
        child: Stack(
          children: [
            Container(
              height: size.height * 0.15,
              width: size.height * 0.15,
              child: ClipRRect(
                child: Image.asset(
                  "assets/images/Profile.png",
                  color: hexStringColor("#095590"),
                  fit: BoxFit.cover,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  bottonsheetIcon(Size size, IconData icon, Color color, String text) {
    return GestureDetector(
      onTap: () {
        Navigator.pop(context);
      },
      child: Column(
        children: [
          Container(
            height: size.height * 0.07,
            width: size.height * 0.07,
            decoration: BoxDecoration(
              color: Colors.white,
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: Colors.grey.withOpacity(0.3),
                  blurRadius: 10,
                ),
              ],
            ),
            child: Icon(
              icon,
              color: color,
            ),
          ),
          SizedBox(height: 10 / 2),
          Text(text.toString(),
              style: TextStyle(
                      color: Colors.black,
                      fontSize: 16,
                      fontWeight: FontWeight.w400)
                  .copyWith(fontSize: 15),
              textAlign: TextAlign.center)
        ],
      ),
    );
  }
}
