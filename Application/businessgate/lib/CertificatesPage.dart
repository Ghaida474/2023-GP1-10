import 'package:flutter/material.dart';
import 'package:businessgate/models/model_user.dart';
import 'dart:convert';
import '../../myservice.dart';
import '../../utils/colors.dart';
import '../database/app_database.dart';
import 'package:flutter_pdfview/flutter_pdfview.dart';
import 'localization/localization_const.dart';

class CertificateViewPage extends StatefulWidget {

  const CertificateViewPage({Key? key}) : super(key: key);

  @override
  _CertificateViewPageState createState() => _CertificateViewPageState();
}

class _CertificateViewPageState extends State<CertificateViewPage> {
  List<CertificateData>? fetchedCertificate;
  MyService _myID = MyService();
  int selectedIndex = 0;

  @override
  void initState() {
    super.initState();
    fetchCertificateAndTopic();
  }

  Future<void> fetchCertificateAndTopic() async {
    try {
        fetchedCertificate = await ModelsUsers().fetchCertificationsM(_myID.myVariable2);
    } catch (error) {
      print('Error fetching certificate and topic: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text(
          getTranslate(context, 'profile.certificates'),
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
        child: FutureBuilder(
        future: fetchCertificateAndTopic(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            // Show loading indicator if data is still being fetched
            return CircularProgressIndicator();
          } else if (snapshot.hasError) {
            // Show an error message if there's an error
            return Text('Error: ${snapshot.error}');
          } else {
            // Build the UI using the fetched data
            return Container(
              height: MediaQuery.of(context).size.height,
              child: _buildCertificateView(),
            );
          }
        },
      ),
      )
    );
  }


Widget _buildCertificateView() {
  return Container(
    padding: EdgeInsets.all(16),
    decoration: BoxDecoration(
      color: Colors.transparent,
      borderRadius: BorderRadius.circular(10),
      boxShadow: [
        BoxShadow(
          color: const Color.fromARGB(255, 158, 158, 158).withOpacity(0.5),
          blurRadius: 5,
        ),
      ],
    ),
    child: Column(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        SizedBox(height: 20),
        if (fetchedCertificate != null)
          Expanded(
            child: ListView.builder(
              itemCount: fetchedCertificate!.length,
              itemBuilder: (context, index) {
                return Container(
                  margin: EdgeInsets.symmetric(vertical: 8),
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: hexStringColor("#095590"),
                    borderRadius: BorderRadius.circular(8),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.grey.withOpacity(0.3),
                        blurRadius: 3,
                        offset: Offset(0, 2),
                      ),
                    ],
                  ),
                  child: ListTile(
                    title: Text(
                      fetchedCertificate![index].programName,
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    trailing: const Icon(
        Icons.arrow_forward_ios,
        size: 18,
        color: Colors.white,
      ),
                    onTap: () {
                      setState(() {
                        selectedIndex = index; // Update the selected index
                      });

                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => CertificateDetailPage(
                            certificateData: fetchedCertificate![index].certificate,
                          ),
                        ),
                      );
                    },
                  ),
                );
              },
            ),
          ),
      ],
    ),
  );
}



}

class CertificateDetailPage extends StatelessWidget {
  final String certificateData;

  CertificateDetailPage({required this.certificateData});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
            extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text(
          getTranslate(context, 'Course.cerDetail'),
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
        child : PDFView(
        pdfData: base64Decode(certificateData),
        enableSwipe: true,
        swipeHorizontal: false,
        autoSpacing: true, // Enable autoSpacing
        pageFling: false,
        fitPolicy: FitPolicy.WIDTH, // Fit to width
        onRender: (pages) {
          // PDF document is rendered successfully
          print('Pages: $pages');
        },
        onError: (error) {
          // Handle error during PDF view
          print('Error: $error');
        },
      ),
    ));
  }
}
