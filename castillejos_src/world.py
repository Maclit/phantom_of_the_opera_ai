# -*- coding: utf-8 -*-
"""
Class to simulate the environnement and build the game tree
"""

MAP_SIZE = 10
MAP_PATHS = [{1, 4}, {0, 2}, {1, 3}, {2, 7}, {0, 5, 8},
            {4, 6}, {5, 7}, {3, 6, 9}, {4, 9}, {7, 8}]

MAP_PINK_PATHS = [{1, 4}, {0, 2, 5, 7}, {1, 3, 6}, {2, 7}, {0, 5, 8, 9},
                 {4, 6, 1, 8}, {5, 7, 2, 9}, {3, 6, 9, 1}, {4, 9, 5},
                 {7, 8, 4, 6}]

BEFORE_POWER = {"purple", "brown"}
AFTER_POWER = {"black", "white", "red", "blue", "grey"}

class World():
    
    def __init__(self):
        self._game_state = None

    def set_env(self, game_state):
        self._game_state = game_state
          
    def get_adjacent_positions(self, position, color, blocked):
        if color == 'pink':
            active_passages = MAP_PINK_PATHS
        else:
            active_passages = MAP_PATHS
        return [room for room in active_passages[position] if set([room, position]) != set(blocked)]

    def get_positions(self, card, game_state):
        characters_in_room = [q for q in game_state['character_cards'] if q['position'] == card['position']]
        number_of_characters_in_room = len(characters_in_room)
        available_rooms = []
        available_rooms.append(self.get_adjacent_positions(card['position'], card['color'], game_state['blocked']))
        for step in range(1, number_of_characters_in_room):
            next_rooms = []
            for room in available_rooms[step - 1]:
                next_rooms += self.get_adjacent_positions(room, card['color'], game_state['blocked'])
            available_rooms.append(next_rooms)
        temp = []
        for sublist in available_rooms:
            for room in sublist:
                temp.append(room)
        temp = set(temp)
        available_positions = list(temp)
        if card['position'] in available_positions:
            available_positions.remove(card['position'])      
        return available_positions

    
    def get_possible_actions(self, game_state, fantom=False):
        active_cards = game_state['active character_cards']
        actions = []
        
        # Get all possible colors        
        for card in active_cards:
            
            # Character node
            color = card['color']
            
            # Get all possible positions
            positions = self.get_positions(card, game_state)
            for position in positions:
                
                decision = {}
                decision['color'] = color
                decision['position'] = position
                decision['value'] = 0 # TODO
        
        return actions
