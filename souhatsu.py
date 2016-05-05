import random
from enum import Enum

class Hai(Enum):
    SU1 = (1, '一索', 'yi')
    SU2 = (2, '二索', 'er')
    SU3 = (3, '三索', 'san')
    SU4 = (4, '四索', 'si')
    SU5 = (5, '五索', 'wu')
    SU6 = (6, '六索', 'liu')
    SU7 = (7, '七索', 'qi')
    SU8 = (8, '八索', 'ba')
    SU9 = (9, '九索', 'jiu')
    HATSU = (0, '發', 'fa')
    DS5 = (5, '赤五', 'rw')

    @classmethod
    def valueAt(cls, num):
        for hai in cls:
            if hai.number == num:
                return hai
        return None

    @classmethod
    def AllHai(cls):
        allhai = [hai for hai in cls if not hai.number == 5] * 4
        allhai += [cls.SU5] * 3 + [cls.DS5]
        return allhai

    @property
    def number(self):
        return self.value[0]

    @property
    def hainame(self):
        return self.value[1]

    @property
    def chiname(self):
        return self.value[2]

    @property
    def is_suhai(self):
        return self.number != None

    @property
    def is_ryuhai(self):
        return self.number in [0,2,3,4,6,8]


class Hand():
    def __init__(self, deck, initnum = 8):
        self.hand = list()
        self.contents = [0]*10
        for i in range(initnum):
            tsumohai = deck.draw()
            self.contents[tsumohai.number] += 1
            self.hand.append(tsumohai)
            # self.contents[deck.draw()] += 1
        self.head = int()
        self.mentsu = []
        self.tsumohai = -1
        self.priority = None

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
        if hand[0] >= 3:
            hand[0] -= 3
            self.mentsu.append(0)
            if self.mentsu_check(hand,count+1):
                    return True

        for i in range(1,8):
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

    def hora_process(self):
        contents = list(self.contents)
        hand = list(self.hand)
        def reach(contents):
            return self.reachflag

        def tannyao(contents):
            return contents[0] == 0 \
                    and contents[1] == 0 \
                    and contents[9] == 0

        def tsumo(contents):
            return self.ronhai == None



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
        hand = list(self.contents)
        if self.tsumohai == -1:
            for i in range(10):
                for j in range(hand[i]):
                    print(repr(i) + ",", end="")
            print() 
            for item in self.hand:
                print(item.hainame, end=',')
            print()

            print()
            return 0

        hand[self.tsumohai.number] -= 1
        for i in range(10):
            for j in range(hand[i]):
                print(repr(i) + ",", end="")
                pass
        print("T" + str(self.tsumohai.number))
        self.hand.remove(self.tsumohai)
        for item in self.hand:
            print(item.hainame, end=',')
        print("T" + self.tsumohai.hainame)
        self.hand.append(self.tsumohai)

    def trash(self, n):
        self[n] -= 1
        self.hand.remove(Hai.valueAt(n))

    def tsumo(self, deck):
        self.tsumohai = deck.draw()
        self.hand.append(self.tsumohai)
        self.contents[self.tsumohai.number] += 1


class Deck():
    def __init__(self):
        self.deck = Hai.AllHai()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop()


class Field():

    def __init__(self):
        self.deck = Deck()
        self.myhand = Hand(self.deck)
        self.yourhand = Hand(self.deck, initnum=7)
        self.myriver = []
        self.yourriver = []

        self.turn = 1
        while self.oneturn():
            pass


    def oneturn(self): 
        if self.turn != 1 and hand.priority == True:
            self.myhand.tsumo(self.deck)
        self.show_field()
        if self.myhand.hora_flag():
            if self.turn == 1:
                self.myhand.tenho_flag = True
                #後で書く
            self.myhand.tsumo_flag = True
            #後で書く
            print("You win")
            return False
        command = int(input())
        self.myriver.append(Hai.valueAt(command))
        self.myhand.trash(command)

        self.yourhand.tsumo(self.deck)
        if self.yourhand.hora_flag():
            if self.turn == 1:
                self.yourhand.chiho_flag = True
            print("\n\nYou lose\n\n")
            self.yourhand.show_hand()
            return False

#        self.naki = self.nakicheck(self.yourhand.hand[0])
#        if self.naki != []:
#            print self.naki

        self.yourriver.append(self.yourhand.hand[0])
        self.yourhand.trash(self.yourhand.hand[0].number)
        return True

    def show_field(self):
        print()
        print("turn:" + str(self.turn))
        for hai in self.yourriver:
            print(hai.hainame, end="")
        print()
        for hai in self.myriver:
            print(hai.hainame, end="")
        print()

        print()
        self.myhand.show_hand()


def gameinit(myhand, deck):
    deck.shuffle()

Field()

"""
deck = Deck()
deck.shuffle()
myhand = Hand(deck)
ophand = Hand(deck)
myhand.show_hand()
if myhand.hora_flag():
    print("goal")
myhand.trash(int(input()))
while myturn(myhand, deck):
    pass
deck = Deck()
deck.shuffle()
myhand = Hand(deck)
myhand[:]  = [2,0,1,1,1,0,0,0,0,3]
myhand.tsumohai = 0
print(myhand.hora_flag())
print(myhand.mentsu[0])
myhand.show_hand()
"""
