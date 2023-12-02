class MyService {

  static final MyService _instance = MyService._internal();

  // passes the instantiation to the _instance object
  factory MyService() => _instance;

    String _myVariable = '';
    int _myVariable2 = 0;
    int _myVariable3 = 0;
    String _filter = '';

  //initialize variables in here
  MyService._internal() {
    _myVariable = 'no value';
  }

  //short getter for my variable
  String get myVariable => _myVariable;

  //short setter for my variable
  set myVariable(String value) {
     _myVariable = value;
  }
  
//short getter for my variable
  int get myVariable2 => _myVariable2;

  //short setter for my variable
  set myVariable2(int value) {
     _myVariable2 = value;
  }

  //short getter for my variable
  int get myVariable3 => _myVariable3;

  //short setter for my variable
  set myVariable3(int value) {
     _myVariable3 = value;
  }

    //getter for _filter
  String get Filter => _filter;

  //setter for _filter
  set Filter(String value) {
    _filter = value;
  }
}
