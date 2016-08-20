var machine;

var currentState = null;
var timeoutID = null;
var timeoutEvent = null;

exports.init = init;
exports.handleEvent = handleEvent;

function init(m, start) {
	machine = m;
	gotoState(start);
}

function gotoState(stateName) {
	setImmediate( function() {
	console.log('Changing to state :'+stateName+':');
	if(timeoutID) {		
		clearTimeout(timeoutID);
		timeoutID = null;
	}
	currentState = machine[stateName];
	var ef = currentState['ENTER'];
	if(ef) {
		if(! Array.isArray(ef)) {
			ef = [ef];
		}
		runFunctions(ef,0);
	}	
	timeoutEvent = currentState['TIMEOUT'];
	if(timeoutEvent) {
		if(timeoutEvent[0]==0) {
			setImmediate( function() {
				console.log('NO TIME');
				timeoutID = null;
				runFunctions(timeoutEvent,2);
				gotoState(timeoutEvent[1]);
			});
		} else {
			timeoutID = setTimeout(function() {
				console.log('TIMEOUT');
				timeoutID = null;
				runFunctions(timeoutEvent,2);
				gotoState(timeoutEvent[1]);
			},timeoutEvent[0]);
		}
	}	
	});
}

function runFunctions(list,index) {
	while(index<list.length) {
		var end = list.indexOf('and',index);
		if(end<0) end=list.length;
		var fn = machine[list[index]];
		fn.apply(machine,list.slice(index+1,end));
		index = end;
		if(index<list.length) {
			++index;
		}
	}
}

function handleEvent(eventName) {	
	setImmediate( function() {
		console.log("Event: "+eventName);
		var ef = currentState[eventName];
		if(ef) {
			if(! Array.isArray(ef)) {
				ef = [ef];
			}
			runFunctions(ef,1); // These may call handleEvent()
			gotoState(ef[0]);		
		} else {
			console.log("Ignoring '"+eventName+"'");
		}	
	});
}
