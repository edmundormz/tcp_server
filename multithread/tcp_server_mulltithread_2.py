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

# Receive data from new a connection and returns data to client
def connection_function(connection, client_address):
    print >>sys.stderr, 'connection from', client_address
    frame = '02,17,19'
    try:
        connection.sendall(frame)
        print 'Data sent: ' + frame
    except:
        print 'Could not send data to client' + str(client_address)
    while True:
        received = connection.recv(64)
        if received:
            print 'Data received: ' + received
            break
    print 'Closing connection from ' + str(client_address)
    connection.close()

# Create the TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
