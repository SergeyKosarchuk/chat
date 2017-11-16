import socket
import threading
import unittest


class TestServer(unittest.TestCase):
    ''' Class for testing server side chat app. '''
    addr = ('', 10000)
    message = 'hello'
    def setUp(self):
        self.sock_to_listen = socket.socket()
        self.sock_to_listen.bind(self.addr)
        tr = threading.Thread(target=self.listen, args=(self.sock_to_listen,), daemon=True)
        tr.start()

    def tearDown(self):
        self.sock_to_listen.close()

    def listen(self, sock):
        ''' Start listen to clients for messages. '''
        sock.listen()
        conn, address = sock.accept()
        while conn:
            data = conn.recv(1024)
            self.recived_message = data.decode('utf-8')
        

    def test_send(self):
        """ Check send/recive message """
        with socket.create_connection(self.addr) as sock:
            data = self.message.encode(encoding='utf_8')
            sock.send(data)
        self.assertEqual(self.message, self.recived_message)