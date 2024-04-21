from status import handle_200, handle_300, handle_404, handle_501
import socket
import os
import mimetypes

class TCPServer:
    
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(1)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            data = conn.recv(1024) 

            response = self.handle_request(data)

            conn.sendall(response)
            conn.close()

    def handle_request(self, data):
        return data

class HTTPServer(TCPServer):
    
    headers = {
        'Server': 'hjhj',
        'Content-Type': 'text/html',
    }  
    
    def handle_request(self, data):
        request = HTTPRequest(data)

        try:
            handler = getattr(self, 'handle_%s' % request.method)
        except:
            handler = handle_501.handler(self.response_headers())
        respone = handler(request)
        return respone
    
    def response_line(self, status_code):
        reason = self._STATUSES[status_code]
        response_line = 'HTTP/1.1 %s %s\r\n' % (status_code, reason)
        return response_line.encode()
    
    def response_headers(self, extra_headers=None):
        
        headers_copy = self.headers.copy() 

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ''

        for h in headers_copy:
            headers += '%s: %s\r\n' % (h, headers_copy[h])

        return headers.encode()

    def handle_options(self, request):
        response_line = self.response_line(200)
        extra_headers = {'Allow': 'OPTIONS, GET'}
        response_headers = self.response_headers(extra_headers)

        blank_line = b'\r\n'

        return b''.join([response_line, response_headers, blank_line])
        
    def handle_GET(self, request):
        
        path = request.uri.strip('/') 
        if not path:
            path = 'index.html'

        if os.path.exists(path) and not os.path.isdir(path): 
            response_line = handle_200.handler()
            content_type = mimetypes.guess_type(path)[0] or 'text/html'
            extra_headers = {'Content-Type': content_type}
            response_headers = self.response_headers(extra_headers)
            with open(path, 'rb') as f:
                response_body = f.read()
                
        else:
            response_headers = self.response_headers()
            response_line, response_body = handle_404.handler()
            
        blank_line = b'\r\n'
        response = b''.join([response_line, response_headers, blank_line, response_body])
        return response
    
class HTTPRequest:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = '1.1' 
        self.parse(data)
        
    def parse(self, data):
        lines = data.split(b'\r\n')

        request_line = lines[0] 

        words = request_line.split(b' ') 
        self.method = words[0].decode() 

        if len(words) > 1:
            self.uri = words[1].decode() 

        if len(words) > 2:
            self.http_version = words[2]
        
if __name__ == '__main__':
    server = HTTPServer()
    server.start()