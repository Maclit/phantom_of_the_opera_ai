# -*- coding: utf-8 -*-

from castillejos_src.world import World

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
        
        world = World()
        world.set_env(question["game state"])
        
        # work
        data = question["data"]
        
        response_index = 0
        if question['question type'] == 'select character':
            actions = world.get_possible_actions(question['game state'], fantom=True)

            L = len(actions)
            self._decisions = actions[0]
            for l in range(1, L):
                if self._decisions['value'] < actions[l]['value']:
                    self._decisions = actions[l]

            L = len(data)
            for l in range(0, L):
                if data[l]['color'] == self._decisions['color']:
                    response_index = l
                    break
                       
        elif question['question type'] == 'select position':
            L = len(data)
            for l in range(0, L):
                if data[l] == self._decisions['position']:
                    response_index = l
                    break
        elif question['question type'] == 'grey character power':
            response_index = self._decisions['grey character power']
        else:
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
