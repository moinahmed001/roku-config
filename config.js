var config = {
	address: "",
	port: 8080,
	ipWhitelist: [],
	language: "en",
	timeFormat: 12,
	units: "metric",

	modules: [
		{
			module: "alert",
		},
		{
			module: "clock",
			position: "top_left"
		},
		{
			module: "calendar",
			position: "top_left",
			config: {
				colored: true,
				calendars: [
					{
						symbol: "dove",
						color: "#F4511E",
						url: "https://calendar.google.com/calendar/ical/4ji5lt582d7lpn13audkbj1h1g%40group.calendar.google.com/private-287a92a1c4d511ab1047e7fc4694c6b9/basic.ics"					},
					{
						symbol: "user-friends",
						color: "#A79B8E",
						url: "https://calendar.google.com/calendar/ical/thilml9k4ottltuhl84p974gc8%40group.calendar.google.com/private-9dbba035afcb37473517425bc4155a4e/basic.ics"					},
					{
						symbol: "briefcase",
						color: "#009688",
						url: "https://calendar.google.com/calendar/ical/7ockiifn21orrjgl1tch5s8mi0%40group.calendar.google.com/private-62a38b2cb80ca63a59f4b8c11b946cae/basic.ics"					}
				]
			}
		},
		 {
		 	module: "compliments",
		 	position: "lower_third",
			"config": {
    "compliments": {
        "anytime": [
            "Take on the day you beautiful land mermaid you!",
            "I hope your day is as nice as your face!",
            "We both look symmetrical!",
            "Back so soon? Don't you have something to do?",
            "Show me your moves!",
            "Ohhhh emmm geee... we look sooooo alike!",
            "Have you been working out?",
            "I'm lucky to be your mirror!",
            "How about that local sports team?",
            "Radically Reflective!",
            "At least you didn't lose your keys today, right?",
            "The Force is strong with you",
            "If I could high five you... I would, I promise.",
            "You knew better, but you still did that today... SHAME on you.",
            "With an attitude like that, you're not completely terrible",
            "HEEEEELLLPP!!!! I'm trapped!!!!!",
            "Seen any good movies lately?",
            "Being awesome is hard, but you'll manage.",
            "I could just hang here all day!",
            "There is always a party with you here.",
            "I need some time to reflect...",
            "I see a lot of my self in you.",
            "I'm a mirror and I'm LIT!",
        ],
        "morning": [
            "Good morning, handsome!",
            "Enjoy your day!",
            "How was your sleep?",
            "Have a good day!"
        ],
        "afternoon": [
            "Hello, beauty!",
            "Looking good today!",
            "Almost dinnertime!"
        ],
        "evening": [
            "You look nice!",
            "You rock!",
            "See you tomorrow!",
            "Sleep tight"
        ],
        "day_sunny" : [
            "It's gonna be a sunny day!"
        ],
        "rain" : [
            "Bring an umbrella today!!!"
        ],
        "night_clear" : [
            "Good night for stargazing!"
        ],
        "cloudy" : [
            "Cloudy today... hmmm..."
        ],
        "day_cloudy": [
            "It will be cloudy during the day"
        ],
        "cloudy_windy": [
            "It will be cloudy and windy!!!"
        ],
        "showers": [
            "You will get soaked today, lots of showers!"
        ],
        "thunderstorm": [
            "Just so you know, there will be thunderstorm!"
        ],
        "snow": [
            "Snoowwwww day.... take extra caution when its icy",
            "Make sure you wear boots with grip as its snowing outside"
        ],
        "fog": [
            "Vision will be reduced while driving, be careful!",
            "Very foggy today..."
        ],
        "night_cloudy": [
            "At night, it will be cloudy"
        ],
        "night_showers": [
            "At night, there will be shower rainfall!"
        ],
        "night_rain": [
            "At night, there will be rain!"
        ],
        "night_thunderstorm": [
            "At night, there will be thunder!"
        ],
        "night_snow": [
            "At night, there will be snow, may wanna wfh tomorrow?!"
        ],
        "night_alt_cloudy_windy": [
            "At night, it will be cloudy and windy!"
        ]
    }
}
		},
		{
			module: "currentweather",
			position: "top_right",
			config: {
				location: "London",
				locationID: "2643743",  //ID from http://bulk.openweathermap.org/sample/city.list.json.gz; unzip the gz file and find your city
				appid: "d1e5571b72a9cea6da44eb7b6260d0c5"
			}
		},
	{
		module: "MMM-MotionDetector",
		position: "top_left",	// Optional. This can be any of the regions. Displays debug informations.
		config: {
			timeout: 90000
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
	        remotePlayer: 'none',
	        showSnapWhenPaused: true,
	        remoteSnaps: true,
	        stream1: {
	            name: '',
	            url: 'rtsp://admin:admin@192.168.0.101:554/11',
	            frameRate: 'undefined',
	            snapshotType: 'url',
	            snapshotRefresh: 10,
	            width: undefined,
	            height: undefined,
	            },
	        }
		},
		{
		  module: 'MMM-MyCommute',
		  position: 'top_right',
		  config: {
		    apikey: 'AIzaSyCkw7SACrjD5T644KanKTwGG_vUWLiGWM4',
		    origin: 'Millman Street, London WC1N 3EW, UK',
		    startTime: '06:30',
		    endTime: '08:00',
		    hideDays: [0,6],
		    destinations: [
		      {
		        destination: 'Harlequin Avenue, Brentford, UK',
		        label: 'To Sky Plc',
						alternatives: true,
						showSummary: true,
		        color: '#82E5AA'
          }
		    ]
		  }
		},
		{
			module: 'MMM-GoogleFit',
    position: 'bottom_left',
    config: {
		stepGoal:5000,
		lastSevenDays: true
    }
},
		{
		module: 'MMM-GoogleFitX',
    position: 'bottom_right',
    config: {
		stepGoal: 5000,
		lastSevenDays: true
    }
},

		{
			module: 'MMM-ELMPrayerTime',
			position: 'top_left',	// This can be any of the regions. Best result is in the top_left/top_right.
			config: {
				apiVersion: '1.0', // please, leave unchanged. reserved for future use.
				timeFormat: 24,
				notDisplayed: ['midnight', 'sunset', 'imsak'],
				useUpdateInterval: true,
				updateInterval: 86400 * 1000, // How often do you want to fetch new praying time? (milliseconds)
				animationSpeed: 2.5 * 1000, // Speed of the update animation. (milliseconds)
				alertTimer: 15000
			}
		},

	]

};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
