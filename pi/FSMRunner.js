var machine;

var currentState = null;
var timeoutID = null;
var timeoutEvent = null;

exports.init = init;
exports.gotoState = gotoState;
exports.handleEvent = handleEvent;

function init(m) {
	machine = m;
	gotoState('START');
}

function gotoState(stateName) {
	if(timeoutID) {		
		clearTimeout(timeoutID);
		timeoutID = null;
	}
	currentState = machine[stateName];
	var ef = currentState['ENTER'];
	if(ef) {
		var fn = machine[ef[0]];
		fn.apply(machine,ef.slice(1,ef.length));
	}	
	timeoutEvent = currentState['TIMEOUT'];
	if(timeoutEvent) {
		timeoutID = setTimeout(function() {
			timeoutID = null;
			gotoState(timeoutEvent[1]);
		},timeoutEvent[0]);
	}	
}

function handleEvent(eventName) {
	var ef = currentState[eventName];
	if(ef) {
		gotoState(ef);		
	}	
}




