import socket
import threading


class Client:
    """ Client class for my chat. """
    def __init__(self, address=('', 10000)):
        """ Save desired address for connection. """
        self._address = address
        self.sock = socket.socket()
        self.listener = threading.Thread(target=self.listen, args=(), daemon=True)
        self._is_active = False

    def start(self):
        """ Method to start chat client """
        self.sock.connect(self._address)
        self.listener.start()
        self._is_active = True
        while self._is_active:
            message = input()
            try:
                self.sock.send(message.encode('utf-8'))
            except socket.error:
                self.sock.detach()
                self.sock.close()
                break

    def listen(self):
        """ Method for background message receiving. """
        while True:
            try:
                data_r = self.sock.recv(1024)
            except socket.error:
                print('Socket error. Connection closed! Hit Enter...')
                self._is_active = False
                self.sock.detach()
                self.sock.close()
                break
            if not data_r:
                print('Connection closed! Hit Enter...')
                self._is_active = False
                self.sock.detach()
                self.sock.close()
                break
            message = data_r.decode('utf-8')
            print(message)


c = Client()
c.start()
