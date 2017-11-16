import socket
import threading
from datetime import datetime
import queue


class Server:
    """ Класс сервера. Ипользуй метод старт для включения. """
    def __init__(self, address=('', 10000)):
        self.sock = socket.socket()
        self._address = address
        self._clients = {}
        self._is_running = False
        self._queue = queue.Queue()

    def stop(self):
        """ Остановка сервера. """
        pass

    def control(self):
        while True:
            command = input()
            if command == 'exit':
                self._is_running = False
                self.sock.close()
                self.sock.detach()

    def start(self):
        """ Включить сервер и запустить сразу по потоку на чтение команд и отправку сообщений. """
        self.sock.bind(self._address)
        self.sock.listen()
        self._is_running = True
        sender = threading.Thread(target=self.send, daemon=True)
        controller = threading.Thread(target=self.control, daemon=True)
        sender.start()
        controller.start()
        print('Server Started!')
        while self._is_running:
            try:
                conn, address = self.sock.accept()
            except:
                break
            client_worker = threading.Thread(target=self.worker, args=(conn, address,), daemon=True)
            client_worker.start()
        print('Server Closed!')

    def send(self):
        """ Рассылаем всем клиентам сообщения в очереди. """
        while True:
            message = self._queue.get()
            for sock in self._clients.values():
                sock[0].send(message.encode())

    def worker(self, conn, address):
        with conn:
            name = self.authorization(conn, address)
            conn.send(b'Chat activated, say "hello"')
            print(f'Client {name} connected from address:{address}')
            self._clients[name] = (conn, address)
            while True:
                try:
                    data = conn.recv(1024)
                except socket.timeout:
                    print('Connection closed by timeout')
                    self._clients.pop(name)
                    break
                if not data:
                    print(f'Client {name} disconnected')
                    self._clients.pop(name)
                    break  # Выходим из цикла если клиент отключился.
                message = data.decode('utf-8')
                time = datetime.now().strftime('%H:%M:%S')
                message = f'{time}[{name}]:{message}'
                self._queue.put(message)

    def check_address(self, address):
        """ Проверяем есть ли этот адрес в клиентах. """
        return None

    def authorization(self, conn, address):
        conn.send(b'Input your name.')
        name = self.check_address(address)
        while not name:
            data = conn.recv(1024)
            name = data.decode('utf-8')
            if name in self._clients.keys():
                conn.send(b'It is already taken! Please input another name.')
                name = None
        return name


server = Server()
server.start()
