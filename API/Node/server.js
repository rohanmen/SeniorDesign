var express = require('express');
var app = express();
var fs = require('fs');
var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = 8080;
var router = express.Router();
var outputFile = 'Node/database.json';
var command_template = 'Node/command_template.json';
var database = JSON.parse(fs.readFileSync(outputFile, 'utf8'));


function writeToFile()
{
	var databaseJSON = JSON.stringify(database);
	console.log(databaseJSON);
	fs.writeFileSync(outputFile, databaseJSON);
}


function addCommand(type, psu_id)
{
	var json = JSON.parse(fs.readFileSync(command_template, 'utf8'));
	json['type'] = type;
	json['psu_id'] = psu_id;
	console.log("here is the json");
	console.log(json);
	database.push(json);
	console.log(database);
	//writeToFile();
}

function addCommand(type, psu_level, psu_id, seconds)
{
	var json = JSON.parse(fs.readFileSync(command_template, 'utf8'));
	json['type'] = type;
	json['psu_level'] = psu_level 
	json['psu_id'] = psu_id;
	json['wait'] = seconds;
	console.log("here is the json");
	console.log(json);
	database.push(json);
	console.log(database);
	//writeToFile();
}

router.get('/', function(req, res) {
    res.json({ message: 'hooray! welcome to our api!' });   
});

router.get('/command', function(req, res) {

	console.log(database);
	console.log(database.length);

	if(database.length > 0)
	{
		res.json(database[0]);
		database.splice(0,1);
		//writeToFile(); 
		//console.log(database);
	}
	else
	{
		var json = JSON.parse(fs.readFileSync(command_template, 'utf8'));
		json['type'] = 'none';
		json['psu_id'] = 0;
		res.json(json);
	}

      
});

/*
router.get('/pull_psu/:psu_id', function(req, res) {
	addCommand('pull_psu', req.params.psu_id);
	//addCommand(req.body.id);
	res.json({message: 'sucess' });
});

router.get('/push_psu/:psu_id', function(req, res) {
	addCommand('push_psu', req.params.psu_id);
	//addCommand(req.body.id);
	res.json({message: 'sucess' });
});
*/

router.get('/wait/:seconds', function(req, res) {
	addCommand('wait', 0, 0, req.params.seconds);
	//addCommand(req.body.id);
	res.json({message: 'sucess' });
});


router.get('/pull_psu/:psu_id', function(req, res) {
	addCommand('pull_psu', 0, req.params.psu_id, 0);
	//addCommand(req.body.id);
	res.json({message: 'sucess' });
});

router.get('/push_psu/:psu_id', function(req, res) {
	addCommand('push_psu', 0, req.params.psu_id, 0);
	//addCommand(req.body.id);
	res.json({message: 'sucess' });
});

router.get('/pull_wait_push/:psu_level?/:psu_id?/:seconds?', function(req, res) {
	addCommand('pull_push_wait', req.params.psu_level, req.params.psu_id, req.params.seconds);
	//addCommand(req.body.id);
	res.json({message: 'sucess' });
});



app.use('/api', router);

app.listen(port, '0.0.0.0');
console.log('Starting port ' + port);


process.stdin.resume();
process.on('exit', function() {
	writeToFile();
	process.exit();
});
process.on('SIGINT', function() {
	writeToFile();
	process.exit();
});
process.on('uncaughtException', function() {
	writeToFile();
	process.exit();
});

