from app import create_app
from gevent.pywsgi import WSGIServer

app = create_app()

if __name__ == '__main__':
    print("KumohCheck judgement server!")
    
    server = WSGIServer(('0.0.0.0', 4000), app)
    server.serve_forever()