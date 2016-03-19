var express = require('express');
var router = express.Router();
var sys = require('sys')
var exec = require('child_process').exec;
var child;
var fs = require('fs');

router.use(function(req, res, next){
  console.log('Prediction API');
  next();
})

router.get('/', function(req, res, next) {

  if(req.query.day && req.query.month && req.query.year && req.query.hours && req.query.minutes){
    var queryString = "/home/sohailyarkhan/anaconda2/bin/python /home/sohailyarkhan/node-server/fyp_node_server/prediction.py " + String(req.query.year) + " " + String(req.query.month) + " " + String(req.query.day) + " " + String(req.query.hours) + " " + String(req.query.minutes);
    console.log(queryString);
    // executes `pwd`
    child = exec(queryString, function (error, stdout, stderr) {
      if(stdout){
        stdout = stdout.replace('[','');
        stdout = stdout.replace(']','');
        stdout = stdout.replace(/(?:\r\n|\r|\n)/g,'');
        splitArray = stdout.split("\' \'");
        splitArray[0] = splitArray[0].replace('\'','');
        splitArray[splitArray.length-1] = splitArray[0].replace('\'','');
        console.log(splitArray);
        var tempJSON = JSON.parse(fs.readFileSync('./speedMap.json', 'utf8'));
        for(var i = 0; i<splitArray.length; i++){
          tempJSON[i].road_saturation = splitArray[i];
        }
        res.status(200);
        res.json({status: 'success', nodes: tempJSON});
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
