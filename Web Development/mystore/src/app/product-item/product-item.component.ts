import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-product-item',
  templateUrl: './product-item.component.html',
  styleUrls: ['./product-item.component.css']
})
export class ProductItemComponent implements OnInit {
  public static productItems = [
    {
      id: 1,
      category: "Data Storage",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/81tjLksKixL._AC_SL1500_.jpg",
      name: "Seagate Portable 2TB External Hard Drive Portable HDD",
      link:
        "https://www.amazon.com/Seagate-Portable-External-Hard-Drive/dp/B07CRG94G3/ref=sr_1_1?dchild=1&qid=1614068054&s=computers-intl-ship&sr=1-1",
      description:
        "Easily store and access 2TB of content on the go with the Seagate Portable Drive, a great laptop hard drive.",
      rating: 4.7,
      likes: 105361
    },
    {
      id: 2,
      category: "Computer Components",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/71WPGXQLcLL._AC_SL1384_.jpg",
      name: "AMD Ryzen 5 3600",
      link:
        "https://www.amazon.com/AMD-Ryzen-3600-12-Thread-Processor/dp/B07STGGQ18/ref=sr_1_2?dchild=1&qid=1614068054&s=computers-intl-ship&sr=1-2",
      description:
        "AMD CPU 100 100000031box Ryzen 5 3600 6C 12T 4200MHz 36MB 65W AM4 Wraith Stealth.",
      rating: 4.9,
      likes: 27308
    },
    {
      id: 3,
      category: "Computer Components",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/51kHiPeTSmL._AC_SL1000_.jpg",
      name: "Corsair Vengeance LPX 16GB (2x8GB) DDR4",
      link:
        "https://www.amazon.com/Corsair-Vengeance-3200MHz-Desktop-Memory/dp/B0143UM4TC/ref=sr_1_3?dchild=1&qid=1614068054&s=computers-intl-ship&sr=1-3",
      description:
        "Vengeance LPX memory is designed for high performance Overclocking.",
      rating: 4.8,
      likes: 74629
    },
    {
      id: 4,
      category: "Data Storage",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/81vkjxbO-rL._AC_SL1500_.jpg",
      name: "Samsung (MZ-V7S1T0B/AM) 970 EVO Plus SSD",
      link:
        "https://www.amazon.com/Samsung-970-EVO-Plus-MZ-V7S1T0B/dp/B07MFZY2F2/ref=sr_1_5?dchild=1&qid=1614068054&s=computers-intl-ship&sr=1-5",
      description:
        "For intensive workloads on PCs and workstations, the Samsung SSD 970 EVO Plus delivers ultimate performance powered by Samsung's NVMe SSD leadership.",
      rating: 4.9,
      likes: 20598
    },
    {
      id: 5,
      category: "Computer Components",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/51VQv0yZEvL._AC_SL1200_.jpg",
      name: "Elgato Cam Link",
      link:
        "https://www.amazon.com/Elgato-Cam-Link-Broadcast-Camcorder/dp/B07K3FN5MR/ref=sr_1_6?dchild=1&qid=1614068054&s=computers-intl-ship&sr=1-6",
      description:
        "With Cam Link 4K, use your DSLR, camcorder or action cam as a professional webcam on your PC or Mac.",
      rating: 4.6,
      likes: 5254
    },
    {
      id: 6,
      category: "Computer Components",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/61Gm1upecsL._AC_SL1500_.jpg",
      name: "ARCTIC MX-4",
      link:
        "https://www.amazon.com/ARCTIC-MX-4-Compound-Micro-particles-Durability/dp/B0795DP124/ref=sr_1_9?dchild=1&qid=1614068054&s=computers-intl-ship&sr=1-9",
      description:
        "Thermal Compound for All CoolersEasy to ApplyWith an ideal consistency, the MX-4 is very easy to use, even for beginners.",
      rating: 4.8,
      likes: 24972
    },
    {
      id: 7,
      category: "Data Storage",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/71RTRS3oAjL._AC_SL1500_.jpg",
      name: "Western Digital 1TB WD Blue SN550 NVMe Internal SSD",
      link:
        "https://www.amazon.com/Blue-SN550-1TB-NVMe-Internal/dp/B07YFFX5MD/ref=sr_1_10?dchild=1&qid=1614068054&s=computers-intl-ship&sr=1-10",
      description:
        "Put NVMe power at the heart of your PC for lightning-fast, ultra-responsive performance.",
      rating: 4.8,
      likes: 13554
    },
    {
      id: 8,
      category: "Data Storage",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/811juXBuTDL._AC_SL1500_.jpg",
      name: "Western Digital 1TB WD Blue 3D NAND Internal PC SSD",
      link:
        "https://www.amazon.com/Blue-NAND-1TB-SSD-WDS100T2B0A/dp/B073SBQMCX/ref=sr_1_12?dchild=1&qid=1614068054&s=computers-intl-ship&sr=1-12",
      description:
        "The WD Blue 3D NAND SATA SSD utilizes 3D NAND technology for capacities up to 4TB with enhanced reliability.",
      rating: 4.8,
      likes: 36412
    },
    {
      id: 9,
      category: "Data Storage",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/61MGrHUMWzL._AC_SL1500_.jpg",
      name:
        "Seagate Storage Expansion Card for Xbox Series X|S 1TB Solid State Drive",
      link:
        "https://www.amazon.com/Seagate-Storage-Expansion-Solid-State/dp/B08K3S6WJM/ref=sr_1_14?dchild=1&qid=1614068054&s=computers-intl-ship&sr=1-14",
      description:
        "Instantly expand the peak speed capacity of the most-powerful gaming experience Xbox has ever created with the Seagate Storage Expansion Card for Xbox Series X|S.",
      rating: 4.8,
      likes: 33625
    },
    {
      id: 10,
      category: "Computer Components",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/71dj%2B5GQwEL._AC_SL1500_.jpg",
      name: "Corsair RM850x Fully Modular Power Supply",
      link:
        "https://www.amazon.com/CORSAIR-RM850x-Certified-Modular-Supply/dp/B079H5WNXN/ref=sr_1_17?brr=1&dchild=1&qid=1614700590&rd=1&s=pc&sr=1-17",
      description:
        "Quiet, efficient and dependable, an RM850x PSU has everything you need to power your high performance PC for years to come.",
      rating: 4.8,
      likes: 6839
    },
    {
      id: 11,
      category: "Networking & Wireless",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/71ASsDrrKeL._AC_SL1500_.jpg",
      name: "TP-Link TL-SG105",
      link:
        "https://www.amazon.com/Ethernet-Splitter-Optimization-Unmanaged-TL-SG105/dp/B00A128S24/ref=sr_1_6?dchild=1&qid=1614701075&s=pc&sr=1-6",
      description:
        "Increase the reliability of your connected devices with the TL-SG105 5-port Gigabit desktop switch.",
      rating: 4.8,
      likes: 48799
    },
    {
      id: 12,
      category: "Networking & Wireless",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/61z5oOk5fzL._AC_SL1350_.jpg",
      name: "NETGEAR Wi-Fi Range Extender EX3700",
      link:
        "https://www.amazon.com/NETGEAR-Wi-Fi-Range-Extender-EX3700/dp/B00R92CL5E/ref=sr_1_7?dchild=1&qid=1614701075&s=pc&sr=1-7",
      description:
        "Plug into a wall outlet for a sleek solution that extends your router's range and stays out of sight.",
      rating: 3.9,
      likes: 48839
    },
    {
      id: 13,
      category: "Networking & Wireless",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/61FA9BbugzL._AC_SL1500_.jpg",
      name: "NETGEAR Nighthawk Smart Wi-Fi Router, R6700 - AC1750",
      link:
        "https://www.amazon.com/NETGEAR-R6700-Nighthawk-Gigabit-Ethernet/dp/B00R2AZLD2/ref=sr_1_10?dchild=1&qid=1614701075&s=pc&sr=1-10",
      description:
        "The NETGEAR Nighthawk AC1750 Smart Wi-Fi Router delivers extreme Wi-Fi speed for gaming up to 1750Mbps.",
      rating: 4.3,
      likes: 70482
    },
    {
      id: 14,
      category: "Networking & Wireless",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/41Qo0EGG4TL._AC_SL1000_.jpg",
      name: "TP-Link AC600 USB WiFi Adapter for PC (Archer T2U Plus)",
      link:
        "https://www.amazon.com/Wireless-desktop-10-9-10-14-Archer-T2U/dp/B07P5PRK7J/ref=sr_1_20?dchild=1&qid=1614701075&s=pc&sr=1-20",
      description:
        "200 Mbps speeds on the 2.4 GHz band is perfect for normal use, such as web surfing with legacy devices.",
      rating: 4.5,
      likes: 14595
    },
    {
      id: 15,
      category: "Networking & Wireless",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/71igbmDJwDL._AC_SL1500_.jpg",
      name: "Sabrent 4-Port USB 2.0 Hub",
      link:
        "https://www.amazon.com/Sabrent-4-Port-Individual-Switches-HB-UMLS/dp/B00BWF5U0M/ref=sr_1_16?dchild=1&qid=1614701075&s=pc&sr=1-16",
      description:
        "Easily add up to 4 devices with the Sabrent USB 2.0 Hub. Particularly great for recent notebooks that provide a limited number of USB ports.",
      rating: 4.6,
      likes: 58738
    },
    {
      id: 16,
      category: "Monitors",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/91fAU6mxFsL._AC_SL1500_.jpg",
      name: "HP 24mh FHD Monitor",
      link:
        "https://www.amazon.com/HP-24mh-FHD-Monitor-Built/dp/B08BF4CZSV/ref=sr_1_1?dchild=1&qid=1614702014&s=pc&sr=1-1",
      description:
        "The HP 24mh FHD Monitor has all the style and performance you need in a monitor without breaking the bank.",
      rating: 4.8,
      likes: 9910
    },
    {
      id: 17,
      category: "Monitors",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/81QpkIctqPL._AC_SL1500_.jpg",
      name: "Acer SB220Q bi 21.5 inches Widescreen LCD IPS",
      link:
        "https://www.amazon.com/Acer-SB220Q-Ultra-Thin-Frame-Monitor/dp/B07CVL2D2S/ref=sr_1_2?dchild=1&qid=1614702014&s=pc&sr=1-2",
      description:
        "The Acer SB220Q bi 21.5 inches Widescreen LCD IPS display combines stylish ultra-thin functionality with amazing 1920 x 1080 resolution, allowing you to enjoy High-Definition entertainment in the comfort of your home.",
      rating: 4.7,
      likes: 26811
    },
    {
      id: 18,
      category: "Monitors",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/914W%2BOtJQ-L._AC_SL1500_.jpg",
      name: "Sceptre Curved 27 inches 75Hz LED Monitor",
      link:
        "https://www.amazon.com/Sceptre-Monitor-Speakers-Edge-Less-C275W-1920RN/dp/B07MTRQ6B3/ref=sr_1_5?dchild=1&qid=1614702014&s=pc&sr=1-5",
      description:
        "With the C275W-1920RN, a slender 1800R screen curvature yields wide-ranging images that seemingly surround you.",
      rating: 4.7,
      likes: 5960
    },
    {
      id: 19,
      category: "Monitors",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/91jzIGu5N-L._AC_SL1500_.jpg",
      name: "LG 24M47VQ 24-Inch LED-lit Monitor",
      link:
        "https://www.amazon.com/LG-24M47VQ-24-Inch-LED-lit-Monitor/dp/B00W95RR32/ref=sr_1_6?dchild=1&qid=1614702014&s=pc&sr=1-6",
      description:
        "Fast response time of 2ms allows the smooth viewing of action scenes, sports and video games with greater clarity and vivid quality.",
      rating: 4.7,
      likes: 3166
    },
    {
      id: 20,
      category: "Monitors",
      image:
        "https://images-na.ssl-images-amazon.com/images/I/81nSaeP3AvL._AC_SL1500_.jpg",
      name: "Dell 27 LED backlit LCD Monitor",
      link:
        "https://www.amazon.com/Dell-backlit-Monitor-SE2719H-1080p/dp/B07KW6HFD1/ref=sr_1_8?dchild=1&qid=1614702014&s=pc&sr=1-8",
      description:
        "View images, video and files clearly on this 27 inches Full HD monitor with thin bezels and a compact footprint that frees up valuable desk space.",
      rating: 4.7,
      likes: 5489
    }
  ];

  constructor() { }

  ngOnInit(): void {
  }
}
