from wsgiref.simple_server import make_server

def hello(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    return [b'<h1>Hello World</h1>']

class AppClass:
    
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
    
    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-Type', 'text/html')]
        self.start(status, response_headers)
        yield b'<h1>Hello World</h1>'


server = make_server('localhost', 5000, hello)
server.serve_forever()