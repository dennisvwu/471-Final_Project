#=====================================================================
# Name: Dennis Wu
# CPSC 471 - Assignment 3 [Final Project]
# File name: cli.py
# Summary: this file implements a simplified FTP client application
#=====================================================================
import socket

def Main():
	host = '127.0.0.1'
	port = 5000

	# create TCP socket
	s = socket.socket()
	s.connect((host, port))

	filename = raw_imput("Filename? -> ")

	# check for quit
	if filename != 'q':
		s.send(filename)
		data = s.recv(1024)

		# check first 6 chars in data
		if data[:6] == 'EXISTS':
			filesize = long(data[6:])

			message = raw_imput("File Exists, " + str(filesize) + "Bytes, download? Y/N? -> ")

			if message == 'Y':
				s.send('OK')
				# open in write binary mode
				f = open(filename, 'wb')
				data = s.recv(1024)
				totalRecv = len(data)
				f.write(data)
				# if more than 1024 bytes of data
				while totalRecv < filesize:
					data = s.recv(1024)
					totalRecv += len(data)
					# write data
					f.write(data)
					# two floating decimal point
					print "{0:.2f}".format((totalRecv/float(filesize)) * 100) + "% Done"

				print "Download Complete!"

		else:
			print "File does not Exists!"

	# close socket
	s.close()

if __name__ == '__main__':
	Main()













import os
import sys


# Command line checks
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <FILE NAME>"

# Server address
serverAddr = "localhost"

# Server port
serverPort = 1234

# The name of the file
fileName = sys.argv[1]

# Open the file
fileObj = open(fileName, "r")

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

# The number of bytes sent
numSent = 0

# The file data
fileData = None

# Keep sending until all is sent
while True:

	# Read 65536 bytes of data
	fileData = fileObj.read(65536)

	# Make sure we did not hit EOF
	if fileData:

		# Get the size of the data read
		# and convert it to string
		dataSizeStr = str(len(fileData))

		# Prepend 0's to the size string
		# until the size is 10 bytes
		while len(dataSizeStr) < 10:
			dataSizeStr = "0" + dataSizeStr

		# Prepend the size of the data to the
		# file data.
		fileData = dataSizeStr + fileData

		# The number of bytes sent
		numSent = 0

		# Send the data!
		while len(fileData) > numSent:
			numSent += connSock.send(fileData[numSent:])

	# The file has been read. We are done
	else:
		break


print "Sent ", numSent, " bytes."

# Close the socket and the file
connSock.close()
fileObj.close()
