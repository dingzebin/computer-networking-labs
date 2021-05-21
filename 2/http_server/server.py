import socket, os
from pathlib import Path
from threading import Thread

HOST=''
PORT=9090
ROOT_PATH='./html'

class socketListener(Thread): 
  def run(self): 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((HOST, PORT))
      s.listen(1) # set backlog
      while True:
        conn, addr = s.accept()
        with conn:
          print('Connected by', addr)
          while True:
            data = conn.recv(1024)
            if not data: break
            p = Path(ROOT_PATH + data.decode().splitlines()[0].split(' ')[1])
            if not p.exists() or p.is_dir(): 
              conn.sendall(self.response(404, 'Not Found', '<html><body><h1>404 Not Found</h1></body></html>').encode())
              break
            else:
              with p.open() as f:
                # read the file all lines
                conn.sendall(self.response(200, 'OK', f.read()).encode())
                break
  def response(self, status, msg, data): 
    return 'HTTP/1.1 ' + str(status) + ' ' + msg + '\r\n' \
      'Server: python-server \r\n' \
      'Content-Type: text/html; charset=utf-8 \r\n' \
      '\r\n' + data

pid = os.getpid()
sl = socketListener()
sl.start()
# Why I use this way to stop it because the socket.accept() can not be stopped by ctrl-c
input('Socket is listening, port[' + str(PORT) + '], press any key to abort...')
os.kill(pid,9)
