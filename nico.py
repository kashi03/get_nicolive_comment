#coding:utf-8
from mymod import *
from bs4 import BeautifulSoup as bs
from contextlib import closing
import socket, json

nico = ''
with open('myconf.json', 'r') as f:
    j = json.loads(f.read())
    id_ = j['id']
    pass_ = j['pass']    
    nico = Nico(id_, pass_)

ticket = nico.login()
ticket = bs(ticket, 'xml')
root = bs(nico.auth(ticket.ticket.string), 'xml')
addr = root.getalertstatus.ms.addr.string
port = root.getalertstatus.ms.port.string
thread = root.getalertstatus.ms.thread.string
nico.connect(addr, port, thread)
with closing(nico.socket):
    while True:
        nico.socket.recv(4096).decode()
