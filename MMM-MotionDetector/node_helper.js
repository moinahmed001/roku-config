const NodeHelper = require("node_helper");
const exec = require("child_process").exec;

module.exports = NodeHelper.create({
	start: function () {
		this.started = false;
		this.isMonitorOn(function(result) {
			console.log("MMM-MotionDetector: monitor on " + result);
		});
	},

	activateMonitor: function () {
		this.isMonitorOn(function(result) {
			if (!result) {
				exec("vcgencmd display_power 1", function(err, out, code) {
					if (err) {
						console.error("MMM-MotionDetector: error activating monitor: " + code);
					} else {
						console.log("MMM-MotionDetector: monitor has been activated");
					}
				});
				exec("pm2 start omx_stream1", function(err, out, code) {
					if (err) {
						console.error("MMM-MotionDetector: error activating camera");
					} else {
						console.log("MMM-MotionDetector: camera has been activated");
					}
				});
			}
		});
		this.started = false;
	},

	deactivateMonitor: function () {
		this.isMonitorOn(function(result) {
			if (result) {
				exec("vcgencmd display_power 0", function(err, out, code) {
					if (err) {
						console.error("MMM-MotionDetector: error deactivating monitor: " + code);
					} else {
						console.log("MMM-MotionDetector: monitor has been deactivated");
					}
				});
				exec("pm2 stop omx_stream1", function(err, out, code) {
					if (err) {
						console.error("MMM-MotionDetector: error DE-activating camera");
					} else {
						console.log("MMM-MotionDetector: camera has been deactivated");
					}
				});
			}
		});
		this.started = false;
	},

	isMonitorOn: function(resultCallback) {
		exec("vcgencmd display_power", function(err, out, code) {
			if (err) {
				console.error("MMM-MotionDetector: error calling monitor status: " + code);
				return;
			}

			console.log("MMM-MotionDetector: monitor " + out);
			resultCallback(out.includes("=1"));
		});
	},

	// Subclass socketNotificationReceived received.
	socketNotificationReceived: function (notification, payload) {
		if (notification === "MOTION_DETECTED" && this.started === false) {
			console.log("MMM-MotionDetector: MOTION_DETECTED, score " + payload.score);
			this.started = true;
			this.activateMonitor();
		}
		if (notification === "DEACTIVATE_MONITOR" && this.started === false) {
			console.log("MMM-MotionDetector: DEACTIVATE_MONITOR, percentage off: " + payload.percentageOff);
			this.started = true;
			this.deactivateMonitor();
		}
	}
});
