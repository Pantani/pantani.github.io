const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = '/Users/pantani/Desktop/go/src/github.com/Pantani/pantani.github.io';
const PORT = 8099;
const types = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.jpg': 'image/jpeg',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.txt': 'text/plain',
  '.xml': 'application/xml',
};

http
  .createServer((req, res) => {
    let p = decodeURIComponent(req.url.split('?')[0]);
    if (p === '/') p = '/index.html';
    const fp = path.join(ROOT, p);
    if (!fp.startsWith(ROOT)) {
      res.writeHead(403);
      return res.end('forbidden');
    }
    fs.readFile(fp, (e, data) => {
      if (e) {
        res.writeHead(404);
        return res.end('not found');
      }
      res.writeHead(200, { 'Content-Type': types[path.extname(fp)] || 'application/octet-stream' });
      res.end(data);
    });
  })
  .listen(PORT, () => console.log('serving on ' + PORT));
