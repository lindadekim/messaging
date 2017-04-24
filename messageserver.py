#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from requestrouter import ActionDetail
import requestrouter

PORT_NUMBER= 9090

class MessagingServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        actionDetail = requestrouter.parseURL(self.path, "GET")        
        self.wfile.write(actionDetail.execute())
        
    def do_DELETE(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        actionDetail = requestrouter.parseURL(self.path, "DELETE")
        self.wfile.write(actionDetail.execute())
        
        
    def do_POST(self):
        content_len=self.headers.getheaders('content-length')        
        len = int(content_len[0]) if content_len else 0
        postdata = self.rfile.read(len)                
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        actionDetail = requestrouter.parseURL(self.path, "POST", postdata)
        self.wfile.write(actionDetail.execute())
        
if __name__ == '__main__':
    try:
        httpd = HTTPServer(('', PORT_NUMBER), MessagingServerHandler)
        httpd.serve_forever()        
    except KeyboardInterrupt:
        print 'interrupted'
    httpd.server_close()
    
    