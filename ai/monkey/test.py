import random
import sys
import os
import logging
from common import *
import argparse


class Player(object):
    def __init__(self, max_card=104, starting_cards=10, rows=4, takes=6):
        self.max_card = max_card
        self.starting_cards = starting_cards
        self.rows = rows
        self.takes = takes
        self.cards = []
        self.tricks = []


class ShortestRowPlayer(Player):
    def make_choice(self, board):
        min = -1
        minc = 0
        for c in self.cards:
            d = -1
            l = 100000
            for row in board:
                if row[-1] < c and (c - row[-1] < d or d < 0):
                    d = c - row[-1]
                    l = len(row)
            if l < min or min < 0:
                min = l
                minc = c
        return minc



class AI:
    def __init__(self):
        self.name = ''
        self.cards = []
        self.logFileName = os.path.join(os.path.dirname(__file__), 'log')
        logging.basicConfig(filename = self.logFileName, level=logging.INFO)
    def InfoSetup(self, setupData):
        pass
    def InfoNewGame(self, newGamedata):
        self.cards = newGamedata[:]
        pass
    def InfoGame(self, gameData):
        pass
    def InfoMove(self, cardData):
        pass
    def InfoScore(self, scoreData):
        pass
    def InfoGameEnd(self, gameEndData):
        pass
    def CmdPickCard(self, board):
        choice = None
        while choice not in self.cards:
            choice = self.make_choice(board)
        self.cards.remove(choice)
        return choice
    def make_choice(self, board):
        min = -1
        minc = 0
        for c in self.cards:
            d = -1
            for row in board:
                if row[-1] < c and (c - row[-1] < d or d < 0):
                    d = c - row[-1]
            if d < min or min < 0:
                min = d
                minc = c
        return minc

    def ask_which(self, board, card):
        return random.randint(0, len(board) - 1)

        #random.shuffle(self.cards)
        #return self.cards.pop()
    def CmdPickRow(self):
            class OpportunisticPlayer(Player):
        def __init__(self, max_card=6, starting_cards=104, rows=4, takes=6):
            self.inner = which(max_card=max_card, starting_cards=starting_cards, rows=rows, takes=takes)
            super(OpportunisticPlayer, self).__init__(max_card=max_card, starting_cards=starting_cards, rows=rows, takes=takes)
        def make_choice(self, board):
            for b in board:
                if sum(map(get_value, b)) <= 1:
                    c = min(self.cards)
                    bmin = min(map(lambda r: r[-1], board))
                    if c < bmin:
                        return c
            self.inner.cards = self.cards
            self.inner.tricks = self.tricks
            return self.inner.make_choice(board)
        def ask_which(self, board, card):
            self.inner.cards = self.cards
            self.inner.tricks = self.tricks
            return self.inner.ask_which(board, card)
    return OpportunisticPlayer

        #return random.randint(0,3)
    def ProcessInfo(self):
        line = sys.stdin.readline()
        if line == '':
            logging.info('No Input')
            sys.exit(1)
        data = line.strip().split('|')
        logging.info("Get Info " + str(line))
        if data[0] == 'INFO':
            if data[1] == 'SETUP':
                self.InfoSetup(eval(data[2]))
            elif data[1] == 'NEWGAME':
                self.InfoNewGame(eval(data[2]))
            elif data[1] == 'GAME':
                self.InfoGame(eval(data[2]))
            elif data[1] == 'MOVE':
                self.InfoMove(eval(data[2]))
            elif data[1] == 'SCORE':
                self.InfoScore(eval(data[2]))
            elif data[1] == 'GAMEEND':
                self.InfoGameEnd(eval(data[2]))
                return False
        elif data[0] == 'CMD':
            if data[1] == 'PICKCARD':
                self.Send(self.CmdPickCard())
            elif data[1] == 'PICKROW':
                self.Send(self.CmdPickRow())
        return True
    def Send(self, data):
        logging.info('Send Info ' + str(data))
        print str(data)
        sys.stdout.flush()
    def Start(self):
        while True:
            if not self.ProcessInfo():
                break

if __name__ == '__main__':
    ai = AI()
    ai.Start()
