/* Magic Mirror Config Sample
*
* By Michael Teeuw http://michaelteeuw.nl
* MIT Licensed.
*
* For more information how you can configurate this file
* See https://github.com/MichMich/MagicMirror#configuration
*
*/

var config = {
  address: "0.0.0.0", // Address to listen on, can be:
  // - "localhost", "127.0.0.1", "::1" to listen on loopback interface
  // - another specific IPv4/6 to listen on a specific interface
  // - "", "0.0.0.0", "::" to listen on any interface
  // Default, when address config is left out, is "localhost"
  port: 8080,
  //	ipWhitelist: ["127.0.0.1", "::ffff:127.0.0.1", "::1"], // Set [] to allow all IP addresses
  // or add a specific IPv4 of 192.168.1.5 :
  // ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.1.5"],
  // or IPv4 range of 192.168.3.0 --> 192.168.3.15 use CIDR format :
  // ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.3.0/28"],

  ipWhitelist: [],
  electronOptions: {
    width: 1080,
    height: 1920
  },
  language: "en",
  timeFormat: 12,
  units: "metric",

  modules: [
    {
      module: "alert",
    },
    {
      module: "updatenotification",
      position: "top_bar"
    },
    {
      module: "currentweather",
      position: "top_right",
      config: {
        location: "London",
        locationID: "2643743",  //ID from http://bulk.openweathermap.org/sample/; unzip the gz file and find your city
        appid: "d1e5571b72a9cea6da44eb7b6260d0c5"
      }
    },
    {
      module: 'MMM-MyCommute',
      position: 'top_right',
      config: {
        apikey: '',
        origin: 'wc1n 3ew, London',
        startTime: '07:00',
        endTime: '08:30',
        hideDays: [0,6],
        pollFrequency: 5 * 60 * 1000,
        destinations: [
          {
            destination: 'Harlequin Avenue, Brentford',
            label: 'To Sky Plc',
            mode: 'driving',
            color: '#28C9E2',
            alternatives: true,
            showNextVehicleDeparture: true
          },
          {
             destination: 'NW10 3RY, London',
             label: 'To Medical Centre',
             mode: 'transit',
             transitMode: 'bus',
             color: '#CF1AD5',
             showNextVehicleDeparture: true,
             alternatives: true
           },
          // {
          //   destination: 'E14 0PT, London',
          //   label: 'To Culloden',
          //   mode: 'transit',
          //   color: '#5F1AD7',
          //   showNextVehicleDeparture: true,
          //   alternatives: true
          // },
          // {
          //   destination: 'E1 4PW, London',
          //   label: 'To Solebay',
          //   mode: 'transit',
          //   transitMode: 'bus|train',
          //   color: '#1A98D7',
          //   showNextVehicleDeparture: true,
          //   alternatives: true
          // },
        ]
      }
    },
    {
      module: 'MMM-RandomQuranAyah',
      position: 'bottom_bar',
      config: {
        apiVersion: '1.0',
        showArabic: false,
        updateInterval: 3600 * 1000 // milliseconds
      }
    },
    {
      module: 'MMM-PIR-Sensor',
      config: {
        sensorPin: 14,
        powerSavingNotification: true
      }
    },
    {
      module: "clock",
      position: "top_left"
    },
    {
      module: "calendar",
      header: "Calendars",
      position: "top_left",
      colored: true,
      color: "#721212",
      coloredSymbolOnly: false,
      maximumEntries: 15,
      config: {
        calendars: [
          {
            symbol: ["dove"],
            color: "#D11BBF",
            colored: true,
            coloredSymbolOnly: false,
            url: "https://calendar.google.com/calendar/ical/4ji5lt582d7lpn13audkbj1h1g%40group.calendar.google.com/private-287a92a1c4d511ab1047e7fc4694c6b9/basic.ics"
          },
          {
            symbol: ["users"],
            color: "#9C9C9C",
            url: "https://calendar.google.com/calendar/ical/thilml9k4ottltuhl84p974gc8%40group.calendar.google.com/private-9dbba035afcb37473517425bc4155a4e/basic.ics"
          },
          {
            symbol: ["briefcase"],
            color: "#721212",
            maximumEntries: 15,
            colored: true,
            coloredSymbolOnly: false,
            url: "https://calendar.google.com/calendar/ical/7ockiifn21orrjgl1tch5s8mi0%40group.calendar.google.com/private-62a38b2cb80ca63a59f4b8c11b946cae/basic.ics"
          }
      ]
    }
  },
  {
      module: 'MMM-ELMPrayerTime',
      position: 'top_left',	// This can be any of the regions. Best result is in the top_left/top_right.
      config: {
          apiVersion: '1.0', // please, leave unchanged. reserved for future use.
          lon: "-0.117675", // latitude of your position (city)
          lat: "51.523018", // longitude of your position (city)
          timezone: "Europe/London", // please refer to http://php.net/manual/en/timezones.php
          timeFormat: 24,
          method: 5,
          notDisplayed: ['midnight', 'sunset','imsak'],
          useUpdateInterval: true,
          updateInterval: 86400 * 1000, // How often do you want to fetch new praying time? (milliseconds)
          animationSpeed: 2.5 * 1000, // Speed of the update animation. (milliseconds)
          language: "en",
          showAdzanAlert: true,
          alertTimer: 15000
      }
  },
  {
    module: "MMM-RTSPStream",
    position: "bottom_center",
    config: {
      autoStart: true,
      rotateStreams: true,
      rotateStreamTimeout: 10,
      moduleWidth: 354,
      moduleHeight: 240,
      localPlayer: 'omxplayer',
      remotePlayer: 'ffmpeg',
      showSnapWhenPaused: true,
      remoteSnaps: true,
      stream1: {
        name: 'Camera 1',
        url: 'rtsp://192.168.0.101:554/11',
        frameRate: 'undefined',
        ffmpegPort: 9999,
        snapshotType: 'url',
        snapshotRefresh: 10,
        width: undefined,
        height: undefined,
      },
    }
  },
  {
    module: "MMM-NowPlayingOnSpotify",
    position: "top_left",

    config: {
      clientID: "41155a7ab6884faf96bae2e7ccd0dda5",
      clientSecret: "63b3b11566c14af380dd24fc9e2a5570",
      accessToken: "BQAQ-Y4klGzM5JfSfliMFptmzf9cNkxoe2pG2IYU9q9D3UbPaB7DjZWyrYhWjn-IRchO60Q96RruY-J-B6uSvn21s9i8R2W_6qUQV0dzwumsurZqkMyd5dlag6UXpOAaL_6J7hB1_p6P0tHtkBEDQX-S5x0F",
      refreshToken: "AQCGqS_Paf3OUiYKkPAoOSveSHGaF35mkLjfmOjkdGgO8rHtt5HAKs-O7tpJidMuroVl7RXAGHjDBuCucO_AZhpIX21Eb-4xmADYpTebAA6nHWJmqwQps2QSwuyhzyAnTji18w"
    }
  },
  {
    module: "compliments",
    position: "lower_third",
    config: {
      compliments: {
        anytime: [
          "What you planning to do today?",
          "It's you.",
          "After everything, it's still you.",
          "You got something there...",
          "Behind you, a three-headed monkey!",
          "Damn. You're looking good!",
          "Looking good!",
          "Slow down!",
          "Yes, my Queen/King, you are the fairest of them all.",
          "OBJECTS IN MIRROR ARE LESS ATTRACTIVE THAN THEY APPEAR.",
          "Quick, DO NOT think about pink elephants!",
          "I hope your day is as nice as your face!",
          "You look symmetrical!",
          "Back so soon? Don't you have something to do?",
          "Show me your moves!",
          "Ohhhh emmm geee... we look sooooo alike!",
          "Have you been working out?",
          "I'm lucky to be your mirror!",
          "Radically Reflective!",
          "At least you didn't lose your keys today, right?",
          "The Force is strong with you",
          "If I could high five you... I would, I promise.",
          "You knew better, but you still did that today... SHAME on you.",
          "With an attitude like that, you're not completely terrible",
          "On a scale from 1 to 10, you're an 11!",
          "HEEEEELLLPP!!!! I'm trapped!!!!!",
          "Seen any good movies lately?",
          "You make my data circuits skip a clock cycle!",
          "Being awesome is hard, but you'll manage.",
          "I could just hang here all day!",
          "I'm not touch screen.",
          "There is always a party with you here.",
          "I need some time to reflect...",
          "I see a lot of my self in you.",
          "I'm a mirror and I'm LIT!"
        ],
        morning: [
          "Good morning!",
          "Enjoy your day!",
          "How was your sleep?",
          "Go get 'em, Tiger!"
        ],
        afternoon: [
          "Hello, beauty!",
          "You look like you had a big meal!",
          "Looking good today!",
          "Hitting your stride!",
          "You are making a difference!",
          "You're more fun than bubble wrap!"
        ],
        evening: [
          "Wow, you look great!",
          "You look nice!",
          "You made someone smile today, I know it.",
          "You are making a difference.",
          "The day was better for your efforts.",
          "A day without sunshine is like, you know, night.",
          "See you tomorrow!",
          "Sleep tight."
        ],
        day_sunny: [
          "Today is a sunny day",
          "It's a beautiful day"
        ],
        snow: [
          "Snowball battle!",
          "Good luck getting to work!",
          "Don't bother going to work its awful outside!"
        ],
        rain: [
          "Don't forget your umbrella",
          "No, seriously grab an umbrella. It will rain today!"
        ],
      	day_cloudy:[
          "It will be cloudy during the DAY time"
      	],
        cloudy:[
          "It will be cloudy whole day"
        ],
        cloudy_windy:[
          "It will be cloudy and windy whole day, careful!!"
        ],
        showers:[
          "Literally gonna be pouring outside, dont leave without an umbrella!"
        ],
        thunderstorm:[
          "Thunderstorm will there today!"
        ],
        fog:[
          "The visibility will be reduced as it will be foggy today!",
          "fog, oh no :("
        ],
        night_clear:[
          "It seems like the night weather will be nice and clear."
        ],
        night_cloudy : ["During the night time it will be Cloudy"],
        night_showers : ["During the night time it will be showering rain outside"],
        night_rain : ["During the night time it will be rainy"],
        night_thunderstorm : ["During the night time there will be thunderstorm"],
        night_snow : ["During the night time it will be snowing"],
        night_alt_cloudy_wind: ["During the night time it will be cloudy with winds"]
      }
    }
  },
  {
    module: "MMM-WeeklySchedule",
    position: "top_right",
    header: "Sabia's todo list",
    config: {
        schedule: {
          timeslots: [ "11:00", "15:00", "16:00", "20:00", "21:00", "22:00" ],
          lessons: {
            mon: [ "", "", "", "Gym", "Shower & Food", "Movies / Series" ],
            tue: [ "", "", "", "Gym", "Shower & Food", "Movies / Series" ],
            wed: [ "", "", "", "Gym", "Shower & Food", "Movies / Series" ],
            thu: [ "", "", "", "Gym", "Shower & Food", "Movies / Series" ],
            fri: [ "", "", "", "Going Out", "", "Cooking" ],
            sat: [ "Housekeeping - cleaning, laundry and shopping", "Family day out", "", "", "", "" ],
            sun: [ "Cooking, shower and work ready", "Visit Family", "", "", "", "" ]
          }
        },
        updateInterval: 1 * 60 * 60 * 1000, // every hour
        showNextDayAfter: "16:00"
      }
    },
    {
      module: 'MMM-doomsDay',
      position: 'top_right', // This can be any of the regions, best results in center regions
      config: {
          doomsDay: "2019-04-16 19:00:00", // YYYY-MM-DD HH:MM:SS, Do not alter the time, just the date
          toWhat: "Holiday Countdown...",
      present: "I bet you are  looking forward to the 17 hours flight",
      timesUp: "Had a good holiday?"
	    }
    }

]

};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
