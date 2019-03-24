# -*- coding:utf-8 -*-
from __future__ import print_function
import socket ,json
from contextlib import closing
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

def mysocket(addr, port, thread):
    bufsize = 4096
    data = '<thread thread="{0}" version="20061206" res_from="-1"/>\0'.format(thread)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
        print(sock.connect_ex((addr, int(port))))
        sent = sock.send(data.encode('utf-8'))
        while True:
            print(sock.recv(bufsize).decode())
    return

def mypost(url, data):
    data = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req) as res:
        return res.read().decode("utf-8")

    return 0

if __name__ == '__main__':
    id_, pass_ = '' 
    with open('myconf.json', 'r') as f:
        j = json.loads(f.read())
        id_ = j['id']
        pass_ = j['pass'] 
    data = {"mail":id_, "password":pass_}
    login = mypost("https://secure.nicovideo.jp/secure/login?site=nicolive_antenna", data)
    root = BeautifulSoup(login, 'xml')

    ticket = root.ticket.string
    data = {'ticket':ticket}
    auth = mypost('http://live.nicovideo.jp/api/getalertstatus', data)
    root = BeautifulSoup(auth, 'xml')
    addr = root.getalertstatus.ms.addr.string
    port = root.getalertstatus.ms.port.string
    thread = root.getalertstatus.ms.thread.string
    # print(root.getalertstatus.ms.addr.string)
    mysocket(addr, port, thread)
