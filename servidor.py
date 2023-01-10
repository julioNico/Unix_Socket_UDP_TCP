#!/usr/bin/env python3
import socket
import time
import base64

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

localIP     = "127.0.0.1"

localPort   = 20212

bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
 

print("UDP server up and listening")


# Listen for incoming datagrams

while(True):

	bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
	#time.sleep(2)
	message = bytesAddressPair[0]
	pos = message.decode().find(",")
	address = bytesAddressPair[1]

	clientMsg = "Message from Client:{}".format(message.decode()[0:pos])
	clientIP  = "Client IP Address:{}".format(address)

	print(clientMsg)

	msg_received = message.decode()[0:pos]
	base64_string = message.decode()[pos+1:]
	texto_decodificado = base64_decode(base64_string)
	print("texto_decodificado: " + texto_decodificado + "\n")

	if texto_decodificado == msg_received:

		b5 = str(message.decode()[0:5])
		#print(b5)
		ping = '1'
		#print(ping)
		start_time = message.decode()[6:10]
		#print("start_time: " + start_time)
		
		msg = message.decode()[11:pos]
		#print("msg: " + msg)
		print(clientIP)

		# Sending a reply to client
		response = ("PONG: " + b5 + ping + str(start_time) + msg.upper())

		print("bytesToSend: " + str(response))

		base64_string = base64_encode(response)

		bytesToSend         = str.encode(response + "," + base64_string)

		UDPServerSocket.sendto(bytesToSend, address)
	
	else:
		print("mensgem recebida está inconsistente ( erro no tipo ou na Sequencia)")