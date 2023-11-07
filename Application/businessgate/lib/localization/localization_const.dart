import 'package:businessgate/localization/localization.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

String getTranslate(BuildContext context, String key) {
  return DemoLocalizations.of(context).getTranslateValues(key);
}

const String english = 'en';

const String arabic = 'ar';

const String languageKey = "languageCode";

Future<Locale> setLocales(String languageCode) async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  await prefs.setString(languageKey, languageCode);
  return _locale(languageCode);
}

Locale _locale(String languageCode) {
  Locale temp;
  switch (languageCode) {
    case english:
      temp = Locale(languageCode);
      break;
    case arabic:
      temp = Locale(languageCode);
      break;
    default:
      temp = const Locale(english);
  }
  return temp;
}

Future<Locale> getLocale() async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  String languageCode = prefs.getString(languageKey) ?? english;
  return _locale(languageCode);
}
