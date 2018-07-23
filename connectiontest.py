import socket

host, port = "192.168.100.10", 5479
def sendnreceive():
    while True:
        buildmsgdata = input("Message:")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(bytes(buildmsgdata + "\n", "UTF-8"))

            received = str(sock.recv(1024), "UTF-8")

            print("Sent {}".format(buildmsgdata))
            print("Received {}".format(received))
            sock.close()

sendnreceive()
