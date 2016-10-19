import socket
import sys
import time
import os #kanske onödigt därför att vi redan har sys, men vet inte. //Jonte
from _thread import * #vad gör det? (importerade för att du har den på servern...) //Jonte

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_server="localhost" #jag är 10.164.137.191
port=5555
quit=0
try:
	s.connect((chat_server,port))
	print ("yay!")
	data = s.recv(2048)
	motd = 'Message of the day: ' + data.decode('utf-8')
	print(str(motd))
	s.send(str.encode("does it work?"))
	second_data = s.recv(2048)
	second_reply = second_data.decode('utf-8')
	print(str(second_reply))
	while quit==0:
		client_message = input(">>>")
		if client_message == "quit":
			quit=1
		else:
			s.send(str.encode(client_message))
			message_data = s.recv(2048)
			server_message = message_data.decode('utf-8')
			print (server_message)
	os.system("pause")
	s.close()
except socket.error as e:
	print(e)






