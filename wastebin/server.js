const express = require('express')
const app = express()

app.get('/', function(req, res) {
    res.sendFile(`${__dirname}/index.html`);
    // res.send(__dirname + "\\" + "index.html")
  });
  app.get('/paste', function(req, res) {
    res.sendFile(`${__dirname}/preview_paste.html`);
    // res.send(__dirname + "\\" + "index.html")
  });

app.listen(3000)
