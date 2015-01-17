#!/usr/bin/python3.4
import http.server
import socketserver
import helvar

helvarNet = helvar.HelvarNet('10.254.1.2', 50000)        
leds = [helvar.LedUnit(helvarNet, '1.2.1.1'),
        helvar.LedUnit(helvarNet, '1.2.1.2'),
        helvar.LedUnit(helvarNet, '1.2.1.3'),
        helvar.LedUnit(helvarNet, '1.2.1.4'),
        helvar.LedUnit(helvarNet, '1.2.1.5')]

class Handler(http.server.BaseHTTPRequestHandler):
    def __parse_url(self):
        parts = self.path.split('/')
        print(self.path)
        return {'base' : parts[1],
                'id' : int(parts[2]),
                'level' : int(parts[3]),
                'fade_time' : int(parts[4])}

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        req = self.__parse_url()
        try:
            if (req['base'] == 'lamp'):
                leds[req['id']].set(req['level'], req['fade_time'])
            self.send_response(200)
        except:
            print("oops:", req)
            self.send_response(501)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        #self.wfile.close()


    def lel(self):
        pass

PORT = 8002


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
