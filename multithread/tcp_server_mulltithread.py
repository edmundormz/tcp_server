import socket
import sys
import thread
import time
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

ip = get_ip_address('eth0')

def connection_function(connection, client_address):
    print >>sys.stderr, 'connection from', client_address
    while True:
            data = connection.recv(16)
            print >>sys.stderr, 'received ', data
            if data:
                print >>sys.stderr, 'sendig data back to the client'
                connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break        
    connection.close()

# Create the TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('192.168.100.8', 8888)
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
        print "Server closed"
