import socket
import sys
import thread
import time
import fcntl
import struct

# Gets IP address from host device (server)
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

# interface to discover ip address of
ip = get_ip_address('eth0')

def checksum(frame):
    a,b,c = frame.split(',')
    a = int(a)
    b = int(b)
    c = int(c)
    checksum_trama = a ^ b ^ c 
    return frame+',' + str(checksum_trama)

def validate(frame):
    if frame.find('255') >= 0:
        print 'Error en la trama enviada' + ' ' +frame
    else:
        print 'Trama enviada exitosamente' + ' ' +frame

# Receive data from new a connection and returns data to client
def connection_function(connection, client_address):
    print >>sys.stderr, 'connection from', client_address
    config_output = '02,17,00'
    turn_on = '00,17,01'
    turn_off = '00,17,00'
    config_input = '02,02,01'
    read_state = '01,02,00'
    configs = [config_output,turn_on,config_input,read_state]
    # to_send = checksum(frame)
    for instruction in configs:
        to_send = checksum(instruction)
        try:        
            connection.sendall(to_send)
            print 'Data sent: ' + to_send
        except:
            print 'Could not send data to client' + str(client_address)
        received = connection.recv(64)
        if received:
            validate(received)
            continue
        else:
            print 'No response'
        time.sleep(5)
        print instruction

    # try:
    #     connection.sendall(connection_function(config))
    #     print 'Data sent: ' + to_send
    # except:
    #     print 'Could not send data to client' + str(client_address)
    # while True:
    #     received = connection.recv(64)
    #     if received:
    #         print 'Data received: ' + received
    #         break
    # print 'Closing connection from ' + str(client_address)
    # connection.close()

# Create the TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = (ip, 8888)
print >>sys.stderr, 'starting up on port ', server_address
sock.bind(server_address)
#Listen for incoming connections
sock.listen(5)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        thread.start_new_thread(connection_function,(connection, client_address))
    except:
        print "Error: unable to start new thread"
    finally:
        print "Connection closed"
