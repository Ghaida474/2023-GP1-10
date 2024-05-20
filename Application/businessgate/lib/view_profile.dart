import 'package:businessgate/localization/localization_const.dart';
import 'package:businessgate/theme.dart';
import 'package:businessgate/utils/colors.dart';
import 'package:flutter/material.dart';

class ViewProfile extends StatefulWidget {
  const ViewProfile({Key? key}) : super(key: key);

  @override
  State<ViewProfile> createState() => _ViewProfileState();
}

class _ViewProfileState extends State<ViewProfile>
    with SingleTickerProviderStateMixin {
  TabController? tabController;

  @override
  void initState() {
    super.initState();
    tabController = TabController(length: 2, vsync: this);
  }

  final courseslist = [
    {
      "image": "assets/program/Rectangle 26-1.png",
      "name": "Web Development",
      "price": "300SAR",
      "review": 125
    },
    {
      "image": "assets/program/Rectangle 26.png",
      "name": "UX Design",
      "price": "450SAR",
      "review": 125
    }, /*
    {
      "image": "assets/program/Rectangle 26 (1).png",
      "name": "React- The Complete Guide",
      "price": "\$45",
      "review": 125
    },
    {
      "image": "assets/program/Rectangle 26 (2).png",
      "name": "Javascrip Zero To Hero",
      "price": "\$45",
      "review": 125
    },
    {
      "image": "assets/program/Rectangle 26 (3).png",
      "name": "Learn Paython Programmming",
      "price": "\$45",
      "review": 125
    },
    {
      "image": "assets/program/Rectangle 26 (4).png",
      "name": "Web Development Course 2021",
      "price": "\$45",
      "review": 125
    },
    {
      "image": "assets/program/Rectangle 26 (5).png",
      "name": "The Paython Mega Course",
      "price": "\$45",
      "review": 125
    },
    {
      "image": "assets/program/Rectangle 26 (6).png",
      "name": "Html Course",
      "price": "\$45",
      "review": 125
    },*/
  ];

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return Scaffold(
      backgroundColor: hexStringColor("#E3E0D2"),
      appBar: AppBar(
        centerTitle: false,
        backgroundColor: Colors.transparent,
        shadowColor: grey94Color.withOpacity(0.3),
        leading: IconButton(
          onPressed: () {
            Navigator.pop(context);
          },
          icon: const Icon(
            Icons.arrow_back_ios,
            size: 22,
            color: blackColor,
          ),
        ),
        titleSpacing: 0,
      ),
      body: Column(
        children: [
          profileContainer(size),
          height5Space,
          tabs(size),
          Expanded(
            child: TabBarView(
              controller: tabController,
              children: [
                firstTabview(size),
                secondTabView(size),
              ],
            ),
          )
        ],
      ),
    );
  }

  secondTabView(Size size) {
    return ListView.builder(
      shrinkWrap: true,
      physics: const BouncingScrollPhysics(),
      itemCount: courseslist.length,
      padding: const EdgeInsets.all(fixPadding),
      itemBuilder: (context, index) {
        return InkWell(
          onTap: () {
            Navigator.pushNamed(context, '/detail');
          },
          child: Container(
            margin: const EdgeInsets.all(fixPadding),
            padding: const EdgeInsets.all(fixPadding / 1.5),
            decoration: BoxDecoration(
              color: whiteColor,
              borderRadius: BorderRadius.circular(10),
              boxShadow: [
                BoxShadow(
                  color: grey94Color.withOpacity(0.5),
                  blurRadius: 5,
                ),
              ],
            ),
            child: Row(
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: Image.asset(
                    courseslist[index]['image'].toString(),
                    width: size.width * 0.24,
                  ),
                ),
                widthSpace,
                width5Space,
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Text(
                        courseslist[index]['name'].toString(),
                        style: black16Stylew600,
                      ),
                      height5Space,
                      Row(
                        children: [
                          for (int i = 0; i < 5; i++)
                            ShaderMask(
                              shaderCallback: (bounds) {
                                return const LinearGradient(
                                  colors: gradient,
                                  begin: Alignment.topCenter,
                                  end: Alignment.bottomCenter,
                                ).createShader(bounds);
                              },
                              child: const Padding(
                                padding: EdgeInsets.only(right: fixPadding / 5),
                                child: Icon(
                                  Icons.star,
                                  size: 17,
                                  color: whiteColor,
                                ),
                              ),
                            ),
                          Text(
                            "(${courseslist[index]['review']} ${getTranslate(context, 'view_profile.review')})",
                            style: grey14Style,
                          ),
                        ],
                      ),
                      height5Space,
                      Text(
                        courseslist[index]['price'].toString(),
                        style: black16Stylew600,
                      )
                    ],
                  ),
                )
              ],
            ),
          ),
        );
      },
    );
  }

  firstTabview(Size size) {
    return ListView(
      shrinkWrap: true,
      physics: const BouncingScrollPhysics(),
      children: [
        Container(
          width: double.maxFinite,
          margin: const EdgeInsets.all(fixPadding * 2),
          padding: const EdgeInsets.all(fixPadding * 1.5),
          decoration: BoxDecoration(
            color: whiteColor,
            borderRadius: BorderRadius.circular(10),
            boxShadow: [
              BoxShadow(
                color: grey94Color.withOpacity(0.5),
                blurRadius: 5,
              )
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                getTranslate(context, "view_profile.about_margarita"),
                style: black16Stylew600,
              ),
              heightSpace,
              const Text(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin mauris quis venenatis accumsan suspendisse rutrum sit. Porta egestas turpis odio ultrices. Ut congue tempor, eget viverra aliquam dolor faucibus. Consectetur ipsum, pellentesque quis mi neque pellentesque neque, id faucibus. Donec nec faucibus aliquam tortor, arcu viverra tincidunt aliquam. Lectus enim, egestas fermentum odio.",
                style: grey14Style,
              ),
              heightSpace,
            ],
          ),
        ),
      ],
    );
  }

  tabs(Size size) {
    return Stack(
      children: [
        Container(
          height: size.height * 0.08,
          decoration: const BoxDecoration(
            border: Border(
              bottom: BorderSide(
                color: Color(0xffC4C4C4),
                width: 3,
              ),
            ),
          ),
        ),
        SizedBox(
          height: size.height * 0.08,
          child: TabBar(
            controller: tabController,
            unselectedLabelColor: grey94Color,
            labelStyle: primary16Style,
            labelColor: primaryColor,
            unselectedLabelStyle: grey16Style,
            indicatorColor: primaryColor,
            indicatorWeight: 3,
            labelPadding: const EdgeInsets.only(left: 0, right: 0),
            indicator: const ShapeDecoration(
                shape: UnderlineInputBorder(
                    borderSide: BorderSide(
                  color: Colors.transparent,
                  width: 0,
                )),
                gradient: LinearGradient(colors: gradient)),
            tabs: [
              Container(
                height: size.height * 0.08,
                alignment: Alignment.center,
                color: Colors.white,
                child: Text(getTranslate(context, 'view_profile.about')),
              ),
              Container(
                height: size.height * 0.08,
                alignment: Alignment.center,
                color: Colors.white,
                child: Text(getTranslate(context, 'view_profile.course')),
              ),
            ],
          ),
        ),
      ],
    );
  }

  profileContainer(Size size) {
    return Container(
      height: size.height * 0.28,
      margin: const EdgeInsets.only(
          top: fixPadding * 2, left: fixPadding * 2, right: fixPadding * 2),
      child: Stack(
        children: [
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              height: size.height * 0.23,
              width: double.infinity,
              padding: const EdgeInsets.all(fixPadding * 2),
              decoration: BoxDecoration(
                color: whiteColor,
                borderRadius: BorderRadius.circular(10),
                boxShadow: [
                  BoxShadow(
                    color: grey94Color.withOpacity(0.5),
                    blurRadius: 5,
                  ),
                ],
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  heightbox(size.height * 0.03),
                  Column(
                    children: [
                      Text(
                        getTranslate(context, 'view_profile.name'),
                        style: black16Stylew600,
                      ),
                    ],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        children: [
                          const Text(
                            "20",
                            style: black16Stylew600,
                          ),
                          Text(
                            getTranslate(context, 'view_profile.course'),
                            style: grey14Style,
                          )
                        ],
                      ),
                      Column(
                        children: [
                          const Row(
                            children: [
                              Icon(
                                Icons.star,
                                size: 18,
                                color: Color(0xffFFCE31),
                              ),
                              Text(
                                "4.5",
                                style: black16Stylew600,
                              ),
                              Text("(125)", style: grey16Stylew400)
                            ],
                          ),
                          Text(
                            getTranslate(
                                context, 'view_profile.average_rating'),
                            style: grey14Style,
                          )
                        ],
                      )
                    ],
                  ),
                ],
              ),
            ),
          ),
          /*Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: Column(
              children: [
                Container(
                  height: size.height * 0.11,
                  width: size.height * 0.11,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(100),
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(100),
                    child: Image.asset(
                      "assets/detail/Ellipse 5.png",
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
              ],
            ),
          ),*/
        ],
      ),
    );
  }
}
