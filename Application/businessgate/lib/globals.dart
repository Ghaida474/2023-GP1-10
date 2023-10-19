class Globals {
  // Create a private constructor to prevent direct instantiation
  Globals._();

  // Create a static instance of the class
  static final Globals _instance = Globals._();

  // Getter to access the instance
  static Globals get instance => _instance;

  // Add your global variables here
  static String globalEmailString = "";

  void updateGlobalEmail(String newEmail) {
  Globals.globalEmailString = newEmail;
}
}
