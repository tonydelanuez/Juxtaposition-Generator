// Require the functionality we need to use:
var http = require('http'),
	url = require('url'),
	path = require('path'),
	mime = require('mime'),
	path = require('path'),
	fs = require('fs');
 
var PythonShell = require('python-shell');
var schedule = require('node-schedule');
var done = false;
var theComment = "";
var express = require('express');
var app = express();
var json_array = "";


PythonShell.run('scraper.py', function () {
  //if (err) throw err;
  console.log('finished running scraper');
  //console.log(theComment);
  grabJSON();
});

//Rerun python script every 45 minutes
var rule = new schedule.RecurrenceRule();
rule.minute = 45;
var j = schedule.scheduleJob(rule, function(){
	PythonShell.run('/app/scraper.py', function () {
	  //if (err) throw err;
	  console.log('Refreshed ');
	  //console.log(theComment);
	  grabJSON();
	});
});

function randomKey(){
	var objKeys = Object.keys(my_json);
	var randomKey = objKeys[Math.floor(Math.random() *objKeys.length)];
	theComment= my_json[randomKey];
	console.log(theComment);
}

function grabJSON(){
	//Convert CSV to JSON
	const csv=require('csvtojson')
	my_json = "";
	csv({noheader:true})
	.fromFile("comments.csv")
	.on('json',(json)=>{ 
		my_json = json;

	})
	.on('done',()=>{
	    console.log('end');
	});
}


app.use('/', express.static(path.join(__dirname, 'app')));

app.get("/data", function(req, res){
	PythonShell.run('scraper.py', function () {
	  //if (err) throw err;
	  console.log('data requested');
	  //console.log(theComment);
	  randomKey();
	});
	res.send(theComment);
});
app.listen(process.env.PORT || 3456);
