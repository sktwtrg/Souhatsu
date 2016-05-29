import random
from enum import Enum

class Hai(Enum):
    SU1 = (1, 1, '一索', 'yi')
    SU2 = (2, 2, '二索', 'er')
    SU3 = (3, 3, '三索', 'san')
    SU4 = (4, 4, '四索', 'si')
    SU5 = (5, 5, '五索', 'wu')
    SU6 = (6, 6, '六索', 'liu')
    SU7 = (7, 7, '七索', 'qi')
    SU8 = (8, 8, '八索', 'ba')
    SU9 = (9, 9, '九索', 'jiu')
    HATSU = (0, 0, '發', 'fa')
    DS5 = (10, 5, '赤五', 'rw')

    def __init__(self, _id, _number, _hainame, _chiname):
        self._id = _id
        self._number = _number
        self._hainame = _hainame

    @classmethod
    def valueAt(cls, num):
        for hai in cls:
            if hai.ID == num:
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

    yakuhai = (0, "役", "yaku", 1)
    reach = (1, "リーチ", "reach", 1)
    tannyao = (2, "断么九", "tannyao", 1)
    tsumo = (3, "ツモ", "tsumo", 1)
    chitoitsu = (4, "七対子", "chitoitsu", 2) 
    ippatsu = (5, "一発", "ippatsu", 1) 
    rinshan = (6, "嶺上開花", "rinshan", 1) 

    def __init__(self, _id, _name, _enname, _hansu):
        self._id = _id
        self._name = _name
        self._enname = _enname
        self._hansu = _hansu

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

    @property
    def hansu(self):
        return self._hansu

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

class Block():

    def __init__(self, hais, block_type=None):
        self.type = block_type
        self.hais = hais
        self.numbers = []
        for hai in hais:
            self.numbers.append(hai.number)

    def __repr__(self):
        return self.numbers.__repr__()


class Hand():

    def __init__(self, deck, initnum = 8, test = None):

        self.hand = list()
        self.contents = [0]*10
        self.all_contents = [0]*10
        self.head = int()
        self.mentsu = []
        self.tsumohai = -1
        self.ronhai = -1
        self.furo = []
        self.yaku = []

        if test != None:
            for i in test:
                self.test_tsumo(i)
            self.tsumohai = -1
            return

        for i in range(initnum):
            self.tsumo(deck)
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
            if self.ronhai == -1 and self.furo == []:
                self.yaku.append(Yaku.valueOf("tsumo"))

        def ippatsu(player):
            if player.ippatsu_flag == True:
                self.yaku.append(Yaku.valueOf("ippatsu"))

        def rinshan(player):
            if player.rinshan_flag == True:
                self.yaku.append(Yaku.valueOf("rinshan"))

        contents = list(self.contents)
        hand = list(self.hand)
        reach(player)
        yakuhai(contents)
        tannyao(contents)
        tsumo()
        ippatsu(player)
        self.show_hand()
        print(self.yaku)
        print(self.mentsu)


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
            mentsu_hais = []
            if check_contents[0] >= 3:
                check_contents[0] -= 3
                mentsu_hais.append(Hai.valueAt(0))
                mentsu_hais.append(Hai.valueAt(0))
                mentsu_hais.append(Hai.valueAt(0))
                self.mentsu.append(Block(mentsu_hais, block_type = "anko"))
                if mentsu_check(check_contents,count+1):
                    return True
                del self.mentsu[-1]

            for i in range(1,10):
                if check_contents[i] >= 3:
                    check_contents[i] -= 3
                    mentsu_hais.append(Hai.valueAt(i))
                    mentsu_hais.append(Hai.valueAt(i))
                    mentsu_hais.append(Hai.valueAt(i))
                    self.mentsu.append(Block(mentsu_hais, block_type = "anko"))
                    if mentsu_check(check_contents, count+1):
                        return True
                    del self.mentsu[-1]
                elif i >= 8:
                    continue
                elif check_contents[i] > 0 and check_contents[i+1] > 0 and check_contents[i+2] > 0:
                    check_contents[i] -= 1
                    check_contents[i+1] -= 1
                    check_contents[i+2] -= 1
                    mentsu_hais.append(Hai.valueAt(i))
                    mentsu_hais.append(Hai.valueAt(i+1))
                    mentsu_hais.append(Hai.valueAt(i+2))
                    self.mentsu.append(Block(mentsu_hais, block_type = "shuntsu"))
                    if mentsu_check(check_contents, count+1):
                        return True
                    del self.mentsu[-1]
            else:
                return False

#        print(contents)
        if chitoitsu_check(contents):
            self.mentsu.append("chitoitsu")
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
        
    def test_tsumo(self, number):
        self.tsumohai = Hai.valueAt(number)
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
        num = str(hai.number)
        num = num + num + num
        self.furo.append("pon:" + num)

    def daiminkan(self, hai, deck):
        self.contents[hai.number] -= 3
        self.hand.remove(hai)
        self.hand.remove(hai)
        self.hand.remove(hai)
        self.tsumo(deck)
        block = Block([hai] * 4, block_type = "daiminkan")
        self.furo.append(block)
        self.show_hand()

    def ankan(self, hai, deck):
        self.contents[hai.number] -= 4
        self.hand.remove(hai)
        self.hand.remove(hai)
        self.hand.remove(hai)
        self.hand.remove(hai)
        self.tsumo(deck)
        block = Block([hai] * 4, block_type = "daiminkan")
        self.furo.append(block)
        self.show_hand()

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

    def __init__(self, name):
        self.kaze = None
        self.hand = None 
        self.name = name
        self.score = int()

    def make_hand(self, hand):
        self.hand = hand
        self.river = []
        self.reach = False
        self.tsumo = False
        self.ron = False
        self.rinshan = False
        self.naki_status = None
        self.ippatsu_flag = False


class Command():
    
    def __init__(self,cmd):

        if "5r" in cmd:
            self.reach  = False
            self.number = int(5)
            self.kan = False
            self.hai = Hai.valueAt(10)
        else:
            self.reach = False
            self.number = int(cmd[-1])
            self.kan = False
            self.hai = Hai.valueAt(self.number)

        if cmd[0] == "r":
            self.reach = True
        elif cmd[0] == "k":
            self.kan = True
        elif cmd == "tsumo":
            pass


class Field():

    def __init__(self):

        self.yourplayer = Player("You")
        self.op_player= Player("OP")
        self.previous_winner = None
        while self.onesession():
            self.deck = Deck()
            self.yourplayer.make_hand(Hand(self.deck, test = [0,0,0,0,9,6,9,9]))
            self.op_player.make_hand(Hand(self.deck, initnum=7, test = [2,2,2,1,1,1,9]))
            self.turn = 1
            self.whos_turn = Kaze.valueOf("oya")
            self.who_priority()
            while self.oneturn(self.nextplayer):
                pass
            print("HAIPAI!!\n")
            input()

    def who_priority(self):

        if self.previous_winner != None:
            self.nextplayer = self.previous_winner
            if self.nextplayer == self.yourplayer:
                self.thisplayer = self.op_player
            else:
                self.thisplayer = self.yourplayer
            self.thisplayer.kaze = Kaze.valueOf("oya")
            self.nextplayer.kaze = Kaze.valueOf("ko")
        else:
            self.yourplayer.kaze = Kaze.valueOf("oya")
            self.op_player.kaze = Kaze.valueOf("ko")
            self.thisplayer = self.op_player
            self.nextplayer = self.yourplayer

    def onesession(self):
        return True


    def oneturn(self, player): 

        def tsumo_phase():
            pass

        def hora_check_phase(player):
            if player.hand.hora_flag(player.hand.contents)\
                    and player.naki_status in [None, "ron"]:
                player.hand.hora_process(player)
                self.previous_winner = player
                player.score += 1
                print(player.score)
                return True
            else:
                player.tsumo = True
                player.ron = False
                return False

        def naki_process(player,hai,cmd):
            if cmd == "pon":
                player.hand.pon(hai)
            elif cmd == "kan":
                player.hand.daiminkan(hai,self.deck)
                if hora_check_phase(player):
                    return False
                player.rinshan = False
                trash_phase(player, self.deck)

            elif cmd == "ron":
                player.hand.ron(hai)
            else:
                return None
            return cmd

        def naki_phase(player, nextplayer):
            if nextplayer.hand.nakipattern(player.sutehai) != []:
                print("\n\n\n\n" + nextplayer.name)
                print("sutehai:", player.sutehai.hainame)
                nextplayer.hand.show_hand()
                print(nextplayer.hand.nakipattern(player.sutehai))
                if player.name == "You":
                    command = str(input())
                else:
                    command = str(input())
                naki_option = naki_process(nextplayer, player.sutehai, command)
                if naki_option != None:
                    nextplayer.naki_status = naki_option
                    player.ippatsu_flag = False
                else:
                    nextplayer.naki_status = None
            #鳴き、ロンの処理


        def trash_phase(player, deck):
            if player.name == "You":
                print("PUT COMMAND")
                command = Command(str(input()))
                if command.reach == True:
                    player.reach = True
                    player.ippatsu_flag = True
                else: 
                    player.ippatsu_flag = False
                if command.kan == True:
                    player.rinshan = True
                    player.hand.ankan(command.hai, deck)
                    if hora_check_phase(player):
                        return True
                    player.rinshan = False
                    trash_phase(player, deck)
                    return
                else:
                    player.sutehai = command.hai

            else:
                player.sutehai = player.hand.hand[0]
            player.hand.tsumohai = -1
            player.river.append(player.sutehai)
            player.hand.trash(player.sutehai)
            #川に切る処理

            player.naki_status = None

        def ryukyoku_check(deck):
            if deck.deck == []:
                return True

        def ryukyoku_process():
            #親を変える
            #罰符
            pass


        #playerの更新
        self.nextplayer, self.thisplayer = self.thisplayer, self.nextplayer
        #この時,self.thisplayer = player

        #tsumo
        if len(player.hand.hand) in [1,4,7]:
            player.hand.tsumo(self.deck)
            player.tsumo = True
        self.show_field()
        if hora_check_phase(player):
            return False
        if trash_phase(player, self.deck):
            #嶺上開花の時のみ終わる
            return False
        naki_phase(player, self.nextplayer)
        #鳴き、ロンの処理

        if ryukyoku_check(self.deck):
            ryukyoku_process()
            return False

        if player.kaze.enname == "oya":
            self.turn += 1
        return True

    def show_field(self):
        print("\n\n\n\n----------------------")
        print(self.thisplayer.name + " Turn")
        print("----------------------")
        print(self.op_player.name + " Hand Score:" + str(self.op_player.score))
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
        print(self.yourplayer.name + " Hand Score:" + str(self.yourplayer.score))
        self.yourplayer.hand.show_hand()
        print("----------------------")


def gameinit(myhand, deck):
    deck.shuffle()

if __name__ == "__main__":
    Field()

