import 'package:businessgate/CertificatesPage.dart';
import 'package:businessgate/afterSurvey.dart';
import 'package:businessgate/allCourses.dart';
import 'package:businessgate/beforeSurvey.dart';
import 'package:businessgate/bottomnavigation/bottom_navigation.dart';
import 'package:businessgate/category.dart';
import 'package:businessgate/course.dart';
import 'package:businessgate/filterPrograms.dart';
import 'package:businessgate/languages.dart';
import 'package:businessgate/myCourses.dart';
import 'package:businessgate/regConfirm.dart';
import 'package:businessgate/subConfirm.dart';
import 'package:flutter/material.dart';
import 'package:businessgate/screens/forget.dart';
import 'package:businessgate/screens/home.dart';
import 'package:businessgate/editProfile.dart';
import 'package:businessgate/profile.dart';
import 'package:businessgate/screens/signin.dart';
import 'package:businessgate/screens/signup.dart';
import 'package:businessgate/localization/localization.dart';
import 'package:businessgate/localization/localization_const.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

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
      navigatorKey: navigatorKey,
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme:
            ColorScheme.fromSeed(seedColor: Color.fromARGB(255, 30, 67, 180)),
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
        '/languages': (context) => Languages(),
        '/allCourses': (context) => allCourses(),
        '/course': (context) => Course(),
        '/category': (context) => CategoryScreen(),
        '/bfSurvey': (context) => bSurvey(),
        '/afSurvey': (context) => aSurvey(),
        '/regConfirm': (context) => RegConformation(),
        '/subConfirm': (context) => SubConformation(),
        '/filteredPrograms': (context) => filteredPrograms(),
        '/certificates': (context) => CertificateViewPage(),
        '/myCourses': (context) => myCoursesNavigationMenu(),
      },
      home: BottomNaviScreen(),
      locale: _locale,
      supportedLocales: const [
        Locale('en'),
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
