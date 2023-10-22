import 'package:businessgate/bottomnavigation/bottom_navigation.dart'; // Import your BottomNaviScreen
import 'package:flutter/material.dart';
import 'package:businessgate/screens/forget.dart';
import 'package:businessgate/screens/home.dart';
import 'package:businessgate/profile/editProfile.dart';
import 'package:businessgate/profile/profile.dart';
import 'package:flutter/material.dart';
import 'package:businessgate/screens/signin.dart';
import 'package:businessgate/screens/signup.dart';
import 'package:businessgate/localization/localization.dart';
import 'package:businessgate/localization/localization_const.dart';
import 'package:flutter/services.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:businessgate/bottomnavigation/bottom_navigation.dart';
void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({Key? key}) : super(key: key);

  static void setLocale(BuildContext context, Locale locale) {
    _MyAppState state = context.findAncestorStateOfType<_MyAppState>()!;
    state.setLocale(locale);
  }

  @override
  State<MyApp> createState() => _MyAppState();
}


class _MyAppState extends State<MyApp> {
   Locale? _locale;

  void setLocale(Locale locale) {
    setState(() {
      _locale = locale;
    });
  }

  @override
  void didChangeDependencies() {
    getLocale().then((locale) {
      setState(() {
        _locale = locale;
      });
    });
    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Color.fromARGB(255, 30, 67, 180)),
        useMaterial3: true,
      ),
      initialRoute: '/signin',
      

      routes: {
        '/signin': (context) => SignIn(),
        '/signup': (context) => SignUp(),
        '/home': (context) => Home(),
        '/forget': (context) => Forget(),
        '/profile': (context) => Profile(),
        '/editprofile': (context) => EditProfile(),
        '/bottomNavi': (context) => BottomNaviScreen(), 
      },
      home: BottomNaviScreen(), 
     
      locale: _locale,
      supportedLocales: const [
        Locale('en'),
        Locale('hi'),
        Locale('id'),
        Locale('zh'),
        Locale('ar'),
      ],
      localizationsDelegates: const [
        DemoLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      localeResolutionCallback: (deviceLocale, supportedLocales) {
        for (var locale in supportedLocales) {
          if (locale.languageCode == deviceLocale?.languageCode) {
            return deviceLocale;
          }
        }
        return supportedLocales.first;
      },
    );
  }
}