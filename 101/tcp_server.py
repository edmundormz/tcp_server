import socket
import sys

# Create the TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.100.5', 8888)
print >>sys.stderr, 'starting up on port ', server_address
sock.bind(server_address)

#Listen for incoming connections
sock.listen(1)

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


while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        connection_function(connection, client_address)
    finally:
        print "Server closed"