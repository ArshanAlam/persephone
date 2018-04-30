#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socket

cache = dict()
PORT_KEY = "port number"
BLOCK_SIZE = 1024
ENCODING_TYPE = "utf-8"

class Peer:
  def __init__(self, host, port):
    self.host = str(host)
    self.port = int(port)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect((self.host, self.port))
    print("Peer at", self.host, self.port)

  def get_host(self):
    return self.host

  def get_port(self):
    return self.port

  def get(self, key):
    self.socket.send(str(key).encode(ENCODING_TYPE))
    return self.socket.recv(BLOCK_SIZE).decode(ENCODING_TYPE)


class Persephone:
  def __init__(self, peer_list):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind(("", 0))
    self.host = self.socket.getsockname()[0]
    self.port = self.socket.getsockname()[1]
    self.peers = peer_list
    print(self.host, self.port)
    
  def accept(self):
    for p in self.peers:
      print(p.get(PORT_KEY))

    self.socket.listen()
    while True:
      conn, addr = self.socket.accept()
      print("Connection from:", str(addr))
      req = conn.recv(BLOCK_SIZE).decode(ENCODING_TYPE)
      if req == PORT_KEY:
        conn.send(str(self.port).encode(ENCODING_TYPE))


def get_peers(peer_address_list):
  peers = list()
  for p in peer_address_list:
    raw = p.split(":")
    host = raw[0]
    port = raw[1]
    peers.append(Peer(host, port))
  return peers


def main():
  p = Persephone(get_peers(sys.argv[1:]))
  p.accept()
  

if __name__ == "__main__":
  main()
