
var IM_BOARD = [0x24,0x24,0x24,0x24,0xFF,0xFF,0x24,0x24,0x24,0x24,0xFF,0xFF,0x24,0x24,0x24,0x24];

var IM_WIPERS = {		
	board : [
	[0xFF,0xFF,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81,0xFF,0xFF],
	[0x42,0x42,0xFF,0xFF,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0xFF,0xFF,0x42,0x42],
	[0x18,0x18,0x18,0x18,0x18,0x18,0xFF,0xFF,0xFF,0xFF,0x18,0x18,0x18,0x18,0x18,0x18]],
	
	vert : [
	[0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01],
	[0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02],
	[0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04],
	[0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08],
	[0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10],
	[0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20],
	[0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x40],
	[0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80]],
	
	horiz : [
	[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF],
	[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0x00,0x00],
	[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0x00,0x00,0x00,0x00],
	[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00],
	[0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
	[0x00,0x00,0x00,0x00,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
	[0x00,0x00,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
	[0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]],
	
	diag : [
	[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01],
	[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x02,0x02],
	[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x02,0x02,0x04,0x04],
	[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x02,0x02,0x04,0x04,0x08,0x08],
	[0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x02,0x02,0x04,0x04,0x08,0x08,0x10,0x10],
	[0x00,0x00,0x00,0x00,0x01,0x01,0x02,0x02,0x04,0x04,0x08,0x08,0x10,0x10,0x20,0x20],
	[0x00,0x00,0x01,0x01,0x02,0x02,0x04,0x04,0x08,0x08,0x10,0x10,0x20,0x20,0x40,0x40],
	[0x01,0x01,0x02,0x02,0x04,0x04,0x08,0x08,0x10,0x10,0x20,0x20,0x40,0x40,0x80,0x80],
	[0x02,0x02,0x04,0x04,0x08,0x08,0x10,0x10,0x20,0x20,0x40,0x40,0x80,0x80,0x00,0x00],
	[0x04,0x04,0x08,0x08,0x10,0x10,0x20,0x20,0x40,0x40,0x80,0x80,0x00,0x00,0x00,0x00],
	[0x08,0x08,0x10,0x10,0x20,0x20,0x40,0x40,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00],
	[0x10,0x10,0x20,0x20,0x40,0x40,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
	[0x20,0x20,0x40,0x40,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
	[0x40,0x40,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
	[0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]]
};

var IM_COMPUTER_PLAYERS = {
    mrRandom : [0x00,0x00,0x06,0x00,0x09,0x00,0xD1,0x00,0xD1,0x00,0x01,0x00,0x06,0x00,0x00,0x00],
    oneder :   [0x00,0x00,0x80,0x80,0xC0,0xC0,0xFF,0xFF,0xFF,0xFF,0xC6,0xC6,0x86,0x86,0x00,0x00],
    catWoman : [0x0E,0x0E,0x05,0x05,0x2E,0x0E,0x20,0x00,0xE0,0x00,0x20,0x09,0x20,0x09,0x00,0x06],
};

var IM_SPLASH_SCREENS = {
	tic : [[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x0F,0x00,0x01,0x00],
	       [0x00,0x00,0x00,0x09,0x00,0x0F,0x00,0x09,0x00,0x00,0x01,0x00,0x0F,0x00,0x01,0x00],
	       [0x00,0x00,0x00,0x09,0xA0,0xAF,0xA0,0xA9,0xE0,0xE0,0x01,0x00,0x0F,0x00,0x01,0x00]],

	tac : [[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x0F,0x0F,0x01,0x01],
	       [0x0E,0x00,0x05,0x00,0x05,0x00,0x0E,0x00,0x00,0x00,0x01,0x01,0x0F,0x0F,0x01,0x01],
	       [0x0E,0x00,0x05,0x00,0x05,0xA0,0x0E,0xA0,0x00,0xE0,0x01,0x01,0x0F,0x0F,0x01,0x01]],

	toe : [[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x07,0x00,0x01,0x00,0x00],
	       [0x07,0x07,0x05,0x05,0x07,0x07,0x00,0x00,0x00,0x01,0x00,0x07,0x00,0x01,0x00,0x00],
           [0x07,0x07,0x8D,0x05,0xAF,0x07,0xA8,0x00,0xF8,0x01,0x00,0x07,0x00,0x01,0x00,0x00]]
};

var IM_GAME_CELLS = [
	[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x03,0x03,0x03],
	[0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x03,0x03,0x03,0x00,0x00,0x00,0x00,0x00,0x00],
	[0x03,0x03,0x03,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
	[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x18,0x18],
	[0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x18,0x18,0x00,0x00,0x00,0x00,0x00,0x00],
	[0x18,0x18,0x18,0x18,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
	[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0xC0,0xC0,0xC0],
	[0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0xC0,0xC0,0xC0,0x00,0x00,0x00,0x00,0x00,0x00],
	[0xC0,0xC0,0xC0,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
];

var IM_SOLID_COLORS = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF],
    [0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00,0xFF,0x00], 
    [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
];

var TIMING = {
		splashLetters :  250,
		splashWord    : 1000,
		wipe          :   75,
		wipeHold      :  250,		
		pickCPUOn     : 1000,
		pickCPUOff    : 1000,
		pickCPUHold   : 2000,
		winOn         :  500,
		winOff        :  500,
		inputDown     :  500,
		inputHeld     : 1000,
		cpuOn         :  500,
		cpuOff        :  500
}

var MACHINE = {	
		
	// ------------------------------------------------
		
	SPLASH   : {
		ENTER : ['setButtonColor',2, 'and', 'drawImage', IM_SPLASH_SCREENS.tic[0]],
		TIMEOUT : [TIMING.splashLetters, 'Tic_TI'],
        down : 'PICKS'
	},
	Tic_TI  : {
		ENTER : ['drawImage', IM_SPLASH_SCREENS.tic[1]],
		TIMEOUT : [TIMING.splashLetters, 'Tic_TIC'],
        down : 'PICKS'
	},
	Tic_TIC : {
		ENTER : ['drawImage', IM_SPLASH_SCREENS.tic[2]],
		TIMEOUT : [TIMING.splashWord, 'WipeH_1'],
        down : 'PICKS'
	},	
	
	WipeH_1 : {
		ENTER : ['orImageBuffer', IM_WIPERS.horiz[0],3],
		TIMEOUT : [TIMING.wipe, 'WipeH_2'],
        down : 'PICKS'
	},
	WipeH_2 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.horiz[0], 'and', 'orImageBuffer', IM_WIPERS.horiz[1],3],
		TIMEOUT : [TIMING.wipe, 'WipeH_3'],
        down : 'PICKS'
	},
	WipeH_3 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.horiz[1], 'and', 'orImageBuffer', IM_WIPERS.horiz[2],3],
		TIMEOUT : [TIMING.wipe, 'WipeH_4'],
        down : 'PICKS'
	},
	WipeH_4 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.horiz[2], 'and', 'orImageBuffer', IM_WIPERS.horiz[3],3],
		TIMEOUT : [TIMING.wipe, 'WipeH_5'],
        down : 'PICKS'
	},
	WipeH_5 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.horiz[3], 'and', 'orImageBuffer', IM_WIPERS.horiz[4],3],
		TIMEOUT : [TIMING.wipe, 'WipeH_6'],
        down : 'PICKS'
	},
	WipeH_6 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.horiz[4], 'and', 'orImageBuffer', IM_WIPERS.horiz[5],3],
		TIMEOUT : [TIMING.wipe, 'WipeH_7'],
        down : 'PICKS'
	},
	WipeH_7 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.horiz[5], 'and', 'orImageBuffer', IM_WIPERS.horiz[6],3],
		TIMEOUT : [TIMING.wipe, 'WipeH_8'],
        down : 'PICKS'
	},
	WipeH_8 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.horiz[6], 'and', 'orImageBuffer', IM_WIPERS.horiz[7],3],
		TIMEOUT : [TIMING.wipe, 'WipeH_HOLD'],
        down : 'PICKS'
	},
	WipeH_HOLD : {
		ENTER : ['drawImage',IM_SOLID_COLORS[0]],
		TIMEOUT : [TIMING.wipeHold, 'Tac_T'],
        down : 'PICKS'
	},
	
	Tac_T   : {
		ENTER : ['drawImage', IM_SPLASH_SCREENS.tac[0]],
		TIMEOUT : [TIMING.splashLetters, 'Tac_TA'],
        down : 'PICKS'
	},
	Tac_TA  : {
		ENTER : ['drawImage', IM_SPLASH_SCREENS.tac[1]],
		TIMEOUT : [TIMING.splashLetters, 'Tac_TAC'],
        down : 'PICKS'
	},
	Tac_TAC : {
		ENTER : ['drawImage', IM_SPLASH_SCREENS.tac[2]],
		TIMEOUT : [TIMING.splashWord, 'WipeV_1'],
        down : 'PICKS'
	},
	
	WipeV_1 : {
		ENTER : ['orImageBuffer', IM_WIPERS.vert[0],3],
		TIMEOUT : [TIMING.wipe, 'WipeV_2'],
        down : 'PICKS'
	},
	WipeV_2 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.vert[0], 'and', 'orImageBuffer', IM_WIPERS.vert[1],3],
		TIMEOUT : [TIMING.wipe, 'WipeV_3'],
        down : 'PICKS'
	},
	WipeV_3 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.vert[1], 'and', 'orImageBuffer', IM_WIPERS.vert[2],3],
		TIMEOUT : [TIMING.wipe, 'WipeV_4'],
        down : 'PICKS'
	},
	WipeV_4 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.vert[2], 'and', 'orImageBuffer', IM_WIPERS.vert[3],3],
		TIMEOUT : [TIMING.wipe, 'WipeV_5'],
        down : 'PICKS'
	},
	WipeV_5 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.vert[3], 'and', 'orImageBuffer', IM_WIPERS.vert[4],3],
		TIMEOUT : [TIMING.wipe, 'WipeV_6'],
        down : 'PICKS'
	},
	WipeV_6 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.vert[4], 'and', 'orImageBuffer', IM_WIPERS.vert[5],3],
		TIMEOUT : [TIMING.wipe, 'WipeV_7'],
        down : 'PICKS'
	},
	WipeV_7 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.vert[5], 'and', 'orImageBuffer', IM_WIPERS.vert[6],3],
		TIMEOUT : [TIMING.wipe, 'WipeV_8'],
        down : 'PICKS'
	},
	WipeV_8 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.vert[6], 'and', 'orImageBuffer', IM_WIPERS.vert[7],3],
		TIMEOUT : [TIMING.wipe, 'WipeV_HOLD'],
        down : 'PICKS'
	},
	WipeV_HOLD : {
		ENTER : ['drawImage',IM_SOLID_COLORS[0]],
		TIMEOUT : [TIMING.wipeHold, 'Toe_T'],
        down : 'PICKS'
	},
	
	Toe_T   : {
		ENTER : ['drawImage', IM_SPLASH_SCREENS.toe[0]],
		TIMEOUT : [TIMING.splashLetters, 'Toe_TO'],
        down : 'PICKS'
	},
	Toe_TO  : {
		ENTER : ['drawImage', IM_SPLASH_SCREENS.toe[1]],
		TIMEOUT : [TIMING.splashLetters, 'Toe_TOE'],
        down : 'PICKS'
	},
	Toe_TOE : {
		ENTER : ['drawImage', IM_SPLASH_SCREENS.toe[2]],
		TIMEOUT : [TIMING.splashWord, 'WipeB_1'],
        down : 'PICKS'
	},
	
	WipeB_1 : {
		ENTER : ['orImageBuffer', IM_WIPERS.board[0],3],
		TIMEOUT : [TIMING.wipe, 'WipeB_2'],
        down : 'PICKS'
	},
	WipeB_2 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.board[0], 'and', 'orImageBuffer', IM_WIPERS.board[1],3],
		TIMEOUT : [TIMING.wipe, 'WipeB_3'],
        down : 'PICKS'
	},
	WipeB_3 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.board[1], 'and', 'orImageBuffer', IM_BOARD,3],
		TIMEOUT : [TIMING.wipe, 'WipeB_4'],
        down : 'PICKS'
	},
	WipeB_4 : {
		ENTER : ['andNotImageBuffer',IM_BOARD, 'and', 'orImageBuffer', IM_WIPERS.board[2],3],
		TIMEOUT : [TIMING.wipe, 'WipeB_5'],
        down : 'PICKS'
	},
	WipeB_5 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.board[2], 'and', 'orImageBuffer', IM_BOARD,3],
		TIMEOUT : [TIMING.wipe, 'WipeB_6'],
        down : 'PICKS'
	},
	WipeB_6 : {
		ENTER : ['andNotImageBuffer',IM_BOARD, 'and', 'orImageBuffer', IM_WIPERS.board[1],3],
		TIMEOUT : [TIMING.wipe, 'WipeB_7'],
        down : 'PICKS'
	},
	WipeB_7 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.board[1], 'and', 'orImageBuffer', IM_WIPERS.board[0],3],
		TIMEOUT : [TIMING.wipe, 'WipeB_HOLD'],
        down : 'PICKS'
	},	
	WipeB_HOLD : {
		ENTER : ['drawImage',IM_SOLID_COLORS[0]],
		TIMEOUT : [TIMING.wipeHold, 'SPLASH'],
        down : 'PICKS'
	},
	
	// ------------------------------------------------
	
	WIN_cpu : {
		ENTER : ['drawBoard', 'and', 'setButtonColor', 1],
		TIMEOUT : [TIMING.winOn, 'WIN_cpu2']		
	},
	WIN_cpu2 : {
		ENTER : ['drawImage', IM_BOARD, 'and', 'setButtonColor',0],
		TIMEOUT : [TIMING.winOff, 'WIN_cpu']
	},	
	
	WIN_human : {
		ENTER : ['drawBoard', 'and', 'setButtonColor', 2],
		TIMEOUT : [TIMING.winOn, 'WIN_human2']		
	},
	WIN_human2 : {
		ENTER : ['drawImage', IM_BOARD, 'and', 'setButtonColor',0],
		TIMEOUT : [TIMING.winOff, 'WIN_human']
	},	
	
	WIN_tie : {
		ENTER : ['drawBoard', 'and', 'setButtonColor', 3],
		TIMEOUT : [TIMING.winOn, 'WIN_tie2']		
	},
	WIN_tie2 : {
		ENTER : ['drawImage', IM_BOARD, 'and', 'setButtonColor',0],
		TIMEOUT : [TIMING.winOff, 'WIN_tie']
	},	
	
	// ------------------------------------------------
	
	PICKS : {
		ENTER :  ['setButtonColor',0,'and','newGame', 'and', 'pickCPU'],
		random : 'Opp_RANDOM',
		oneder : 'Opp_ONEDER',
		cat :    'Opp_CAT'
	},
	
	Opp_RANDOM : {
		ENTER : ['drawImage', IM_COMPUTER_PLAYERS.mrRandom],
		TIMEOUT : [TIMING.pickCPUOn, 'Opp_RANDOM2']
	},
	Opp_RANDOM2 : {
		ENTER : ['drawImage', IM_SOLID_COLORS[0]],
		TIMEOUT : [TIMING.pickCPUOff, 'Opp_RANDOM3']	
	},
	Opp_RANDOM3 : {
		ENTER : ['drawImage', IM_COMPUTER_PLAYERS.mrRandom],
		TIMEOUT : [TIMING.pickCPUHold, 'PickWipe_1']
	},	
	
	Opp_ONEDER : {
		ENTER : ['drawImage', IM_COMPUTER_PLAYERS.oneder],
		TIMEOUT : [TIMING.pickCPUOn, 'Opp_ONEDER2']
	},
	Opp_ONEDER2 : {
		ENTER : ['drawImage', IM_SOLID_COLORS[0]],
		TIMEOUT : [TIMING.pickCPUOff, 'Opp_ONEDER3']	
	},
	Opp_ONEDER3 : {
		ENTER : ['drawImage', IM_COMPUTER_PLAYERS.oneder],
		TIMEOUT : [TIMING.pickCPUHold, 'PickWipe_1']
	},
	
	Opp_CAT : {
		ENTER : ['drawImage', IM_COMPUTER_PLAYERS.catWoman],
		TIMEOUT : [TIMING.pickCPUOn, 'Opp_CAT2']
	},
	Opp_CAT2 : {
		ENTER : ['drawImage', IM_SOLID_COLORS[0]],
		TIMEOUT : [TIMING.pickCPUOff, 'Opp_CAT3']	
	},
	Opp_CAT3 : {
		ENTER : ['drawImage', IM_COMPUTER_PLAYERS.catWoman],
		TIMEOUT : [TIMING.pickCPUHold, 'PickWipe_1']
	},	
	
	PickWipe_1 : {
		ENTER : ['orImageBuffer', IM_WIPERS.board[0],3],
		TIMEOUT : [TIMING.wipe, 'PickWipe_2']
	},
	PickWipe_2 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.board[0], 'and', 'orImageBuffer', IM_WIPERS.board[1],3],
		TIMEOUT : [TIMING.wipe, 'PickWipe_3']
	},
	PickWipe_3 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.board[1], 'and', 'orImageBuffer', IM_BOARD,3],
		TIMEOUT : [TIMING.wipe, 'PickWipe_4']
	},
	PickWipe_4 : {
		ENTER : ['andNotImageBuffer',IM_BOARD, 'and', 'orImageBuffer', IM_WIPERS.board[2],3],
		TIMEOUT : [TIMING.wipe, 'PickWipe_5']
	},
	PickWipe_5 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.board[2], 'and', 'orImageBuffer', IM_BOARD,3],
		TIMEOUT : [TIMING.wipeHold, 'Pick2']
	},	
	
	Pick2 : {
		ENTER : ['pickFirstPlayer'],
		human : 'PLAY_HUMAN',
		cpu :   'PLAY_CPU'	
	},
	
	// ------------------------------------------------
	
	OVER_HUMAN : {
		ENTER : ['setButtonColor',2, 'and', 'drawBoard'],
		TIMEOUT : [TIMING.winOn, 'OVER_HUMAN2'],
		down : 'OverWipe_1'
	},
	OVER_HUMAN2 : {
		ENTER : ['setButtonColor',0, 'and', 'drawImage', IM_SOLID_COLORS[0]],
		TIMEOUT : [TIMING.winOff, 'OVER_HUMAN'],
		down : 'OverWipe_1'
	},
	
	OVER_CPU : {
		ENTER : ['setButtonColor',1, 'and', 'drawBoard'],
		TIMEOUT : [TIMING.winOn, 'OVER_CPU2'],
		down : 'OverWipe_1'
	},
	OVER_CPU2 : {
		ENTER : ['setButtonColor',0, 'and', 'drawImage', IM_SOLID_COLORS[0]],
		TIMEOUT : [TIMING.winOff, 'OVER_CPU'],
		down : 'OverWipe_1'
	},
	
	OVER_TIE : {
		ENTER : ['setButtonColor',3, 'and', 'drawBoard'],
		TIMEOUT : [TIMING.winOn, 'OVER_TIE2'],
		down : 'OverWipe_1'
	},
	OVER_TIE2 : {
		ENTER : ['setButtonColor',0, 'and', 'drawImage', IM_SOLID_COLORS[0]],
		TIMEOUT : [TIMING.winOff, 'OVER_TIE'],
		down : 'OverWipe_1'
	},
	
	OverWipe_1 : {
		ENTER : ['setButtonColor','0','and','orImageBuffer', IM_WIPERS.diag[0],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_2']
	},
	OverWipe_2 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[0], 'and', 'orImageBuffer', IM_WIPERS.diag[1],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_3']
	},
	OverWipe_3 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[1], 'and', 'orImageBuffer', IM_WIPERS.diag[2],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_4']
	},
	OverWipe_4 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[2], 'and', 'orImageBuffer', IM_WIPERS.diag[3],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_5']
	},
	OverWipe_5 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[3], 'and', 'orImageBuffer', IM_WIPERS.diag[4],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_6']
	},
	OverWipe_6 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[4], 'and', 'orImageBuffer', IM_WIPERS.diag[5],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_7']
	},
	OverWipe_7 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[5], 'and', 'orImageBuffer', IM_WIPERS.diag[6],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_8']
	},
	OverWipe_8 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[6], 'and', 'orImageBuffer', IM_WIPERS.diag[7],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_9']
	},
	OverWipe_9 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[7], 'and', 'orImageBuffer', IM_WIPERS.diag[8],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_10']
	},
	OverWipe_10 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[8], 'and', 'orImageBuffer', IM_WIPERS.diag[9],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_11']
	},
	OverWipe_11 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[9], 'and', 'orImageBuffer', IM_WIPERS.diag[10],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_12']
	},
	OverWipe_12 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[10], 'and', 'orImageBuffer', IM_WIPERS.diag[11],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_13']
	},
	OverWipe_13 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[11], 'and', 'orImageBuffer', IM_WIPERS.diag[12],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_14']
	},
	OverWipe_14 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[12], 'and', 'orImageBuffer', IM_WIPERS.diag[13],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_15']
	},
	OverWipe_15 : {
		ENTER : ['andNotImageBuffer',IM_WIPERS.diag[13], 'and', 'orImageBuffer', IM_WIPERS.diag[14],3],
		TIMEOUT : [TIMING.wipe, 'OverWipe_HOLD']
	},	
	OverWipe_HOLD : {
		ENTER : ['drawImage',IM_SOLID_COLORS[0]],
		TIMEOUT : [TIMING.wipeHold, 'SPLASH']        
	},
		
	// ------------------------------------------------
	
	PLAY_HUMAN : {
		ENTER :   ['setButtonColor', 2, 'and', 'advanceCursor'],
	    TIMEOUT : [0, 'InputA']
	},
	
	InputA : {
		ENTER : ['setCellAtCursor', 3, 'and', 'drawBoard'],
	    TIMEOUT : [TIMING.inputDown, 'InputB'],
	    down : 'InputC'
	},
	
	InputB : {
		ENTER : ['setCellAtCursor', 0, 'and', 'drawBoard'],
		TIMEOUT : [TIMING.inputDown, 'InputA'],
	    down : 'InputC'
	},
	
	InputC : {
		ENTER : ['setCellAtCursor', 3, 'and', 'drawBoard'],
		TIMEOUT : [TIMING.inputHeld, 'HMove'],
	    up : ['PLAY_HUMAN', 'setCellAtCursor', 0]
	},
			
	HMove : {
		ENTER : ['setCellAtCursor', 2, 'and',  'drawBoard', 'and', 'getGameState'],
		cpu :   'OVER_CPU',
		human : 'OVER_HUMAN',
		play :  'PLAY_CPU',
		tie :   'OVER_TIE'
	},
	
	
		
	PLAY_CPU : {
		ENTER : ['setButtonColor',1, 'and', 'getCPUMove', 'and', 'setCellAtCursor',1,'and','drawBoard'],
	    TIMEOUT : [TIMING.cpuOn, 'OppC1']
	},
	
	OppC1 : {
		ENTER : ['setCellAtCursor',0, 'and', 'drawBoard'],
	    TIMEOUT : [TIMING.cpuOff, 'OppC2']
	},
	
    OppC2 : {
    	ENTER : ['setCellAtCursor',1, 'and', 'drawBoard'],
	    TIMEOUT : [TIMING.cpuOn, 'OppC3']
	},
	
	OppC3 : {
		ENTER : ['setCellAtCursor',0, 'and', 'drawBoard'],
	    TIMEOUT : [TIMING.cpuOff, 'MoveCPU']
	},
	
    MoveCPU : {
    	ENTER : ['setCellAtCursor',1, 'and', 'drawBoard', 'and', 'getGameState'],
    	cpu :   'OVER_CPU',
		human : 'OVER_HUMAN',
		play :  'PLAY_HUMAN',
		tie :   'OVER_TIE'
	},	
	
}

var cursor;
var board;
var cpu;

var imageBuffer = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

function randomInt(high) {
	return Math.floor(Math.random() * (high));
}


MACHINE.log = function(value) {
	console.log(value);
}

MACHINE.drawBoard = function() {
	imageBuffer = IM_BOARD.slice();
	for(var x=0;x<9;++x) {
		if(board[x]!=0) {
			for(var y=0;y<16;++y) {
				imageBuffer[y] = imageBuffer[y] | IM_GAME_CELLS[x][y] & IM_SOLID_COLORS[board[x]][y]; 
			}
		}
	}
	hardware.drawImage(imageBuffer);	
}

MACHINE.newGame = function() {
	board = [0,0,0,  0,0,0,  0,0,0];	
	cursor = 8; // First advance ... back to 0	
}

MACHINE.pickCPU = function() {	
	cpu = randomInt(3);
	if(cpu==0) {
		runner.handleEvent('random');
	} else if(cpu==1) {
		runner.handleEvent('oneder');
	} else {
		runner.handleEvent('cat');
	}	
}

MACHINE.pickFirstPlayer = function() {
	if(randomInt(2)==0) {
		runner.handleEvent('human');
	} else {
		runner.handleEvent('cpu');
	}
}

MACHINE.setCellAtCursor = function(color) {
	board[cursor] = color;
}

MACHINE.advanceCursor = function() {
	for(var x=0;x<9;++x) {
		++cursor;
		if(cursor==9) {
			cursor=0;
		}
		if(board[cursor]==0) {
			return;
		}
	}
}

var WINS = [
	[0,1,2],[3,4,5],[6,7,8],        
	[0,3,6],[1,4,7],[2,5,8],
	[0,4,8],[2,4,6]
];

function checkBoard(b) {
	for(var x=0;x<WINS.length;++x) {
		var tripple = WINS[x];
		if(b[tripple[0]]==0) continue;
		if(b[tripple[0]]==b[tripple[1]] && b[tripple[0]]==b[tripple[2]]) {
			if(b[tripple[0]] == 1) {
				return 'cpu';
			} else {
				return 'human';				
			}
		}
	}	
	for(var x=0;x<9;++x) {
		if(b[x]==0) {
			return 'play';
		}
	}	
	return 'tie';	
}

MACHINE.getGameState = function() {	
	var ret = checkBoard(board);
	runner.handleEvent(ret);	
}

function getMoveRandom() {
	while(true) {
		var x = randomInt(9);
		if(board[x]==0) {
			return x;
		}
	}
}

function getMoveOneder() {
	// Look for a win
	for(var x=0;x<9;++x) {
		if(board[x]!=0) continue;
		board[x] = 1;
		var res=checkBoard(board);
		board[x] = 0;
		if(res=='cpu') {
			return x;
		}
	}	
	// Look for a block
	for(var x=0;x<9;++x) {
		if(board[x]!=0) continue;
		board[x] = 2;
		var res=checkBoard(board);
		board[x] = 0;
		if(res=='human') {
			return x;
		}
	}	
	return -1;
}

function getMoveCat() {
	var num = 0;
	for(var x=0;x<9;++x) {
		if(board[x]>0) ++num;
	}
	
	// Moves made (computer goes first):
	// - 0: Pick upper left
	// - 2: Pick center if free or bottom right
	// - 4: If opponent in 1 - take 6. If opponent in 3 - take 2
	if(num==0) {
		return 0;
	} else if(num==2) {
		if(board[4]==0) return 4;
		return 8;
	} else if(num==4) {
		if(board[1]==2) return 6;
		if(board[3]==2) return 2;
		return -1;
	}
	
	// Moves made (human goes first):
	// - 1: Pick center if free or random corner (bottom right ... same as 2 above)
	// - 3: Pick random middle
	else if(num==1) {
		if(board[4]==0) return 4;
		return 8;
	} else if(num==3) {
		if(board[1]==0) return 1;
		if(board[3]==0) return 3;
		if(board[5]==0) return 5;
		if(board[7]==0) return 7;
		return -1;
	}
	
	return -1;
}

MACHINE.getCPUMove = function() {
	var move = 0;
	if(cpu==2) { // CAT
		move = getMoveOneder();
		if(move>=0) {
			cursor = move;
			return;
		}
		move = getMoveCat();
		if(move>=0) {
			cursor = move;
			return;
		}		
	} else if(cpu==1) { // Oneder
		move = getMoveOneder();
		if(move>=0) {
			cursor = move;
			return;
		} 
	} 	
	cursor = getMoveRandom();
}

MACHINE.setButtonColor = function(value) {
	hardware.setButtonColor(value);
}

MACHINE.drawImage = function(image) {
	imageBuffer = image.slice(); // Make a copy
	hardware.drawImage(imageBuffer);
}

MACHINE.orImageBuffer = function(image, color) {
	for(var x=0;x<16;++x) {
		imageBuffer[x] = imageBuffer[x] | image[x] & IM_SOLID_COLORS[color][x];
	}
	hardware.drawImage(imageBuffer);
}

MACHINE.andNotImageBuffer = function(image) {
	for(var x=0;x<16;++x) {
		imageBuffer[x] = imageBuffer[x] & ~image[x];
	}
	hardware.drawImage(imageBuffer);
}



var runner = require('./FSMRunner.js');

var hardware = require('./Hardware.js');

function buttonEventListener(event) {
	runner.handleEvent(event);
}

hardware.init(buttonEventListener, function() {	
	runner.init(MACHINE,'SPLASH');	
});





