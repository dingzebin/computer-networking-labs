import socket, os
from pathlib import Path, WindowsPath
from threading import Thread

HOST=''
PORT=9090
ROOT_PATH='./html'

class ConnectionHanlder(Thread): 
  def __init__(self, conn, remote_addr):
    Thread.__init__(self)
    self.conn = conn
    self.remote_addr = remote_addr
  def run(self): 
    with self.conn:
      print('Connected by', self.remote_addr)
      while True:
        data = self.conn.recv(1024)
        if not data: break
        p = Path(ROOT_PATH + data.decode().splitlines()[0].split(' ')[1])
        if not p.exists() or p.is_dir(): 
          self.conn.sendall(self.response(404, 'Not Found', '<html><body><h1>404 Not Found</h1></body></html>').encode())
          break
        else:
          with p.open() as f:
            # read the file all lines
            self.conn.sendall(self.response(200, 'OK', f.read()).encode())
            break
  def response(self, status, msg, data): 
    return 'HTTP/1.1 ' + str(status) + ' ' + msg + '\r\n' \
      'Server: python-server \r\n' \
      'Content-Type: text/html; charset=utf-8 \r\n' \
      '\r\n' + data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen(1) # set backlog
  while True:
    conn, addr = s.accept()
    handler = ConnectionHanlder(conn, addr)
    handler.start()