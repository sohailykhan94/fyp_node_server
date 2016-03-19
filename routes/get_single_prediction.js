var express = require('express');
var router = express.Router();
var sys = require('sys')
var exec = require('child_process').exec;
var child;
var fs = require('fs');

router.use(function(req, res, next){
  console.log('Prediction Single API');
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
    var queryString = "/home/sohailyarkhan/anaconda2/bin/python /home/sohailyarkhan/node-server/fyp_node_server/prediction_single.py " + String(req.query.year) + " " + String(req.query.month) + " " + String(req.query.day) + " " + String(req.query.hours) + " " + String(req.query.minutes) + " " + String(req.query.src) + " " + String(req.query.des);
    console.log(queryString);
    // executes `pwd`
    child = exec(queryString, function (error, stdout, stderr) {
      if(stdout){
        stdout = stdout.replace('[\'','');
        stdout = stdout.replace('\']','');
        stdout = stdout.replace(/(?:\r\n|\r|\n)/g,'');
        var tempJSON = JSON.parse(fs.readFileSync('./speedMap.json', 'utf8'));
        var label = stdout;
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
      //sys.print('stdout: ' + stdout);
      //sys.print('stderr: ' + stderr);
      if (error !== null) {
        console.log('exec error: ' + error);
      }
    });
  }else{
    res.status(404);
    res.json({status: 'error', data: 'error'});
  }
});

//2,11,2014,19,0,4651,4631, 30

module.exports = router;
