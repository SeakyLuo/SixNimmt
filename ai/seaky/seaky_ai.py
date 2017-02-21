#!/usr/bin/env python
import sys
import random
import logging
import os

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
        self.rows=gameData['rows']
        pass

    def InfoMove(self, cardData):
        pass

    def InfoScore(self, scoreData):
        pass

    def InfoGameEnd(self, gameEndData):
        pass

    def CmdPickCard(self):
        self.rows.reverse()
        def find_row(card):
            idx=0
            if card<self.rows[0][-1]:
                return -1
            for i,row in enumerate(self.rows):
                if card<row[-1]:
                    idx=i
                    break
                elif i==3 and card>row[-1]:
                    idx=i
            return idx

        card_evaluation={}
        for card in self.cards:
            evaluation=0
            idx=find_row(card)
            if idx!=-1:
                if len(self.rows[idx])!=5:
                    evaluation+=1
            card_evaluation[card]=evaluation
        max_evaluation=max(card_evaluation.values())
        pick_card=random.choice([ card for card in card_evaluation if card_evaluation[card]==max_evaluation])
        self.cards.remove(pick_card)
        return pick_card       


    def CmdPickRow(self):
        ##pick the row that has lowest points
        row_num=0
        lowest_points=70
        for i,row in enumerate(self.rows):
            count_points=0
            for card in row:
                if card==55:
                    count_points+=7
                elif card%11==0:
                    count_points+=5
                elif card%10==0:
                    count_points+=3
                elif card%5==0:
                    count_points+=2
                else:
                    count_points+=1
            if count_points<lowest_points:
                count_points=lowest_points
                row_num=i
        return row_num

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