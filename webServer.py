# import socket module
from socket import *
# In order to terminate the program
import sys

# Request format
# GET /somedir/page.html HTTP/1.1
# Host: www.someschool.edu
# Connection: close
# User-agent: Mozilla/5.0
# Accept-language: fr

# Response format
# HTTP/1.1 200 OK
# Connection: close
# Date: Tue, 18 Aug 2015 15:44:04 GMT
# Server: Apache/2.2.3 (CentOS)
# Last-Modified: Tue, 18 Aug 2015 15:11:03 GMT
# Content-Length: 6821
# Content-Type: text/html
# (data data data data data ...)


NOT_FOUND_RESPONSE = "HTTP/1.1 404 Not Found\r\n"

# TODO must be encoded back to bytes
OK_RESPONSE_HEADER = "HTTP/1.1 200 OK\r\n"
HTML_CONTENT_TYPE = "Content-Type: text/html; charset=UTF-8\r\n"

def webServer(port=13331):
  serverSocket = socket(AF_INET, SOCK_STREAM)

  #Prepare a server socket
  serverSocket.bind(("127.0.0.1", port))

  serverSocket.listen()

  while True:
    #Establish the connection

    print(f"Ready to serve... on: http://localhost:{port}")
    connectionSocket, addr = serverSocket.accept()

    try:
      # read in request
      message = connectionSocket.recv(1024)

      # split request lines
      lines = message.decode("UTF-8").split("\r\n")
      (method, URL, version) = lines[0].split()

      # log request
      print(f"{method}\t{URL}\t{version}")

      # start building request
      response = ""

      # last header line should be skipped according to spec
      # TODO do stuff with these? could easily be turned into a map if
      # we wanted to handle these
      header_lines = lines[1:-2]

      data = None
      try:
        with open(f"./{URL}", "r") as f:
          data = f.read()
        print("file found")
        response += OK_RESPONSE_HEADER
        response += HTML_CONTENT_TYPE
        response += "\r\n"
        response += data
        response += "\r\n"
      except FileNotFoundError as e:
        print("file not found")
        response = NOT_FOUND_RESPONSE

      # remember to byte-ify response
      connectionSocket.sendall(bytes(response, "UTF-8"))
      # close connecting socket
      connectionSocket.close()

    # handle all other exceptions loudly
    except Exception as e:
      raise(e)

  # Commenting out the below (some use it for local testing). It is not required for Gradescope, and some students have moved it erroneously in the While loop.
  # DO NOT PLACE ANYWHERE ELSE AND DO NOT UNCOMMENT WHEN SUBMITTING, YOU ARE GONNA HAVE A BAD TIME
  #serverSocket.close()
  #sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
  webServer(13331)
