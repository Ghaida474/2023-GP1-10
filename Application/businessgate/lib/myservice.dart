class MyService {

  static final MyService _instance = MyService._internal();

  // passes the instantiation to the _instance object
  factory MyService() => _instance;

    String _myVariable = '';

  //initialize variables in here
  MyService._internal() {
    _myVariable = 'no value';
  }

  //short getter for my variable
  String get myVariable => _myVariable;

  //short setter for my variable
  set myVariable(String value) => myVariable = value;

}
