from kivy.config import Config
Config.set("graphics", "resizable", False)
Config.set("kivy", "window_icon", "kipy.ico")
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from functools import partial
import socket


host = ""
# interface controller
class ScreenManagement(ScreenManager):
    pass


class LoginScreen(Screen):
    Window.size = 320, 160
    # Create invisible data for ip and user to Screenmanagement for username and ip
    def logininfo(self):
        self.username = self.ids.username.text
        self.ipaddr = self.ids.ipAddr.text
        ScreenManagement.username = self.username
        ScreenManagement.ipaddr = self.ipaddr
        Window.size = 600, 400
        Interface.sendnreceive(self, self.username, self.ipaddr, "conn")

    pass


class Interface(Screen):
    def sendnreceive(self, username, ipaddr, source, *largs):
        global host
        host, port = ipaddr, 5479
        if source == "msg":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # connect to given IP
                sock.connect((host, port))
                # Send click, send data in msg input field
                sock.sendall(bytes("{} : {}".format(username, self.ids.msgInput.text) + "\n", "utf-8"))
                # receive data from server
                received = str(sock.recv(10000), "utf-8")

                # Add message to message Feed
                self.ids.messages.text = ""
                self.ids.messages.text += "{} \n".format(received)
                self.ids.msgInput.text = ""  # Reset the message line
                sock.close()
                Clock.schedule_interval(partial(self.sendnreceive, username, ipaddr, "ref"), 0.5)

        elif source == "conn":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
                sock.sendall(bytes("{} Connected!".format(username) + "\n", "utf-8"))
                sock.close()

        elif source == "ref":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, 5479))
                sock.sendall(bytes("ref", "utf-8"))
                received = str(sock.recv(10000), "utf-8")
                sock.close()
            self.ids.messages.text = ""
            self.ids.messages.text += "{} \n".format(received)

    #def refresh(self, dt):
    #    global host
    #    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #        sock.connect((host, 5479))
    #        sock.sendall(bytes("refresh request", "utf-8"))
    #        received = str(sock.recv(10000), "utf-8")
    #        sock.close()
    #    self.ids.messages.text = ""
    #    self.ids.messages.text += "{} \n".format(received)

    pass

startapp = Builder.load_file("Kipy.kv")


class Kipy(App):
    def build(self):
        return startapp

if __name__ == '__main__':
    Kipy().run()
