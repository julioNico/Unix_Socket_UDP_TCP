#!/usr/bin/env python3

import socket
import time
import statistics
import base64

received = 0
transmitted = 0
end_time = 0
start_time = 0

b5 = '00000'
ping = '0' #b6
timestamp = round(time.time()) #timestemp

#----------------------------------------

def MensagemDoPacote(): 
	while(True):
		print("\nInsira a mensagem do pacote:")
		msg_do_pacote = input()
		flag = len(msg_do_pacote)
		print ("\nqtd de caracteres: " + str(flag))
		if flag <= 30:
			break
		else:
			print("\nMensagem maior que 30 caracteres.")
	return str(msg_do_pacote)

#----------------------------------------

def base64_encode(sample_string):

    sample_string_bytes = sample_string.encode("ascii")
    
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    
    #print(f"Encoded string: {base64_string}")
    return base64_string

#----------------------------------------

def base64_decode(base64_string):

    base64_bytes = base64_string.encode("ascii")
    
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    
    #print(f"Decoded string: {sample_string}")
    return sample_string

#----------------------------------------

msg_do_pacote = MensagemDoPacote()



msgFromClient       = (b5 + ping + str(timestamp)[0:5] + msg_do_pacote)

base64_string = base64_encode(msgFromClient)

bytesToSend         = str.encode(msgFromClient + "," + base64_string)

print("\nmsgFromClient: " + msgFromClient + "\n")
serverAddressPort   = ("127.0.0.1", 20212)

bufferSize          = 1024
rtt					= []
n 					= 1
# Create a UDP socket at client side

UDP_Client_Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDP_Client_Socket.settimeout(3)

while n < 10:
	try: 
		start_time = round(time.time(), 1)
		# Send to server using created UDP socket
		UDP_Client_Socket.sendto(bytesToSend, serverAddressPort)
		transmitted = n+1
		# Response received from Server
		msgFromServer = UDP_Client_Socket.recvfrom(bufferSize)

		end_time = round(time.time(), 1)
		received = n+1

		message = msgFromServer[0]
		pos = msgFromServer[0].decode().find(",")
		address = msgFromServer[1]



		msg = "Message from Server {}".format(message.decode()[0:pos])

		msg_received = message.decode()[0:pos]
		base64_string = message.decode()[pos+1:]
		texto_decodificado = base64_decode(base64_string)
		print("texto_decodificado: " + texto_decodificado + "\n")

		if texto_decodificado == msg_received:

			RTT = round(end_time - start_time, 1) * 1000
			rtt.append(RTT)
			
			print(msg)
			print("rtt(IPV4): " + str(RTT) + "ms")
		else:
			print("mensgem recebida está inconsistente ( erro no tipo ou na Sequencia)")
			rtt.append(0)
			received = n-1
			
	except socket.timeout:
		rtt.append(0)
		print("conexão perdida")

	n = n + 1

loss = transmitted - received

min = str(min(rtt))
max = str(max(rtt))
avg = str(statistics.mean(rtt))
mdev = str(statistics.pstdev(rtt))

print("\n #### retults #### \n")

print("packets transmitted: " + str(transmitted) + "\n")
print("packets received: " + str(received) + "\n")
print("packets loss: " + str(loss) + "\n")

print("rtt min: " + min + "ms\n")
print("rtt avg: " + avg + "ms\n")
print("rtt max: " + max + "ms\n")
print("rtt mdev: " + mdev + "ms\n")

print("total time: " + str(round(end_time - timestamp, 1) * 1000) + "ms")