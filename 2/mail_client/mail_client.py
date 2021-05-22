import socket
import base64

SMTP_ADDR = 'smtp.163.com'
SMTP_PORT = 25
USER_NAME = ''
PASSWORD = ''


class MailUtil(object): 
  def __init__(self, smtp_addr, smtp_port, user_name, password):
    self.smtp_addr = smtp_addr
    self.smtp_port = smtp_port
    self.user_name = user_name
    self.password = password

  def send(self, to_email, subject, content):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.smtp_addr, self.smtp_port))
      s.send(b'HELO 163.com\r\n')
      print('C: HELO 163.com')
      message = s.recv(512)
      print('S: ' + message.decode())

      s.send(b'auth login\r\n')
      print('C: auth login')
      m = s.recv(1024)
      print('S: ' + m.decode())
      
      s.send(((base64.b64encode(self.user_name.encode())).decode() + '\r\n').encode())
      print('C: ' + base64.b64encode(self.user_name.encode()).decode())
      message = s.recv(1024)
      print('S: ' + message.decode())
      
      s.send(((base64.b64encode(self.password.encode())).decode() + '\r\n').encode())
      print('C: ' + base64.b64encode(self.password.encode()).decode())
      message = s.recv(1024)
      print('S: ' + message.decode())

      s.send(('MAIL FROM: <' + self.user_name + '>\r\n').encode())
      print('C: MAIL FROM: <' + self.user_name + '>')
      message = s.recv(1024)
      print('S: ' + message.decode())
      
      s.send(('RCPT TO: <' + to_email + '>\r\n').encode())
      print('C: RCPT TO: <' + to_email + '>')
      message = s.recv(1024)
      print('S: ' + message.decode())

      s.send(b'DATA\r\n')
      print('C: DATA')
      message = s.recv(1024)
      print('S: ' + message.decode())
      
      s.send(('FROM: ' + self.user_name + '\r\n').encode())
      s.send(('To: ' + to_email + '\r\n').encode())
      s.send(('Subject: ' + subject + '\r\n').encode())
      s.send(b'\r\n')
      s.send(content.encode())
      s.send(b'\r\n')
      s.send(b'.\r\n')
      
      message = s.recv(1024)
      print('S: ' + message.decode())
      s.send(b'QUIT\r\n')

      message = s.recv(1024)
      print('S: ' + message.decode())

mailUtil = MailUtil(SMTP_ADDR, SMTP_PORT, USER_NAME, PASSWORD)
mailUtil.send('to_email', 'test smtp', 'em....no more content')

