import random
from enum import Enum

class Hai(Enum):
    SU1 = (0, 1, '一索', 'yi')
    SU2 = (1, 2, '二索', 'er')
    SU3 = (2, 3, '三索', 'san')
    SU4 = (3, 4, '四索', 'si')
    SU5 = (4, 5, '五索', 'wu')
    SU6 = (5, 6, '六索', 'liu')
    SU7 = (6, 7, '七索', 'qi')
    SU8 = (7, 8, '八索', 'ba')
    SU9 = (8, 9, '九索', 'jiu')
    HATSU = (9, 0, '發', 'fa')
    DS5 = (10, 5, '赤五', 'rw')

    def __init__(self, _id, _number, _hainame, _chiname):
        self._id = _id
        self._number = _number
        self._hainame = _hainame

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
    def ID(self):
        return self._id

    @property
    def number(self):
        return self._number

    @property
    def hainame(self):
        return self._hainame

    @property
    def chiname(self):
        return self.value[3]

    @property
    def is_suhai(self):
        return self.number != None

    @property
    def is_ryuhai(self):
        return self.number in [0,2,3,4,6,8]


class Yaku(Enum):

    yakuhai = (0, "役", "yaku")
    reach = (1, "リーチ", "reach")
    tannyao = (2, "断么九", "tannyao")
    tsumo = (3, "ツモ", "tsumo")
    chitoitsu = (4, "七対子", "chitoitsu")


    def __init__(self, _id, _name, _enname):
        self._id = _id
        self._name = _name
        self._enname = _enname

    @classmethod
    def valueOf(cls, enname):
        for yaku in cls:
            if yaku.enname == enname:
                return yaku
        return None

    @classmethod
    def AllHai(cls):
        pass

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def enname(self):
        return self._enname


class Kaze(Enum):

    oya = (0, "親", "oya")
    ko = (1, "子", "ko")

    def __init__(self, _id, _name, _enname):
        self._id = _id
        self._name = _name
        self._enname = _enname

    @classmethod
    def valueOf(cls, name):
        for kaze in cls:
            if kaze.enname == name:
                return kaze
        return None

    @property
    def ID(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def enname(self):
        return self._enname

    def next_turn(self):
        if self.enname == "oya":
            return self.valueOf("ko")
        else:
            return self.valueOf("oya")


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
        self.ronhai = -1
        self.furo = []
        self.yaku = []

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

    def hora_process(self,player):

        def reach(player):
            if player.reach == True:
                self.yaku.append(Yaku.valueOf("reach"))

        def yakuhai(contents):
            if self.contents[0] == 3\
                    or 0 in self.furo:
                self.yaku.append(Yaku.valueOf("yaku"))

        def tannyao(contents):
            if contents[0] == 0 \
                    and contents[1] == 0 \
                    and contents[9] == 0:
                self.yaku.append(Yaku.valueOf("tannyao"))

        def tsumo():
            if self.ronhai == -1:
                self.yaku.append(Yaku.valueOf("tsumo"))

        contents = list(self.contents)
        hand = list(self.hand)
        reach(player)
        yakuhai(contents)
        tannyao(contents)
        tsumo()
        print(self.yaku)


    def hora_flag(self,contents):

        def chitoitsu_check(contents):
            toitsu_num = 0
            for num in contents:
                if num == 2:
                    toitsu_num += 1
                if toitsu_num == 4:
                    return True

        def mentsu_check(check_contents, count):
            if check_contents == [0]*10:
                return True
            if check_contents[0] >= 3:
                check_contents[0] -= 3
                self.mentsu.append(0)
                if mentsu_check(check_contents,count+1):
                    return True

            for i in range(1,10):
                if check_contents[i] >= 3:
                    check_contents[i] -= 3
                    self.mentsu.append(i)
                    if mentsu_check(check_contents, count+1):
                        return True
                elif i >= 8:
                    continue
                elif check_contents[i] > 0 and check_contents[i+1] > 0 and check_contents[i+2] > 0:
                    check_contents[i] -= 1
                    check_contents[i+1] -= 1
                    check_contents[i+2] -= 1
                    self.mentsu.append(10+i)
                    if mentsu_check(check_contents, count+1):
                        return True
            else:
                self.mentsu = []
                return False

#        print(contents)
        if chitoitsu_check(contents):
            self.yaku.append(Yaku.valueOf("chitoitsu"))
            return True

        for i, number in enumerate(contents):
            contents_check = list(contents)[:]
            if contents_check[i] >= 2:
                contents_check[i] -= 2
                self.head = i
#                print("head:",self.head)
                if mentsu_check(contents_check, 0):
                    return True
        else:
                self.yaku = []
                return False


    def tenpai_flag(self):
#        hand = copy.deepcopy(self)
        contents = self.contents
        matihais = []
        print(contents)
        if len(self.hand) in [2, 5, 8]:
            for i in range(10):
                contents_reduced = self.contents[:]
                if contents[i] > 0:
                    contents_reduced[i] -= 1
                else:
                    continue
                for j in range(10):
                    contents_temp = contents_reduced[:]
                    contents_temp[j] += 1
                    if self.hora_flag(contents_temp):
                        matihais.append(i)
                        break
            if matihais != []:
                print(matihais)
                return True
            else:
                return False

        for i in range(10):
            contents[i] += 1
            if self.hora_flag(contents):
                return True
        return False


    def show_hand(self):
        contents = list(self.contents)[:]
        hand = list(self.hand)[:]

        if self.tsumohai != -1: contents[self.tsumohai.number] -= 1
        for i in range(10):
            for j in range(contents[i]):
                print(repr(i) + ",", end="")
                pass
        if self.tsumohai != -1:
            print("T" + str(self.tsumohai.number), end="")
        if self.furo != []:
            print("副露:",self.furo)
        print()

        if self.tsumohai != -1:
            hand.remove(self.tsumohai)
        for item in hand:
            print(item.hainame, end=',')
        if self.tsumohai != -1:
            print("T" + self.tsumohai.hainame)
        else:
            print()

    def trash(self, hai):
        self[hai.number] -= 1
        self.hand.remove(hai)

    def tsumo(self, deck):
        self.tsumohai = deck.draw()
        self.hand.append(self.tsumohai)
        self.contents[self.tsumohai.number] += 1

    def nakipattern(self, hai):
        def pon_check(hai):
            return self.contents[hai.number] >= 2
        def kan_check(hai):
            return self.contents[hai.number] >= 3
        def ron_check(hai):
            contents = self.contents[:]
            contents[hai.number] += 1
            return self.hora_flag(contents)
        nakipattern = []
        if pon_check(hai): nakipattern.append("pon")
        if kan_check(hai): nakipattern.append("kan")
        if ron_check(hai): nakipattern.append("ron")
        return nakipattern

    def pon(self, hai):
        self.contents[hai.number] -= 2
        self.hand.remove(hai)
        self.hand.remove(hai)
        self.furo.append(hai.number)

    def daiminkan(self, hai, deck):
        self.contents[hai.number] -= 3
        self.hand.remove(hai)
        self.hand.remove(hai)
        self.hand.remove(hai)
        self.tsumo(self, deck)
        self.furo.append(hai.number)

    def ron(self, hai):
        self.ronhai = hai
        self.tsumohai = -1
        self.contents[hai.number] += 1
        self.hand.append(hai)

class Deck():

    def __init__(self):
        self.deck = Hai.AllHai()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop()

class Player():

    def __init__(self, name, hand):
        self.kaze = None
        self.hand = hand
        self.name = name
        self.river = []
        self.reach = False
        self.tsumo = False
        self.ron = False
        self.naki_status = None


class Command():
    
    def __init__(self,cmd):

        if len(cmd) == 1:
            self.reach = False
            self.number = int(cmd)
            self.kan = False
        elif cmd[0] == "r":
            self.reach = True
            self.number = int(cmd[1])
            self.kan = False
        elif cmd[0] == "k":
            self.reach = False
            self.number = int(cmd[1]) 
            self.kan = True
        elif cmd == "tsumo":
            pass


class Field():

    def __init__(self):

        self.deck = Deck()
        self.yourplayer = Player("You", Hand(self.deck))
        self.op_player = Player("OP", Hand(self.deck, initnum=7))
        self.turn = 1
        self.whos_turn = Kaze.valueOf("oya")
        self.who_priority()
        while self.oneturn(self.nextplayer):
            pass

    def who_priority(self):

        self.yourplayer.kaze = Kaze.valueOf("oya")
        self.op_player.kaze = Kaze.valueOf("ko")
        self.thisplayer = self.op_player
        self.nextplayer = self.yourplayer

    def oneturn(self, player): 

        def tsumo_phase():
            pass

        def naki_phase(hand,hai,cmd):
            if cmd == "pon":
                hand.pon(hai)
            elif cmd == "kan":
                hand.daiminkan(hai,self.deck)
            elif cmd == "ron":
                hand.ron(hai)
            else:
                return None
            return cmd

        def hora_check_phase(player):
            if player.hand.hora_flag(player.hand.contents)\
                    and player.naki_status in [None, "ron"]:
                player.hand.hora_process(player)
                if player.name == "You":
                    print("\nYou win\n")
                    print(player.hand.yaku)
                else:
                    print("\n\You lose\n")
                    player.hand.show_hand()
                return True
            else:
                player.tsumo = True
                player.ron = False
                return False


        def trash_phase(player):
            if player.name == "You":
                command = Command(input())
                if command.reach == True:
                    player.reach = True
                    player.hand.yaku.append(Yaku.valueOf("reach"))
                player.sutehai = Hai.valueAt(command.number)
            else:
                player.sutehai = player.hand.hand[0]
            player.hand.tsumohai = -1
            player.river.append(player.sutehai)
            player.hand.trash(player.sutehai)
            #川に切る処理

            player.naki_status = None

        #playerの更新
        self.nextplayer, self.thisplayer = self.thisplayer, self.nextplayer
        #この時,self.thisplayer = player

        #tsumo
        if len(player.hand.hand) in [1,4,7]:
            player.hand.tsumo(self.deck)
            player.tsumo = True
        #player.hand.contents = [3,0,2,0,0,0,0,0,0,0]
        self.show_field()

        if hora_check_phase(player):
            return False

        trash_phase(player)

        if self.nextplayer.hand.nakipattern(player.sutehai) != []:
            print("\n\n\n\n" + self.nextplayer.name)
            print("sutehai:",player.sutehai.hainame)
            self.nextplayer.hand.show_hand()
            print(self.nextplayer.hand.nakipattern(player.sutehai))
            if player.name == "You":
                command = str(input())
            else:
                command = str(input())
            naki_option = naki_phase(self.nextplayer.hand, player.sutehai, command)
            if naki_option != None:
                self.nextplayer.naki_status = naki_option
            else:
                self.nextplayer.naki_status = None
        #鳴き、ロンの処理

        if player.kaze.enname == "oya":
            self.turn += 1

        return True

    def show_field(self):
        print("\n\n\n\n----------------------")
        print(self.thisplayer.name + " Turn")
        print("----------------------")
        print(self.op_player.name + " Hand")
        self.op_player.hand.show_hand()
        print("\n\n")
        if self.op_player.reach == True:
            print("REACH!!")
        for hai in self.op_player.river:
            print(hai.hainame, end="")
        print()
        print("turn:" + str(self.turn))
        for hai in self.yourplayer.river:
            print(hai.hainame, end="")
        if self.yourplayer.reach == True:
            print("\nREACH!!")
        print("\n\n\n")
        print(self.yourplayer.name + " Hand")
        self.yourplayer.hand.show_hand()
        print("----------------------")


def gameinit(myhand, deck):
    deck.shuffle()

if __name__ == "__main__":
    Field()

