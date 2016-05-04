import random
from enum import Enum

class Hai(Enum):
    SU1 = (1, '一索')
    SU2 = (2, '一索')
    SU3 = (3, '一索')
    SU4 = (4, '一索')
    SU5 = (5, '一索')
    SU6 = (6, '一索')
    SU7 = (7, '一索')
    SU8 = (8, '一索')
    SU9 = (9, '一索')
    HATSU = (None, '發')

    @classmethod
    def valueAt(cls, num):
        for hai in cls:
            if hai.number == num:
                return hai
        return None

    @property
    def number(self):
        return self.value[0]

    @property
    def hainame(self):
        return self.value[1]

    @property
    def is_suhai(self):
        return self.number != None


class Hand():
    def __init__(self, deck):
        self.contents = [0]*10
        for i in range(6):
            a = deck.draw()
            self.contents[a] += 1
            # self.contents[deck.draw()] += 1
        self.head = int()
        self.mentsu = []
        self.tsumohai = -1

    def __len__(self):
        return self.contents.__len__()

    def __getitem__(self, key):
        return self.contents.__getitem__(key)

    def __setitem__(self, key, value):
        return self.contents.__setitem__(key, value)

    def __iter__(self):
        return self.contents.__iter__()

    def __contains__(self, item):
        return self.contents.__contains__(item)

    def append(self, item):
        return self.contents.append(item)

    def mentsu_check(self, hand, count):
        # print(hand)
        if hand == [0]*10:
            return True
        if hand[9] >= 3:
            hand[9] -= 3
            self.mentsu.append(9)
            if self.mentsu_check(hand,count+1):
                    return True

        for i in range(7):
            if hand[i] >= 3:
                hand[i] -= 3
                self.mentsu.append(i)
                if self.mentsu_check(hand, count+1):
                    return True
            elif hand[i] > 0 and hand[i+1] > 0 and hand[i+2] > 0:
                hand[i] -= 1
                hand[i+1] -= 1
                hand[i+2] -= 1
                self.mentsu.append(10+i)
                if self.mentsu_check(hand, count+1):
                    return True
        else:
            self.mentsu = []
            return False

    def hora_flag(self):
        for i, number in enumerate(self.contents):
            hand = list(self)
            if hand[i] >= 2:
                hand[i] -= 2
                self.head = i
                if self.mentsu_check(hand, 0):
                    return True

        else:
            return False

    def show_hand(self):
        hand = list(self)
        if self.tsumohai == -1:
            for i in range(10):
                for j in range(hand[i]):
                    print(repr(i+1) + ",", end="")
            print()
            return 0
        hand[self.tsumohai] -= 1
        for i in range(10):
            for j in range(hand[i]):
                print(repr(i+1) + ",", end="")
        print("T" + repr(self.tsumohai+1))

    def trash(self, n):
        self[n-1] -= 1

    def tsumo(self, deck):
        self.tsumohai = deck.draw()
        self[self.tsumohai] += 1


class Deck():
    def __init__(self):
        self.deck = list(range(10))*4

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop()


def gameinit(myhand, deck):
    deck.shuffle()


def myturn(myhand, deck):

    myhand.tsumo(deck)
    myhand.show_hand()
    if myhand.hora_flag():
        print("goal")
        return False
    myhand.trash(int(input()))
    return True
"""
deck = Deck()
deck.shuffle()
myhand = Hand(deck)
myhand.show_hand()
if myhand.hora_flag():
    print("goal")
myhand.trash(int(input()))
while myturn(myhand, deck):
    pass
"""

deck = Deck()
deck.shuffle()
myhand = Hand(deck)
myhand[:]  = [2,0,1,1,1,0,0,0,0,3]
myhand.tsumohai = 0
print(myhand.hora_flag())
print(myhand.mentsu[0])
myhand.show_hand()
