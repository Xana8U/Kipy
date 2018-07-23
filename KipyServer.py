import socketserver
import sqlite3
import time

conn = sqlite3.connect("Messages.db")
c = conn.cursor()

'''Handles connections and returns a data to clients'''
class TCPhandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        if str(self.data).strip("b''") == "ref":
            c.execute("SELECT * FROM messages ORDER BY ROWID DESC LIMIT 80")
            dbdata = str()
            for entry in c.fetchall()[::-1]:
                dbdata += entry[1].replace("\\xc3\\xb6", "ö").replace("\\xc3\\xa4", "ä") + "\n"
            print("{} > ".format(self.client_address), str(self.data).strip("b''"))
            self.request.sendall(bytes(dbdata, "utf-8"))

        else:
            c.execute("INSERT INTO messages VALUES ('{}', '{}')".format(time.strftime("%x %X", time.localtime()),
                                                                    str(self.data).strip("b''")))
            conn.commit()
            c.execute("SELECT * FROM messages ORDER BY ROWID DESC LIMIT 80")
            dbdata = str()
            for entry in c.fetchall()[::-1]:
                dbdata += entry[1].replace("\\xc3\\xb6", "ö").replace("\\xc3\\xa4", "ä") + "\n"
            print("{} > ".format(self.client_address), str(self.data).strip("b''"))
            self.request.sendall(bytes(dbdata, "utf-8"))


if __name__ == "__main__":
    host, port = "192.168.100.10", 5479

    with socketserver.TCPServer((host, port), TCPhandler) as server:
        server.serve_forever()

