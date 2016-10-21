
var SWITCH_PIN = 7;
var GREEN_PIN  = 11;
var RED_PIN    = 13;

var ADDRESS    = 0x72; // I2C address

var gpio = require('rpi-gpio');

var i2c = require('i2c-bus'),
  i2c1=i2c.openSync(1);

exports.init = init;
exports.setButtonColor = setButtonColor;
exports.drawImage = drawImage;

function init(buttonListener, cb) {

	i2c1.sendByteSync(ADDRESS,0x21); // 0010_xxxs s=1      (turn on system oscillator)
	i2c1.sendByteSync(ADDRESS,0xEF); // 1110_dddd d=15     (set brightness to full)
	i2c1.sendByteSync(ADDRESS,0x81); // 1000_xbbd b=0, d=1 (blinking off, display on)
	
	drawImage([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]); // clear the display
	
	gpio.setup(GREEN_PIN, gpio.DIR_OUT, function(err) {
		gpio.setup(RED_PIN, gpio.DIR_OUT, function(err) {				
			module.exports.setButtonColor(0);
			cb();
		});	
	});
	
	gpio.setup(SWITCH_PIN, gpio.DIR_IN, gpio.EDGE_BOTH);
	gpio.on('change', function(channel,value) {
		if (value) {
			buttonListener('down');
		} else {
			buttonListener('up');
		}	
	});
}

function setButtonColor(color) {
	color = color & 3;
	if(color==2 || color==3) {
		gpio.write(GREEN_PIN, false);
	} else {
		gpio.write(GREEN_PIN, true);
	}
	if(color==1 || color==3) {
		gpio.write(RED_PIN, false);
	} else {
		gpio.write(RED_PIN, true);
	}
}

function drawImage(image) {	
	
	i2c1.writeI2cBlockSync(ADDRESS,0,16,new Buffer(image));
	
}
