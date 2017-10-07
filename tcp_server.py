import socket
import sys

# Create the TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('172.16.15.183', 8888)
print >>sys.stderr, ´'starting up on % port %' % server_address
sock.bind(server_address)

#Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chnks and retransmit it
        while True:
            data = connection.recv(16) # 32?
            print >>sys.stderr, 'received "%"' % data
            if data:
                print >>sys.stderr, 'sendig data back to the client'
                connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
    finally:
        connection.close()