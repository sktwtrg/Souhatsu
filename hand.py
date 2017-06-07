from block import Block
from deck import Deck
from souhatsu_enums import Hai
from player import Player

class Hand:

    def __init__(self, deck, initnum = 8, test = None):

        self.hand = list()
        self.contents = [0]*10
        self.head = Block([])
        self.mentsu = []
        self.tsumohai = Hai.valueAt(-1)
        self.ronhai = Hai.valueAt(-1)
        self.agarihai = Hai.valueAt(-1)
        self.hansu = 0
        self.fu = 0
        self.ten = 0
        self.mensen = True
        self.furo = []
        self.yaku = []
        self.machi_type = None
        self.machi_type_candidate = []

        if test != None:
            for i in test:
                self.test_tsumo(i)
            return

        for i in range(initnum):
            self.tsumo(deck)
        return

    def hora_process(self, player):
        self.show_hand()
        print(player.name + " hora!")
        print("役:",end="")
        print(self.yaku)
        print("面子:",end="")
        print(self.mentsu)
        print("頭:",end="")
        print(self.head)
        print("副露:",end="")
        print(self.furo)
        print("待ち形:",end="")
        print(self.machi_type_candidate)
        print("飜数",end="")
        print(self.hansu)
        print("符",end="")
        print(self.fu)
        print("点数",end="")
        print(self.ten)

    def show_hand(self):
        contents = list(self.contents)[:]
        hand = list(self.hand)[:]

        if self.tsumohai.number != -1: contents[self.tsumohai.number] -= 1

        for i in range(10):
            for j in range(contents[i]):
                print(repr(i) + ",", end="")
        if self.tsumohai.number != -1:
            print("T" + str(self.tsumohai.number), end="")
        if self.furo != []:
            print("副露:",self.furo)
        print()

        if self.tsumohai.number != -1:
            hand.remove(self.tsumohai)
        for item in hand:
            print(item.hainame, end=',')
        if self.tsumohai.number != -1:
            print("T" + self.tsumohai.hainame)
        else:
            print()
        
        print(contents)

    def trash(self, hai):
        self.contents[hai.number] -= 1
        self.hand.remove(hai)

    def tsumo(self, deck):
        self.tsumohai = deck.draw()
        self.hand.append(self.tsumohai)
        self.contents[self.tsumohai.number] += 1
        return self.tsumohai

    def test_tsumo(self, number):
        self.tsumohai = Hai.valueAt(number)
        self.hand.append(self.tsumohai)
        self.contents[self.tsumohai.number] += 1
        return self.tsumohai

    def pon(self, hai):
        self.hand.append(hai)
        num = hai.number
        self.contents[num] -= 2
        block_hais = []
        for i in range(3):
            self.hand.remove(hai)
            block_hais.append(hai)
        block = block(block_hais, block_type = "minko")
        self.mensen = False
        self.furo.append(block)

    # ツモはせずターンを飛ばして普通のツモをする（ツモはFieldで行う）
    def daiminkan(self, hai, deck):
        self.hand.append(hai)
        num = hai.number
        self.contents[num] -= 3
        block_hais = []
        for i in range(4):
            self.hand.remove(hai)
            block_hais.append(hai)
        block = block(block_hais, block_type = "daiminkan")
        self.furo.append(block)
        self.mensen = False
        self.show_hand()

    def ankan(self, hai, deck):
        num = hai.number
        self.contents[num] -= 4
        block_hais = []
        block_entities = []
        for i in range(4):
            self.hand.remove(hai)
            block_hais.append(hai)
        self.tsumo(deck)
        block = block(block_hais, block_type = "ankan")
        self.furo.append(block)
        self.show_hand()

    #ron後 hora処理
    def ron(self, hai):
        self.ronhai = hai
        self.tsumohai = Hai.valueAt(-1)
        self.contents[hai.number] += 1
        self.hand.append(hai)
        self.agarihai = hai

if __name__ == "__main__":
    deck = Deck()
    player = Player('aaa')
    hand = Hand(deck, player, test=[0,0,0,1,1,1,1,2])
    hand.show_hand()
