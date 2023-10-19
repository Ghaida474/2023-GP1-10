import 'package:businessgate/theme.dart';
import 'package:flutter/material.dart';

class Home extends StatefulWidget {
  const Home({Key? key}) : super(key: key);

  @override
  State<Home> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<Home> {
  final category = [
    {
      "name": "Business",
      "icon": Icons.add_business_outlined,
      "color": const Color(0xff6B97F8),
      "isimage": false,
    },
    {
      "name": "Design",
      "icon": Icons.design_services_outlined,
      "color": const Color(0xff15A812),
      "isimage": false,
    },
    
    {
      "name": "Marketing",
      "icon": Icons.medical_services_rounded,
      "color": const Color(0xffAD5C5C),
      "isimage": true,
      "image": "assets/home/nimbus_marketing.png",
    },
  ];

  final recommeded = [
    {
      "name": "Web Development Course",
      "price": "\$45",
      "review": 125,
      "image": "assets/home/web.jpg",
    },
    {
      "name": "The Web devlopment bootcamp",
      "price": "\$45",
      "review": 125,
      "image": "assets/home/web.jpg",
    }
  ];

  

  final popular = [
    {
      "image": "assets/home/Rectangle 14.png",
      "course": "Google ux design",
      "name": "Albert portila",
      "review": 125,
      "Price": "\$25.00",
    },
    {
      "image": "assets/home/Rectangle 14.png",
      "course": "Google ux design",
      "name": "Albert portila",
      "review": 125,
      "Price": "\$25.00",
    },
    {
      "image": "assets/home/Rectangle 14.png",
      "course": "Data science",
      "name": "Albert portila",
      "review": 125,
      "Price": "\$25.00",
    }
  ];

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return Scaffold(
      backgroundColor: whiteColor,
      appBar: AppBar(
        centerTitle: false,
        automaticallyImplyLeading: false,
        backgroundColor: whiteColor,
        toolbarHeight: size.height * 0.085,
        elevation: 3,
        shadowColor: Colors.grey.withOpacity(0.3),
        title: Row(
          children: [
            Container(
              height: size.height * 0.07,
              width: size.height * 0.07,
              padding: const EdgeInsets.all(1.5),
              decoration: const BoxDecoration(
               // gradient: LinearGradient(colors: gradient),
                shape: BoxShape.circle,
              ),
              child: const CircleAvatar(
                  backgroundImage: AssetImage("assets/profile/Logo.jpg")),
            ),
            widthSpace,
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Hello Lina",
                  style: black16Style,
                ),
                heightbox(2),
              ],
            )
          ],
        ),
        actions: [
          SizedBox(
            height: 50,
            width: 50,
            child: Stack(
              children: [
                IconButton(
                  onPressed: () {
                    Navigator.pushNamed(context, '/notification');
                  },
                  icon: const Icon(
                    Icons.notifications,
                    color: Colors.black,
                  ),
                ),
                Positioned(
                  right: 18,
                  top: 15,
                  child: Container(
                    height: 6,
                    width: 6,
                    decoration: const BoxDecoration(
                      color: Color.fromARGB(255, 222, 228, 235),
                      shape: BoxShape.circle,
                    ),
                  ),
                ),
              ],
            ),
          )
        ],
      ),
      body: ListView(
        physics: const BouncingScrollPhysics(),
        children: [
          topContainer(size),
          categorytext(),
          categoryList(size),
          height5Space,
          recommededText(),
          recommededList(size),
          popularText(),
          poularlist(size),
          height5Space,
        
        ],
      ),
    );
  }

  featureText() {
    return Padding(
      padding: const EdgeInsets.symmetric(
        vertical: fixPadding,
        horizontal: fixPadding * 2,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            "Feature Course",
            style: black18Style,
          ),
        ],
      ),
    );
  }

 

  poularlist(Size size) {
    return Column(
      children: [
        GestureDetector(
          onTap: () {
            Navigator.pushNamed(context, '/detail');
          },
          child: Container(
            margin: const EdgeInsets.only(
                left: fixPadding * 2,
                right: fixPadding * 2,
                bottom: fixPadding * 2,
                top: fixPadding),
            height: size.height * 0.29,
            decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(10),
                color: whiteColor,
                boxShadow: [
                  BoxShadow(
                    color: grey94Color.withOpacity(0.5),
                    blurRadius: 5,
                  )
                ]),
            child: Column(
              children: [
                ClipRRect(
                  borderRadius: const BorderRadius.vertical(
                    top: Radius.circular(10),
                  ),
                  child: Image.asset(
                    "assets/home/Rectangle 14.png",
                    height: size.height * 0.16,
                    width: double.infinity,
                    fit: BoxFit.cover,
                  ),
                ),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(fixPadding),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Text(
                              "Google ux design",
                              style: black16Stylew600,
                              overflow: TextOverflow.ellipsis,
                            ),
                            Row(
                              children: [
                                for (int i = 0; i < 5; i++)
                                  ShaderMask(
                                    shaderCallback: (Rect bounds) {
                                      return const LinearGradient(
                                        colors: gradient,
                                        begin: Alignment.topCenter,
                                        end: Alignment.bottomCenter,
                                      ).createShader(bounds);
                                    },
                                    child: const Padding(
                                      padding: EdgeInsets.only(
                                          right: fixPadding / 5),
                                      child: Icon(
                                        Icons.star,
                                        size: 15,
                                        color: whiteColor,
                                      ),
                                    ),
                                  ),
                                const Text(
                                  "(125)",
                                  style: grey14Style,
                                )
                              ],
                            ),
                          ],
                        ),
                        const Text(
                          "Albert portila",
                          style: grey14Style,
                        ),
                        const Text(
                          "\$25.00",
                          style: primary16Style,
                        )
                      ],
                    ),
                  ),
                )
              ],
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: fixPadding),
          child: Row(
            children: [
              poularIcon2(
                  size, "assets/home/Rectangle 14 (1).png", "Google ux design"),
              poularIcon2(
                  size, "assets/home/Rectangle 14 (2).png", "Data science"),
            ],
          ),
        ),
      ],
    );
  }

  poularIcon2(Size size, String image, String name) {
    return Expanded(
      child: GestureDetector(
        onTap: () {
          Navigator.pushNamed(context, '/detail');
        },
        child: Container(
          margin: const EdgeInsets.symmetric(horizontal: fixPadding),
          height: size.height * 0.32,
          decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(10),
              color: whiteColor,
              boxShadow: [
                BoxShadow(
                  color: grey94Color.withOpacity(0.5),
                  blurRadius: 5,
                )
              ]),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              ClipRRect(
                borderRadius: const BorderRadius.vertical(
                  top: Radius.circular(10),
                ),
                child: Image.asset(
                  image,
                  height: size.height * 0.16,
                  width: double.infinity,
                  fit: BoxFit.cover,
                ),
              ),
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.all(fixPadding),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        name,
                        style: black16Stylew600,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const Text(
                        "Albert portila",
                        style: grey14Style,
                      ),
                      Row(
                        children: [
                          for (int i = 0; i < 5; i++)
                            ShaderMask(
                              shaderCallback: (Rect bounds) {
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
                                  size: 15,
                                  color: whiteColor,
                                ),
                              ),
                            ),
                          const Text(
                            "(125)",
                            style: grey14Style,
                          ),
                        ],
                      ),
                      const Text(
                        "\$25.00",
                        style: primary16Style,
                      )
                    ],
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }

  popularText() {
    return Padding(
      padding: const EdgeInsets.symmetric(
        vertical: fixPadding,
        horizontal: fixPadding * 2,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            "Popular Courses",
            style: black18Style,
          ),
          GestureDetector(
            onTap: () {
              Navigator.pushNamed(context, '/popular');
            },
            child: Text("See all",
                style: primary14Style),
          )
        ],
      ),
    );
  }

  recommededList(Size size) {
    return Column(
      children: recommeded
          .map(
            (e) => GestureDetector(
              onTap: () {
                Navigator.pushNamed(context, '/detail');
              },
              child: Container(
                width: double.infinity,
                margin: const EdgeInsets.symmetric(
                  horizontal: fixPadding * 2,
                  vertical: fixPadding,
                ),
                padding: const EdgeInsets.all(fixPadding / 1.5),
                decoration: BoxDecoration(
                  color: whiteColor,
                  boxShadow: [
                    BoxShadow(
                      color: grey94Color.withOpacity(0.5),
                      blurRadius: 5,
                    ),
                  ],
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Row(
                  children: [
                    ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: Image.asset(
                        e['image'].toString(),
                        fit: BoxFit.cover,
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
                            e["name"].toString(),
                            style: black16Stylew600,
                          ),
                          height5Space,
                          Row(
                            children: [
                              for (int i = 0; i < 5; i++)
                                ShaderMask(
                                  shaderCallback: (Rect bounds) {
                                    return const LinearGradient(
                                      colors: gradient,
                                      begin: Alignment.topCenter,
                                      end: Alignment.bottomCenter,
                                    ).createShader(bounds);
                                  },
                                  child: const Padding(
                                    padding:
                                        EdgeInsets.only(right: fixPadding / 5),
                                    child: Icon(
                                      Icons.star,
                                      size: 17,
                                      color: whiteColor,
                                    ),
                                  ),
                                ),
                              Text(
                                "(${e['review']} ${ 'Review'})",
                                style: grey14Style,
                              )
                            ],
                          ),
                          height5Space,
                          Text(
                            e['price'].toString(),
                            style: black16Stylew600,
                          )
                        ],
                      ),
                    )
                  ],
                ),
              ),
            ),
          )
          .toList(),
    );
  }

  recommededText() {
    return Padding(
      padding: const EdgeInsets.symmetric(
        vertical: fixPadding,
        horizontal: fixPadding * 2,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            "Recommended",
            style: black18Style,
          ),
          GestureDetector(
            onTap: () {
              Navigator.pushNamed(context, '/recommended');
            },
            child: Text("See all",
                style: primary14Style),
          ),
        ],
      ),
    );
  }

  categoryList(Size size) {
    return SizedBox(
      height: size.height * 0.055,
      child: ListView.builder(
        padding: const EdgeInsets.symmetric(horizontal: fixPadding * 1.5),
        scrollDirection: Axis.horizontal,
        itemCount: category.length,
        shrinkWrap: true,
        physics: const BouncingScrollPhysics(),
        itemBuilder: (BuildContext context, int index) {
          return Container(
            alignment: Alignment.center,
            padding: const EdgeInsets.symmetric(
                horizontal: fixPadding * 1.5, vertical: fixPadding),
            margin: const EdgeInsets.symmetric(horizontal: fixPadding / 2),
            decoration: BoxDecoration(
              color: category[index]['color'] as Color,
              borderRadius: BorderRadius.circular(10),
              boxShadow: [
                BoxShadow(
                  color: grey94Color.withOpacity(0.3),
                  blurRadius: 5,
                )
              ],
            ),
            child: Row(
              children: [
                category[index]['isimage'] == false
                    ? Icon(
                        category[index]['icon'] as IconData,
                        size: 20,
                        color: whiteColor,
                      )
                    : Image.asset(
                        category[index]['image'].toString(),
                        height: 20,
                        width: 20,
                        color: whiteColor,
                      ),
                width5Space,
                Text(
                  category[index]['name'].toString(),
                  style: white16Stylew500,
                )
              ],
            ),
          );
        },
      ),
    );
  }

  categorytext() {
    return Padding(
      padding: const EdgeInsets.symmetric(
        vertical: fixPadding,
        horizontal: fixPadding * 2,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            "Category",
            style: black18Style,
          ),
          GestureDetector(
            onTap: () {
              Navigator.pushNamed(context, "/category");
            },
            child: Text("See all",
                style: primary14Style),
          )
        ],
      ),
    );
  }

  topContainer(Size size) {
    return Stack(
      children: [
        SizedBox(
          height: size.height * 0.22,
          width: double.infinity,
          child: Image.asset(
            "assets/home/Rectangle2.jpg",
            fit: BoxFit.cover,
          ),
        ),
        Positioned(
          bottom: 15,
          left: 0,
          right: 0,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: fixPadding * 2),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
              //  Text(
                //  getTranslate(context, ''),
               //   style: white16Style,
                //),
                const Text(
                  "Unlock the world of data analysis this summer!",
                  style: white18Style,
                ),
                height5Space,
                GestureDetector(
                  onTap: () {
                    Navigator.pushNamed(context, '/detail');
                  },
                  child: Container(
                    height: size.height * 0.05,
                    width: size.width * 0.3,
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        colors: gradient,
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                      ),
                      borderRadius: BorderRadius.only(
                        topLeft: Radius.circular(20),
                        bottomRight: Radius.circular(20),
                      ),
                    ),
                    alignment: Alignment.center,
                    child: Text(
                      "Know more",
                      style: white16Style,
                    ),
                  ),
                ),
              ],
            ),
          ),
        )
      ],
    );
  }
}
