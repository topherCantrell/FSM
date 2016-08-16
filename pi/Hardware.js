
var SWITCH_PIN = 7;
var GREEN_PIN = 11;
var RED_PIN = 13;

var gpio = require('rpi-gpio');

var i2c = require('i2c-bus'),
  i2c1=i2c.openSync(1);

exports.init = init;
exports.setButtonColor = setButtonColor;
exports.drawImage = drawImage;

function init(buttonListener, cb) {

	i2c1.writeByteSync(0x72,0x21,0);
	i2c1.writeByteSync(0x72,0xEF,0);
	i2c1.writeByteSync(0x72,0x81,0);
	drawImage([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]);
	
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
	for (var x=0;x<16;++x) {
		i2c1.writeByteSync(0x72,x,image[x]);
	}
}
