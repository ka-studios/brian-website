from tkinter import Tk, Canvas
from cryptography.fernet import Fernet
import json as js
import http.client as client

class Connection:
    def __init__(self, server):
        self.server = server
        self.connection = client.HTTPSConnection(self.server)
    def send(self, json, method, server, headers={'Content-type': 'application/json'}):
        self.connection.request(method, server, json, headers)
        return self.connection.getresponse().read().decode()

class Main:
    def __init__(self):
        self.connection = Connection("0.0.0.0")
        self.key = Fernet.generate_key()
        self.password = None
        self.purchaseDataAmount = 0 # data to allocate in GB
        #self.BuyMemoryButton = Button(window, text="Purchase Memory", command=purchaseData())
        #self.setPasswordButton = Button(window, text="Set Password", command=setPassword())
        #self.BuyMemoryButton.place(anchor='nw')
        #self.setPasswordButton.place(x=135, y=0)

def main(self):
    pass

def generateJSON(self, data, key, password, encryption):
    with open("send.json", 'r') as json_file:
        json_data = json_file.read()
        json_data = js.loads(json_data)
        json_data['data']['data']               = data
        json_data['verification']['key']        = key
        json_data['verification']['password']   = password
        json_data['verification']['encryption'] = encryption
    return js.dumps(json_data)
def purchaseData(self):
        cost = self.purchaseDataAmount
        data = self.generateJSON(cost, None, self.password, None)
        self.connection.send(data, 'POST', "/buyMemory.html")

def setPassword(self):
    passTK = Tk()
    passTK.title("Set Password")
    PasswordWindow = Canvas(passTK, width=400, height=100)
    PasswordWindow.pack()
tk = Tk()
tk.title("App")
tk.wm_attributes('-topmost', 1)
tk.resizable(0, 0)
window = Canvas(tk, width=600, height=500)
window.pack()

print ("Ctrl-C to stop program after closing the window")

if __name__ == "__main__":
    m = Main()
while True:
        try:
            m
            tk.update()
            tk.update_idletasks()
        except KeyboardInterrupt:
            break
