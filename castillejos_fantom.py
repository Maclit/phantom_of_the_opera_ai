# -*- coding: utf-8 -*-


import json
import random
import socket

import castillejos_src.protocol as protocol

host = "localhost"
port = 12000
# HEADERSIZE = 10



class Player():

    def __init__(self):

        self.end = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._decisions = {}

    def connect(self):
        self.socket.connect((host, port))

    def reset(self):
        self.socket.close()

    def answer(self, question):
        
        # work
        data = question["data"]
        
        response_index = random.randint(0, len(data)-1)

        return response_index
            
            

    def handle_json(self, data):
        data = json.loads(data)
        response = self.answer(data)
        # send back to server
        bytes_data = json.dumps(response).encode("utf-8")
        protocol.send_json(self.socket, bytes_data)

    def run(self):

        self.connect()

        while self.end is not True:
            received_message = protocol.receive_json(self.socket)
            if received_message:
                self.handle_json(received_message)
            else:
                print("no message, finished learning")
                self.end = True


p = Player()

p.run()
