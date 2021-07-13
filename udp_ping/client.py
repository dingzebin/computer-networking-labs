import socket
import time

serverName = 'localhost'
serverPort = 12000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
  s.settimeout(1)
  i = 0
  print('PING ' + serverName + ': abcd')
  while i < 10:
    start = time.time()
    s.sendto(b'abcd', (serverName, serverPort))
    try:
      message, serverAddr = s.recvfrom(1024)
      print(message.decode() + ' from ' + serverAddr[0] + ': icmp_seq=' + str(i) + ' time=' + str(round(time.time() - start, 3)) + 'ms')
    except:
      print('icmpt_seq=' + str(i) + ' timeout')
    i += 1