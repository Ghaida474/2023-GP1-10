class MyService {
  static final MyService _instance = MyService._internal();

  // passes the instantiation to the _instance object
  factory MyService() => _instance;

  String _myVariable = '';
  String _filter = '';
  int _myVariable2 = 0;

  //initialize variable
  MyService._internal() {
    _myVariable = 'no value';
  }

  //getter for my variable
  String get myVariable => _myVariable;

  //setter for my variable
  set myVariable(String value) {
    _myVariable = value;
  }

  //getter for _filter
  String get Filter => _filter;

  //setter for _filter
  set Filter(String value) {
    _filter = value;
  }

  int get myVariable2 => _myVariable2;

  set myVariable2(int value) {
    _myVariable2 = value;
  }
}
