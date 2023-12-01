import 'package:flutter/material.dart';
//import 'package:flutter_full_pdf_viewer/flutter_full_pdf_viewer.dart';
//mport 'package:flutter_cached_pdfview/flutter_cached_pdfview.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

import 'package:businessgate/models/model_user.dart';
import 'dart:convert';

import 'dart:typed_data';



import 'package:businessgate/localization/localization_const.dart';
import '../../myservice.dart';
import '../../utils/colors.dart';

import '../database/app_database.dart';
import 'dart:ffi';
import 'package:postgres/postgres.dart';

import 'dart:io';


import 'package:businessgate/theme.dart';


import 'package:flutter_pdfview/flutter_pdfview.dart';
import 'package:path_provider/path_provider.dart';

class CertificateNavigationMenu extends StatelessWidget {
  const CertificateNavigationMenu({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Certificates'),
      ),
      body: Container(
        padding: EdgeInsets.all(20),
        alignment: Alignment.center,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                navigateToCertificates(context, 1);
              },
              child: Text('Upcoming'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                navigateToCertificates(context, 2);
              },
              child: Text('Running'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                navigateToCertificates(context, 3);
              },
              child: Text('Completed'),
            ),
          ],
        ),
      ),
    );
  }

  void navigateToCertificates(BuildContext context, int choice) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => CertificateViewPage(sectionIndex: choice),
      ),
    );
  }
}



class CertificateViewPage extends StatefulWidget {
  final int sectionIndex;

  const CertificateViewPage({Key? key, required this.sectionIndex}) : super(key: key);

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
      appBar: AppBar(
        title: Text('Certificates'),
      ),
      body: FutureBuilder(
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
    );
  }


Widget _buildCertificateView() {
  return Container(
    padding: EdgeInsets.all(16),
    decoration: BoxDecoration(
      color: hexStringColor("#F5F5F5"),
      borderRadius: BorderRadius.circular(10),
      boxShadow: [
        BoxShadow(
          color: const Color.fromARGB(255, 158, 158, 158).withOpacity(0.5),
          blurRadius: 5,
        ),
      ],
    ),
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        /*
        Text(
          // maybe add trainee name
          'Certificates',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: hexStringColor("#095590"),
          ),
        ),*/
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
                    color: Colors.white,
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
                        color: hexStringColor("#095590"),
                      ),
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
      appBar: AppBar(
        title: Text('تفاصيل الشهادة'),
      ),
      body: PDFView(
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
    );
  }
}
