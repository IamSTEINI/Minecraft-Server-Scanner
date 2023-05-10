import struct
import socket
import base64
import json
import sys



vfilter = ""
class Server:
    def __init__(self, data):
        self.description = data.get('description')
        if isinstance(self.description, dict):
            self.description = self.description['text']

        self.icon = base64.b64decode(data.get('favicon', '')[22:])
        self.players = Players(data['players'])
        self.version = data['version']['name']
        self.protocol = data['version']['protocol']

    @staticmethod
    def getVersion(data):
        return data['version']['name']
    @staticmethod
    def getDesc(data):
        return data.get('description')['text']
    @staticmethod
    def getIcon(data):
        return base64.b64decode(data.get('favicon', '')[22:])
    @staticmethod
    def getProt(data):
        return data['version']['protocol']
    @staticmethod
    def getPlayers(data):
        return Players(data['players'])

    def __str__(self):
        return 'Server(description={!r}, icon={!r}, version={!r}, '\
                'protocol={!r}, players={})'.format(
            self.description, bool(self.icon), self.version,
            self.protocol, self.players
        )

class Players(list):
    def __init__(self, data):
        super().__init__(Player(x) for x in data.get('sample', []))
        self.max = data['max']
        self.online = data['online']

    def __str__(self):
        return '[{}, online={}, max={}]'.format(
            ', '.join(str(x) for x in self), self.online, self.max
        )

class Player:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

    def __str__(self):
        return self.name


def ping(ip, port=25565):
    def read_var_int():
        i = 0
        j = 0
        while True:
            k = sock.recv(1)
            if not k:
                return 0
            k = k[0]
            i |= (k & 0x7f) << (j * 7)
            j += 1
            if j > 5:
                raise ValueError('var_int too big')
            if not (k & 0x80):
                return i

    sock = socket.socket()
    sock.connect((ip, port))
    try:
        host = ip.encode('utf-8')
        data = b''  
        data += b'\x00' 
        data += b'\x04'  
        data += struct.pack('>b', len(host)) + host
        data += struct.pack('>H', port)
        data += b'\x01'  
        data = struct.pack('>b', len(data)) + data
        sock.sendall(data + b'\x01\x00')  
        length = read_var_int()  
        if length < 10:
            if length < 0:
                raise ValueError('negative length read')
            else:
                raise ValueError('invalid response %s' % sock.read(length))

        sock.recv(1) 
        length = read_var_int()  
        data = b''
        while len(data) != length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                raise ValueError('connection abborted')

            data += chunk
        
        dtolad = json.loads(data)
        serverstring = color.blue+str(Server.getDesc(dtolad)) +color.green+ " | VER: "+color.blue+str(Server.getVersion(dtolad))+color.green+" | PLAYERS: "+color.blue+str(Server.getPlayers(dtolad))+" | PROTOCOL: "+color.blue+str(Server.getProt(dtolad))

        if(vfilter != ""):
            if(Server.getVersion(dtolad) == vfilter):
                return serverstring
            else:
                return "NONE"
        else:
            return serverstring
    finally:
        sock.close()

import colorama
import os
def setTitle(name):
    os.system("title "+name)

class color:
    white = colorama.Fore.WHITE
    green = colorama.Fore.LIGHTGREEN_EX
    red = colorama.Fore.LIGHTRED_EX
    magenta = colorama.Fore.LIGHTMAGENTA_EX
    blue = colorama.Fore.LIGHTBLUE_EX
        
def checkip(ip):
    try:
        res = ping(ip)
        if(res != "NONE"):
            print(color.blue+ip+color.white+" | "+color.green+str(res))
    except Exception:
        pass


import threading

def scan_ips(ips):
    for ip in ips:
        checkip(ip)
        setTitle(ip)


ips = []

os.system("cls")
print(colorama.Fore.LIGHTRED_EX+"""\nMADE BY STEIN\n\nSTEIN'S SERVERCHECKER\n""")

    
    
ipin = input(colorama.Fore.LIGHTGREEN_EX+"--------------\n| ENTER YOUR\n| IP> "+colorama.Fore.LIGHTMAGENTA_EX).split(":")[0]
prefix = colorama.Fore.LIGHTMAGENTA_EX+"["+colorama.Fore.LIGHTGREEN_EX+"#"+colorama.Fore.LIGHTMAGENTA_EX+"]"+colorama.Fore.WHITE
node = '.'.join(ipin.split('.')[:-1])
print(prefix+" SELECTED> "+color.red+ipin+color.white+" | NODE: "+color.blue+node)


vfilter = input(colorama.Fore.LIGHTGREEN_EX+"| Version (blank = any) > "+colorama.Fore.WHITE)

print(prefix+" STARTING SCAN...")
print(prefix+" Fetch node...")
for ipstr in range(1, 256):
    newnode = node+"."+str(ipstr)
    ips.append(newnode)

print(prefix+" Starting threads")
print(prefix+" Scanning")
chunk_size = len(ips) // 10
ip_chunks = [ips[i:i+chunk_size] for i in range(0, len(ips), chunk_size)]
threads = []
for i in range(10):
    t = threading.Thread(target=scan_ips, args=(ip_chunks[i],))
    threads.append(t)
    t.start()
for t in threads:
    t.join()

print(prefix+" SCAN COMPLETED!")
os.system("PAUSE")