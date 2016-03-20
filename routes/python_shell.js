var express = require('express');
var router = express.Router();
var sys = require('sys')
var exec = require('child_process').exec;
var child;
var fs = require('fs');
var PythonShell = require('python-shell');
var options = {
  mode: 'text',
  scriptPath: '/home/sohailyarkhan/node-server/fyp_node_server/',
  pythonPath: '/home/sohailyarkhan/anaconda2/bin/python'
};
var pyshell = new PythonShell('single_predict_input.py',options);

router.use(function(req, res, next){
  console.log('Prediction Single Input Python API');
  next();
})

router.get('/', function(req, res, next) {

  if(req.query.day && req.query.month && req.query.year && req.query.hours && req.query.minutes && req.query.src && req.query.des){
    var day = parseInt(req.query.day);
    var month = parseInt(req.query.month);
    var year = parseInt(req.query.year);
    var hours = parseInt(req.query.hours);
    var minutes = parseInt(req.query.minutes);
    var src = parseInt(req.query.src);
    var des = parseInt(req.query.des);
    var tempJSON = JSON.parse(fs.readFileSync('./speedMapSrcDes.json', 'utf8'));
    for(var i= 0;i<tempJSON.length-1;i++){
      if(tempJSON[i].src == src && tempJSON[i].des == des){
        var src_lat = tempJSON[i].src_lat;
        var src_long = tempJSON[i].src_long;
        var des_lat = tempJSON[i].des_lat;
        var des_long = tempJSON[i].des_long;
      }
    }
    var queryString = String(req.query.year) + " " + String(req.query.month) + " " + String(req.query.day) + " " + String(req.query.hours) + " " + String(req.query.minutes) + " " + String(req.query.src) + " " + String(req.query.des) + '\n\r';
    console.log(queryString);
    // executes `pwd`
    pyshell.send(queryString);
    pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
      console.log(message);
      if(message){
        message = message.replace('[\'','');
        message = message.replace('\']','');
        message = message.replace(/(?:\r\n|\r|\n)/g,'');
        var label = message;
          var result = {
            src_lat: src_lat,
            src_long: src_long,
            des_lat: des_lat,
            des_long: des_long,
            road_saturation_level: label
          }
        res.status(200);
        res.json({status: 'success', nodes: result});
      }else{
        res.status(404);
        res.json({status: 'error', data: 'error'});
      }
    });
  }else{
    res.status(404);
    res.json({status: 'error', data: 'error'});
  }
});

//2,11,2014,19,0,4651,4631, 30

module.exports = router;
