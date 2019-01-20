/**
 * Server-sent Event 例子，运行
 * $ node sse.js
 * see http://javascript.ruanyifeng.com/htmlapi/eventsource.html#toc18
 */

const http = require('http')

http.createServer(function(req, res) {
    let filename = '.' + req.url;

    if (filename === './steam') {
        res.writeHead(200, {
            'Content-Type': 'text/event-steam',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*'
        });
        res.write('retry: 10000\n');
        res.write('event connectime\n')
        res.write("data: " + (new Date()) + "\n\n");
        res.write("data: " + (new Date()) + "\n\n");

        interval = setInterval(function () {
            res.write("data: " + (new Date()) + "\n\n");
        }, 1000);

        req.connection.addListener('close', function() {
            clearInterval(interval);
        }, false);
      
    }
}).listen(8844);
