import socket
import sys
import thread
import time


# Create the TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.100.5', 8888)
print >>sys.stderr, 'starting up on port ', server_address
sock.bind(server_address)

#Listen for incoming connections
sock.listen(5)

while True:
    # Wait for a connection
    print >>sys.stderr, 'Waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

def connection_thread(connection,client_address):
    
# # Define a function for the thread
# def print_time( threadName, delay):
#    count = 0
#    while count < 5:
#       time.sleep(delay)
#       count += 1
#       print "%s: %s" % ( threadName, time.ctime(time.time()) )


# # Create two threads as follows
# try:
#     print "%s" % (time.ctime(time.time()) )
#     thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#     thread.start_new_thread( print_time, ("Thread-2", 4, ) )
# except:
#    print "Error: unable to start thread"

# while 1:
#    pass