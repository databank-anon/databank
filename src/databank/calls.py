from threading import Thread
import socket
import pickle
from Crypto.Cipher import AES

def join_route(app_id, route):
    return "/{}{}".format(app_id, route)

TCP_PORT_S = 3141
TCP_PORT_D = 3142

BUFFER_SIZE = 65536
TIMEOUT     = 5
DEFAULT_IP  = '0.0.0.0'
THREADS_N   = 10

BLOCK_SIZE  = 16

def pad(msg):
    padding = BLOCK_SIZE - (len(msg)-1) % BLOCK_SIZE - 1
    return msg + padding * b' '

## Distant function calls: server side

class ClientHandler(Thread):

    def __init__(self, id_, server, conn):
        super(ClientHandler, self).__init__()
        self.id_ = id_
        self.server = server
        self.conn = conn

    def run(self):
        function, args, kwargs = pickle.loads(self.server.aes[self.id_].decrypt(
            self.conn.recv(BUFFER_SIZE)).strip())
        function = join_route(self.id_, function)
        if function in self.server.callbacks:
            app, f = self.server.callbacks[function]
            app.callback_user_id = -self.id_
            app.callback_user_name = str(-self.id_)
            result = f(*args, **kwargs)
            dump = pickle.dumps(result)
            self.conn.send(self.server.aes[self.id_].encrypt(pad(dump)))
            self.conn.close()

class Server(Thread):

    def __init__(self, databank_side=True):
        super(Server, self).__init__()
        self.callbacks = {}
        self.sp_IP = {}
        self.aes = {}
        self.databank_side = databank_side

    def register_callback(self, id_, rule, app, f):
        self.callbacks[join_route(id_, rule)] = (app, f)

    def register_app(self, id_, sp_IP, key):
        self.sp_IP[sp_IP] = id_
        self.aes[id_] = AES.new(bytes(key, 'utf8'), AES.MODE_EAX)
    
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_port = TCP_PORT_D if self.databank_side else TCP_PORT_S
        sock.bind((DEFAULT_IP, tcp_port))
        sock.listen(THREADS_N)
        while True:
            conn, addr = sock.accept()
            if addr[0] in self.sp_IP:
                client_handler = ClientHandler(self.sp_IP[addr[0]], self, conn)
                client_handler.start()

## Distant function calls: client side

def do_call(msg, addr, databank_side=True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(TIMEOUT)
    tcp_port = TCP_PORT_S if databank_side else TCP_PORT_D
    sock.connect((addr, tcp_port))
    sock.send(msg)
    ret = sock.recv(BUFFER_SIZE).strip()
    sock.close()
    return ret
        
