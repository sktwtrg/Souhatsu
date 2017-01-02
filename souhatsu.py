import random
import math
from PIL import Image
from sdl2 import *
import sdl2.ext as sdl2ext
import score_board
import SouhatsuEnums
from TextBoxManager import TextBoxManager
from sdl2systems import *

class Block:

    def __init__(self, hais, block_type=None):
        self.type = block_type
        self.hais = hais
        self.entities = None
        self.numbers = []
        self.fu = 0
        for hai in hais:
            self.numbers.append(hai.number)
        self.block_fu_check()

    def set_entities(self, entities):
        self.entities = entities 

    def __repr__(self):
        return self.numbers.__repr__()

    def move(self, player):
        if self.type == 'minko':
            position = (player.hand_pos[0] + len(player.hand.hand) * player.hand.hai_size[0] + 20, player.hand_pos[1])
            entities[0].move(position[0], position[1])
            entities[1].move(position[0] + Hand.hai_size[0], position[1])
            entities[2].move(position[0] + Hand.hai_size * 2 , position[1])

    def block_fu_check(self):
        if self.type == 'shuntsu':
            pass
        elif self.type == 'anko':
            if 1 < self.numbers[0]< 9 : 
                self.fu = 4
            else :
                self.fu = 8
        elif self.type == 'minko':
            if 1 < self.numbers[0]< 9 : 
                self.fu = 2
            else :
                self.fu = 4
        elif self.type == 'daiminkan':
            if 1 < self.numbers[0]< 9 : 
                self.fu = 8
            else :
                self.fu = 16
        elif self.type == 'ankan':
            if 1 < self.numbers[0]< 9 : 
                self.fu = 16
            else :
                self.fu = 32
        elif self.type == 'head':
            if self.numbers[0] == 0: self.fu = 2
        elif self.type == 'chitoitsu':
            self.fu = 25

class Hand:

    #sizeなど外部か
    hai_size = (40, 60)

    def __init__(self, deck, player, world, factory, movement, initnum = 8, test = None):

        self.player = player
        self.world = world
        self.factory = factory
        self.movement = movement
        self.hand = list()
        self.entities = list()
        self.contents = [0]*10
        self.head = int()
        self.mentsu = []
        self.tsumohai = -1
        self.ronhai = -1
        self.agarihai = -1
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

    def machi_type_check(self):
        #TODO:描き方変？
        if self.mentsu[0].type == 'chitoitsu':
            self.machi_type_candidate.append('tanki')
            self.machi_type= 'tanki'
        elif self.agarihai.number in self.head.numbers:
            self.machi_type_candidate.append('tanki')
            self.machi_type= 'tanki'

        for block in self.mentsu:
            if block.type in ['minko','daiminkan']:
                pass
            if block.type == 'shuntsu':
                if self.agarihai.number == block.numbers[1]:
                    self.machi_type_candidate.append('kanchan')
                    self.machi_type= 'kanchan'
                elif (block.numbers[0] == 1 and self.agarihai.number == 3)\
                        or (block.numbers[2] == 9 and self.agarihai.number == 7):
                    self.machi_type_candidate.append('penchan')
                    self.machi_type= 'penchan'
                elif self.agarihai.number in block.numbers:
                    self.machi_type_candidate.append('ryanmen')
                    self.machi_type = 'ryanmen'
            elif self.agarihai.number in block.numbers:
                self.machi_type_candidate.append('shabo')
                self.machi_type = 'shabo'



    def yaku_check(self, player):
        self.yaku = []

        def double_reach(player):
            if player.double_reach == True:
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("double_reach"))

        def reach(player):
            if player.reach == True and \
                    player.double_reach == False:
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("reach"))

        def yakuhai():
            if self.contents[0] == 3:
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("yaku"))
            for block in self.furo:
                if 0 in block.numbers:
                    self.yaku.append(SouhatsuEnums.Yaku.valueOf("yaku"))

        def tannyao():
            if self.contents[0] == 0 \
                    and self.contents[1] == 0 \
                    and self.contents[9] == 0:
                pass
            else:
                return
            for block in self.furo:
                if 0 in block.numbers or\
                        1 in block.numbers or\
                        9 in block.numbers:
                    return
            else:
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("tannyao"))


        def pinfu():
            if not self.mensen:
                return

            if 'ryanmen' not in self.machi_type_candidate:
                return
            for block in self.mentsu:
                if block.fu != 0:
                    return
            if self.head.fu != 0:
                return
            self.yaku.append(SouhatsuEnums.Yaku.valueOf("pinfu"))

            if self.ronhai == -1:
                self.fu = 20

        def tsumo():
            if self.ronhai == -1 \
                    and self.mensen:
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("tsumo"))

        def ippatsu(player):
            if player.ippatsu_flag == True:
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("ippatsu"))

        def chitoitsu():
            if self.mentsu[0].type == 'chitoitsu':
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("chitoitsu"))
                self.fu = 25

        def rinshan(player):
            if player.rinshan == True:
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("rinshan"))

        def ryuiso():
            for hai in self.hand:
                if not hai.is_ryuhai:
                    break
            else:
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("ryuiso"))

        def tenhou(player):
            if player.tenhou_flag:
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("tenhou"))

        def chihou(player):
            if player.chihou_flag and\
                    self.ronhai == -1:
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("chihou"))

        def renhou(player):
            if player.chihou_flag and\
                    self.ronhai != -1:
                self.yaku.append(SouhatsuEnums.Yaku.valueOf("renhou"))

        def toitoihou():
            for block in self.mentsu:
                if block.type not in ('minko', 'anko', 'ankan', 'daiminkan'):
                    return
            self.yaku.append(SouhatsuEnums.Yaku.valueOf("toitoihou"))

        def ryananko():
            for block in self.mentsu:
                if block.type not in ('anko', 'ankan'):
                    return
            self.yaku.append(SouhatsuEnums.Yaku.valueOf("ryananko"))

        def ipeiko():
            #TODO:未実装、必要？
            return

        def chanta_etc():
            if self.mentsu[0].type == 'chitoitsu':
                return

            for block in self.mentsu:
                if not (block.type in ('anko', 'minko', 'ankan', 'minkan')\
                        and block.numbers[0] in (0,1,9)):
                    break
            else:
                if self.head.numbers[0]in (0,1,9):
                    self.yaku.append(SouhatsuEnums.Yaku.valueOf("honroutou"))
                    return

            for block in self.mentsu:
                if block.numbers[0] != 1 and\
                        block.numbers[2] != 9:
                    break
            else:
                if self.head.numbers[0]in (1,9):
                    self.yaku.append(SouhatsuEnums.Yaku.valueOf("junchan"))
                    return

            for block in self.mentsu:
                if block.numbers[0] not in (0,1) and\
                        block.numbers[2] != 9:
                    break
            else:
                if self.head.numbers[0]in (0,1,9):
                    self.yaku.append(SouhatsuEnums.Yaku.valueOf("chanta"))
                    return



        hand = list(self.hand)
        double_reach(player)
        reach(player)
        pinfu()
        yakuhai()
        tannyao()
        tsumo()
        ippatsu(player)
        chitoitsu()
        rinshan(player)
        ryuiso()
        tenhou(player)
        chihou(player)
        renhou(player)
        toitoihou()
        ryananko()
        ipeiko()
        chanta_etc()

        for yaku in self.yaku:
            self.hansu += yaku.hansu

    def fu_check(self):
        if self.fu in (20,25):
            return
        if self.ronhai == -1:
            self.fu = 22
        elif self.mensen:
            self.fu = 30
        else:
            self.fu = 20

        for block in self.mentsu:
            self.fu += block.fu

        self.fu += self.head.fu

        if self.machi_type_candidate[0] in ['penchan', 'kanchan', 'tanki']:
            self.fu += 2
        self.fu = int(10 * math.ceil(float(self.fu) * 0.1))

    def ten_check(self):
#        self.hansu += 4
        print('namecheck:' + self.player.kaze.enname)
        #ハネマン以上
        if self.hansu >= 6:
            if self.hansu in (6,7):
                self.ten = 12000
            elif self.hansu in (8,9,10):
                self.ten = 16000
            elif self.hansu in (11,12):
                self.ten = 24000
            else:
                self.ten = 32000
            if self.player.kaze.enname == 'oya':
                self.ten = int(1.5 * self.ten)
                if self.ronhai == -1:
                    self.ten = int(2.0 * self.ten / 3)
            elif self.ronhai == -1:
                self.ten = int(3.0 * self.ten / 4)
            return

        #満貫以下
        if self.player.kaze.enname == 'ko':
            self.ten = int(100 * math.ceil(0.01 * self.fu * 4 * float(pow(2, 2 + self.hansu))))
            if self.ten >= 8000:
                self.ten = 8000
        elif self.player.kaze.enname == 'oya':
            self.ten = int(100 * math.ceil(0.01 * self.fu * 6 * float(pow(2, 2 + self.hansu))))
            if self.ten >= 12000:
                self.ten = 12000

        if self.ronhai != -1:
            self.ten = int(1000 * math.ceil(0.001 * float(self.ten)))
        else:
            if self.player.kaze.enname == 'ko':
                self.ten = int(1000 * math.ceil(0.001 * (float(self.ten)/4))) + int(1000 * math.ceil(0.001 * (float(self.ten)/2)))
            elif self.player.kaze.enname == 'oya':
                self.ten = int(1000 * math.ceil(0.001 * (float(self.ten)/3))) * 2

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

    def hora_flag(self, contents, agarihai, ron):
        self.mentsu = []

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
            #TODO:change this
            mentsu_hais = []
            if check_contents[0] >= 3:
                check_contents[0] -= 3
                for x in range(3):
                    mentsu_hais.append(
                            SouhatsuEnums.Hai.valueAt(0)
                            )
                if ron and agarihai.number == 0:
                    self.mentsu.append(
                            Block(
                                mentsu_hais,
                                block_type = "minko"
                                )
                            )
                else:
                    self.mentsu.append(
                            Block(
                                mentsu_hais,
                                block_type = "anko"
                                )
                            )
                #発面子を抜いて面子チェック
                if mentsu_check(check_contents,count+1):
                    return True
                del self.mentsu[-1]

            for i in range(1,10):
                if check_contents[i] >= 3:
                    check_contents[i] -= 3
                    for x in range(3):
                        mentsu_hais.append(SouhatsuEnums.Hai.valueAt(i))
                    if ron and agarihai.number == i:
                        self.mentsu.append(
                                Block(
                                    mentsu_hais,
                                    block_type = "minko"
                                    )
                                )
                    else:
                        self.mentsu.append(
                                Block(
                                    mentsu_hais,
                                    block_type = "anko"
                                    )
                                )
                    if mentsu_check(check_contents, count+1):
                        return True
                    del self.mentsu[-1]
                elif i >= 8:
                    continue
                elif check_contents[i] > 0 and check_contents[i+1] > 0 and check_contents[i+2] > 0:
                    check_contents[i] -= 1
                    check_contents[i+1] -= 1
                    check_contents[i+2] -= 1
                    mentsu_hais.append(SouhatsuEnums.Hai.valueAt(i))
                    mentsu_hais.append(SouhatsuEnums.Hai.valueAt(i+1))
                    mentsu_hais.append(SouhatsuEnums.Hai.valueAt(i+2))
                    self.mentsu.append(Block(mentsu_hais, block_type = "shuntsu"))
                    #順子を抜いて面子チェック
                    if mentsu_check(check_contents, count+1):
                        return True
                    del self.mentsu[-1]
            else:
                return False

#        print(contents)
        if chitoitsu_check(contents):
            #TODO:チートイツのブロックは0とする
            block = Block([SouhatsuEnums.Hai.valueAt(0)], block_type = "chitoitsu")
            self.mentsu.append(block)
            return True

        for i, number in enumerate(contents):
            contents_check = list(contents)[:]
            if contents_check[i] >= 2:
                contents_check[i] -= 2
                self.head = Block([SouhatsuEnums.Hai.valueAt(i)]*2, block_type = "head")
                #一つ目の面子チェック
                if mentsu_check(contents_check, 0):
                    self.mentsu += self.furo
                    return True
        else:
            self.yaku = []
            self.mentsu = []
            return False


    def tenpai_flag(self):
        #使ってない
#        hand = copy.deepcopy(self)
        contents = self.contents
        matihais = []
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
        
        print(contents)

    def trash(self, hai):
        self[hai.number] -= 1
        self.hand.remove(hai)

    def tsumo(self, deck):
        self.tsumohai = deck.draw()
        self.hand.append(self.tsumohai)
        self.contents[self.tsumohai.number] += 1

        #TODO:ここを関数化
        img_pil = Image.open(self.tsumohai.img_path)
        img_pil = img_pil.resize(Hand.hai_size)
        img_surface = pilSurface(img_pil)
        entity = SouhatsuEnums.HaiEntity(self.world, self.factory.from_surface(img_surface.contents), self.tsumohai, self.player.hand_pos[0] + 41 * (len(self.hand) - 1), self.player.hand_pos[1])

        self.movement.hais.append(entity) 
        self.entities.append(entity)
        self.world.hai_entities.append(entity)
        self.world.process()
        #TODO:ここまでなんとかする
        return self.tsumohai
        
    def test_tsumo(self, number):
        self.tsumohai = SouhatsuEnums.Hai.valueAt(number)
        self.hand.append(self.tsumohai)
        self.contents[self.tsumohai.number] += 1

        #TODO:ここを関数化
        img_pil = Image.open(self.tsumohai.img_path)
        img_pil = img_pil.resize(Hand.hai_size)
        img_surface = pilSurface(img_pil)
        entity = SouhatsuEnums.HaiEntity(self.world, self.factory.from_surface(img_surface.contents), self.tsumohai, self.player.hand_pos[0] + 41 * (len(self.hand) - 1), self.player.hand_pos[1])

        self.movement.hais.append(entity) 
        self.entities.append(entity)
        self.world.hai_entities.append(entity)
        self.world.process()
            #TODO:ここまでなんとかする

    def nakipattern(self, hai):
        IsReach = self.player.reach
        def pon_check(hai):
            return (not IsReach) and self.contents[hai.number] >= 2
        def kan_check(hai):
            return (not IsReach) and self.contents[hai.number] >= 3
        def ron_check(hai):
            contents = self.contents[:]
            contents[hai.number] += 1
            return self.hora_flag(contents, hai, True)
        nakipattern = []
        if pon_check(hai): nakipattern.append("pon")
        if kan_check(hai): nakipattern.append("kan")
        if ron_check(hai): nakipattern.append("ron")
        return nakipattern

    def rihai_move(self):
        for i, entity in enumerate(self.entities):
            entity.move(self.player.hand_pos[0] + (Hand.hai_size[0] + 1) * i, self.player.hand_pos[1])

    def pon(self, entity):
        self.hand.append(entity.hai)
        self.entities.append(entity)
        num = entity.hai.number
        self.contents[num] -= 2
        block_hais = []
        block_entities = []
        for i in range(3):
            for entity in self.entities:
                if entity.hai.number != num:
                    continue
                self.hand.remove(entity.hai)
                self.entities.remove(entity)
                block_hais.append(entity.hai)
                block_entities.append(entity)
                break
        block = Block(block_hais, block_type = "minko")
        block.set_entities(block_entities)
        self.pon_move(block_entities)
        self.mensen = False
        self.furo.append(block)
        self.world.process()

    def pon_move(self, entities):
        position = (self.player.hand_pos[0] + len(self.player.hand.hand) * self.hai_size[0] + 20, self.player.hand_pos[1])
        entities[0].move(position[0], position[1])
        entities[1].move(position[0] + self.hai_size[0], position[1])
        entities[2].move(position[0] + self.hai_size[0] * 2 , position[1])
        self.rihai_move()


    def daiminkan(self, entity, deck):
        self.hand.append(entity.hai)
        self.entities.append(entity)
        num = entity.hai.number
        self.contents[num] -= 3
        block_hais = []
        block_entities = []
        for i in range(4):
            for entity in self.entities:
                if entity.hai.number != num:
                    continue
                self.hand.remove(entity.hai)
                self.entities.remove(entity)
                block_hais.append(entity.hai)
                block_entities.append(entity)
                break
        block = Block(block_hais, block_type = "daiminkan")
        block.set_entities(block_entities)
        self.daiminkan_move(block_entities)
        self.furo.append(block)
        self.mensen = False
        self.show_hand()
        self.world.process()

    def daiminkan_move(self, entities):
        position = (self.player.hand_pos[0] + (len(self.player.hand.hand) + 1) * self.hai_size[0] + 20, self.player.hand_pos[1])
        entities[0].move(position[0], position[1])
        entities[1].move(position[0] + self.hai_size[0], position[1])
        entities[2].move(position[0] + self.hai_size[0] * 2 , position[1])
        entities[3].move(position[0] + self.hai_size[0] * 3 , position[1])
        self.rihai_move()

    def ankan(self, num, deck):
        self.contents[num] -= 4
        block_hais = []
        block_entities = []
        for i in range(4):
            for entity in self.entities:
                if entity.hai.number != num:
                    continue
                self.hand.remove(entity.hai)
                self.entities.remove(entity)
                block_hais.append(entity.hai)
                block_entities.append(entity)
                break
        self.tsumo(deck)
        block = Block(block_hais, block_type = "ankan")
        block.set_entities(block_entities)
        self.ankan_move(block_entities)
        self.furo.append(block)
        self.show_hand()
        self.world.process()

    def ankan_move(self, entities):
        position = (self.player.hand_pos[0] + (len(self.player.hand.hand) + 1) * self.hai_size[0] + 20, self.player.hand_pos[1])
        entities[0].move(position[0], position[1])
        entities[1].move(position[0] + self.hai_size[0], position[1])
        entities[2].move(position[0] + self.hai_size[0] * 2 , position[1])
        entities[3].move(position[0] + self.hai_size[0] * 3 , position[1])
        self.rihai_move()

    def ron(self, entity):
        self.ronhai = entity.hai
        self.tsumohai = -1
        self.contents[entity.hai.number] += 1
        self.hand.append(entity.hai)
        self.entities.append(entity)
        self.agarihai = entity.hai

class Deck:

    def __init__(self):
        self.deck = SouhatsuEnums.Hai.AllHai()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop()

class Player:

    def __init__(self, name, player_pos):
        self.kaze = None
        self.hand = None
        self.name = name
        self.score = 35000

        self.player_pos = player_pos
        self.next = None

        if player_pos == 'up':
            self.hand_pos = (180, 100)
            self.river_pos = (150, 200)
        if player_pos == 'down':
            self.hand_pos = (120,400)
            self.river_pos = (150,300)

    def set_next(self, nextplayer):
        self.next = nextplayer

    def make_hand(self, hand):
        self.hand = hand
        self.river = []
        self.river_entities = []
        self.double_reach = False
        self.reach = False
        if self.kaze.enname == 'oya':
            self.tenhou_flag = True
            self.chihou_flag = False
        else:
            self.tenhou_flag = False
            self.chihou_flag = True
        self.tsumo = False
        self.ron = False
        self.rinshan = False
        self.naki_status = None
        self.ippatsu_flag = False

    def reach_move(self, factory, world):
        #TODO:ここを関数化
        img_pil = Image.open('./pai-images/tennbou-001.png')
        img_pil = img_pil.transpose(Image.ROTATE_90)
        img_pil = img_pil.resize((150,7))

        img_surface = pilSurface(img_pil)
        entity = SouhatsuEnums.TenbouEntity(
                world,
                factory.from_surface(img_surface.contents),
                self.river_pos[0] + 60,
                self.river_pos[1] - 15
                )

        self.ribou = entity
        #TODO:world.hai_entitiesに入れる?
        world.hai_entities.append(entity)
        world.process()
        #TODO:ここまでなんとかする

class Command:
    
    def __init__(self, cmd, player, river, gui = False, textbox_manager = None, world = None):
        self.reach  = False
        self.number = None
        self.kan = False
        self.hai = None
        self.state = False

        if gui:
            self.textbox_manager = textbox_manager
            self.world = world
            self.river = river
            self.gui_trash_parse(player)
            return

        if len(cmd) == 0: 
            self.state = False
            return

        if "5r" in cmd:
            self.reach  = False
            self.number = int(5)
            self.kan = False
            self.hai = SouhatsuEnums.Hai.valueAt(10)
        elif cmd[-1] in [str(x) for x in range(10)]:
            self.reach = False
            self.number = int(cmd[-1])
            self.kan = False
            self.hai = SouhatsuEnums.Hai.valueAt(self.number)
        else:
            self.state = False
            return 

        if cmd[0] == "r":
            self.reach = True
        elif cmd[0] == "k":
            self.kan = True
        elif cmd == "tsumo":
            pass
        self.state =  self.candidate(player)

    def candidate(self, player):

        if self.hai not in player.hand.hand:
            return False
        if self.kan == True and player.hand.contents[self.number] < 4:
            return False
        if self.reach == True and False:
            return False
        return True

    def gui_trash_parse(self, player):
        self.reach = False
        self.kan = False
        self.state = True
        self.button_names = []
        if not player.reach and \
                player.hand.mensen:
            self.textbox_manager.make_button('reach')
            self.button_names.append('reach')

        if 4 in player.hand.contents:
            self.textbox_manager.make_button('kan')
            self.button_names.append('kan')
        self.world.process()
        while True:
            events = sdl2ext.get_events()
            if (player.reach and\
                    self.hai == player.hand.tsumohai) or \
                    ((not player.reach)and\
                    self.number != None):
                for button_name in self.button_names:
                    self.textbox_manager.del_button(button_name)
                self.world.process()
                break

            for event in events:
                if event.type == SDL_QUIT:
                    running = False
                    break
                elif event.type == SDL_MOUSEMOTION:
                    for hai in player.hand.entities:
                        if hai.sprite.y < player.hand_pos[1] - 30:
                            continue
                        elif sprite_mouse_overlap(hai.sprite, event.motion):
                            hai.velocity.vy = -1
                        else:
                            hai.velocity.vy = 1
                elif event.type == SDL_MOUSEBUTTONDOWN:
                    for i, hai in enumerate(player.hand.entities):
                        if sprite_mouse_overlap(hai.sprite, event.button):
                            self.hai = hai.hai
                            self.hai_entity = hai
                            self.number = self.hai.number

#TODO:カンとリーチどっちもできてしまう
                    for button_name in self.button_names:
                        if sprite_mouse_overlap(self.textbox_manager.entity_dict[button_name].sprite, event.button):
                            if button_name == 'reach':
                                self.reach = not self.reach
                            elif button_name == 'kan':
                                self.kan = not self.kan

            SDL_Delay(10)
            self.world.process()

class NakiCommand:
    
    def __init__(self, naki_pattern, textbox_manager, world):
        self.naki_pattern = naki_pattern
        self.textbox_manager = textbox_manager
        self.world = world
        self.button_names = list()
        self.buttons = list()

        for pattern in naki_pattern:
            self.textbox_manager.make_button(pattern)
            self.button_names.append(pattern)
            self.buttons.append(self.textbox_manager.entity_dict[pattern])
        self.world.process()

        while True:
            events = sdl2ext.get_events()
            for event in events:
                if event.type == SDL_QUIT:
                    running = False
                    break
                elif event.type == SDL_MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if sprite_mouse_overlap(button.sprite, event.button):
                            self.command = button.textbox.name
                            break
                    else:
                        self.command = None
                    for button_name in self.button_names:
                        self.textbox_manager.del_button(button_name)
                    world.process()

                    return

            SDL_Delay(10)
            world.process()


class Field:

    def __init__(self):
        
        sdl2ext.init()
        self.window = sdl2ext.Window("Souhatsu", size=(800, 600))
        self.window.show()
#        self.world = sdl2ext.World()
        self.world = World()
        self.movement = MovementSystem(0, 0, 800, 600)
        self.spriterenderer = SoftwareRenderer(self.window)

        self.world.add_system(self.movement)
        self.world.add_system(self.spriterenderer)
        self.factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)

        self.textbox_manager = TextBoxManager(self.world, self.factory)


    def start(self):
        self.yourplayer = Player("You", 'down')
        self.op_player= Player("OP", 'up')
        self.yourplayer.set_next(self.op_player)
        self.op_player.set_next(self.yourplayer)
        self.previous_winner = None

        self.turn = int()
        while self.onesession():
            
            # 点数表示のタイミングと変更のタイミングを考える
            self.textbox_manager.make_ten_box('my_ten_board', self.yourplayer.score)
            self.textbox_manager.make_ten_box('op_ten_board', self.op_player.score)

            self.movement.hais = []
            self.whos_turn = SouhatsuEnums.Kaze.valueOf("oya")
            self.who_priority()
            self.deck = Deck()
#            self.yourplayer.make_hand(
#                    Hand(
#                        self.deck,
#                        self.yourplayer,
#                        self.world,
#                        self.factory,
#                        self.movement
#                        )
#                    )
#            self.op_player.make_hand(
#                    Hand(
#                        self.deck,
#                        self.op_player,
#                        self.world,
#                        self.factory,
#                        self.movement,
#                        initnum=7
#                        )
#                    )
            self.yourplayer.make_hand(Hand(self.deck, self.yourplayer, self.world, self.factory, self.movement, test = [2,3,4,6,6,9,9,9]))
            self.op_player.make_hand(Hand(self.deck, self.op_player, self.world, self.factory, self.movement, initnum=7, test = [2,2,10,4,4,6,10]))
            self.movement.hais += self.yourplayer.hand.entities
            self.movement.hais += self.op_player.hand.entities
            
            self.turn = 1

            self.world.process()
            while self.oneturn():

                self.world.process()
                pass
            print("HAIPAI!!\n")
#            del_allにまとめる
            self.textbox_manager.del_button('op_ten_board')
            self.textbox_manager.del_button('my_ten_board')
            self.world.del_all()
            self.world.process()

    def who_priority(self):

        if self.previous_winner != None:
            #前の親がいる時
            self.nextplayer = self.previous_winner
            if self.nextplayer == self.yourplayer:
                self.thisplayer = self.op_player
            else:
                self.thisplayer = self.yourplayer
            self.thisplayer.kaze = SouhatsuEnums.Kaze.valueOf("ko")
            self.nextplayer.kaze = SouhatsuEnums.Kaze.valueOf("oya")
        else:
            self.yourplayer.kaze = SouhatsuEnums.Kaze.valueOf("oya")
            self.op_player.kaze = SouhatsuEnums.Kaze.valueOf("ko")
            self.thisplayer = self.op_player
            self.nextplayer = self.yourplayer

    def onesession(self):
        if self.yourplayer.score < 0 \
                or self.op_player.score < 0:
            return False
        return True


    def oneturn(self): 
        def tsumo_phase():
            pass

        def hora_process(hora_player):
            horaed_player = hora_player.next
            hora_player.hand.machi_type_check()
            hora_player.hand.yaku_check(hora_player)
            hora_player.hand.fu_check()
            hora_player.hand.ten_check()
            #hand.hora_process とhora_processは違う change this
            hora_player.hand.hora_process(hora_player)
            score_board.make_score_board(
                    self.window,
                    [yaku.enname for yaku in hora_player.hand.yaku],
                    hora_player.hand.fu,
                    hora_player.hand.hansu,
                    hora_player.hand.ten
                    )
            self.previous_winner = hora_player
            hora_player.score += hora_player.hand.ten
            horaed_player.score -= hora_player.hand.ten
            print("player score : " + str(hora_player.score))

        def hora_check_phase(player):

            if player.hand.hora_flag(
                    player.hand.contents,
                    player.hand.hand[-1],
                    False
                    ) and \
                    player.naki_status in [None,'kan']:
                print("You Tsumo?")
                self.textbox_manager.make_button('tsumo')
                while True:

                    events = sdl2ext.get_events()
                    for event in events:
                        if event.type == SDL_QUIT:
                            running = False
                            return
                        elif event.type == SDL_MOUSEBUTTONDOWN:
                            if sprite_mouse_overlap(self.textbox_manager.entity_dict['tsumo'].sprite, event.button):

                                player.hand.agarihai = player.hand.tsumohai
                                #TODO:上がりはいが-1の時はこれでいいのか。いつ起こる。とりあえずここで止める
                                if player.hand.agarihai == -1:
                                    input()
                                    player.hand.agarihai = player.hand.hand[0]
                                hora_process(player)
                                self.textbox_manager.del_button('tsumo')
                                return True
                            else:
                                self.textbox_manager.del_button('tsumo')
                                return False


            else:
                return False

        def naki_process(cmd, naki_pattern):
            entity = self.thisplayer.sutehai_entity
            if cmd not in naki_pattern:
                return None
            elif cmd == "pon":
                self.nextplayer.hand.pon(entity)
            elif cmd == "kan":
                self.nextplayer.hand.daiminkan(entity, self.deck)
                self.nextplayer.rinshan = True

            elif cmd == "ron":
                self.nextplayer.hand.ron(entity)
            return cmd

        def naki_phase():
            naki_pattern = self.nextplayer.hand.nakipattern(self.thisplayer.sutehai)
            if naki_pattern != []:
                print("\n\n\n\n" + self.nextplayer.name)
                print("sutehai:", self.thisplayer.sutehai.hainame)
                print("naki_pattern:",end='')
                print(naki_pattern)
                self.nextplayer.hand.show_hand()
                if self.thisplayer.name == "You":
#                    command = str(input())
                    command = NakiCommand(
                            naki_pattern,
                            self.textbox_manager,
                            self.world
                            )
                    command = command.command
                else:
#                    command = str(input())
                    command = NakiCommand(
                            naki_pattern,
                            self.textbox_manager,
                            self.world
                            )
                    command = command.command
                print(command)
                naki_option = naki_process(
                        command,
                        naki_pattern
                        )
                print(naki_option)
                #playerhandに処理をする(naki_optionがNoneかチェックもする)
                if naki_option == 'ron':
                    print(self.nextplayer.hand.ronhai)
                    hora_process(self.nextplayer)
                    return False
                elif naki_option != None:
                    self.nextplayer.naki_status = naki_option
                    self.thisplayer.ippatsu_flag = False
                else:
                    self.nextplayer.naki_status = None
                    self.nextplayer.tsumo = True
            return True


        def trash_phase(player, deck):
            if player.name == "You":
                print("PUT COMMAND")
#                command = Command(str(input()), player)
                command = Command(
                        None,
                        player,
                        player.river,
                        gui = True,
                        textbox_manager = self.textbox_manager,
                        world = self.world
                        )
                #gui command.stateはguiの場合常にTrue
                while not command.state:
                    command = Command(str(input()), player)
                if command.reach == True:
                    if self.turn == 1:
                        player.double_reach = True
                    player.reach = True
                    player.ippatsu_flag = True
                    player.reach_move(
                            self.factory,
                            self.world
                            )
                else: 
                    player.ippatsu_flag = False
                if command.kan == True:
                    player.rinshan = True
                    player.hand.ankan(command.number, deck)
                    if hora_check_phase(player):
                        return False
                    player.rinshan = False
                    trash_phase(player, deck)
                    return True
                else:
                    command.hai_entity.move(player.river_pos[0] \
                            + len(player.river) * 41,
                            player.river_pos[1])
                    player.hand.entities.remove(command.hai_entity)
                    player.river_entities.append(command.hai_entity)
                    player.hand.rihai_move()
                    player.sutehai_entity = command.hai_entity
                    player.sutehai = command.hai
                    self.world.process()

            else:
                player.sutehai_entity = player.hand.entities[0]
                player.sutehai = player.hand.hand[0]
                #TODO:ここ関数か
                player.hand.entities[0].move(player.river_pos[0] + len(player.river) * 41, player.river_pos[1])
                player.hand.entities.remove(player.hand.entities[0])
                for j in range(0,len(player.hand.entities)):
                    player.hand.entities[j].move(player.hand.entities[j].sprite.x - 41 , player.hand_pos[1])
                self.world.process()
                #TODO:ここまで

            player.hand.tsumohai = -1
            player.river.append(player.sutehai)
            player.hand.trash(player.sutehai)
            #川に切る処理

            player.naki_status = None
            return True

        def ryukyoku_check(deck):
            if deck.deck == []:
                return True

        def ryukyoku_process():
            #親を変える
            #罰符
            if self.yourplayer.kaze.enname == 'oya':
                self.previous_winner = self.op_player
            else:
                self.previous_winner = self.yourplayer


        #playerの更新
        player = self.nextplayer
        self.nextplayer, self.thisplayer = self.thisplayer, self.nextplayer
        #この時,self.thisplayer = player
        #以下playerがplayする
        #鳴きなどはself.nextplayerがする

        #tsumo
        if len(player.hand.hand) in [1,4,7]:
            player.hand.tsumo(self.deck)

        self.show_field()

        if hora_check_phase(player):
            return False

        if not trash_phase(player, self.deck):
            #嶺上開花の時のみ終わる
            return False

        if not naki_phase():
            return False
        #鳴き、ロンの処理naki_phaseはronの時False

        if ryukyoku_check(self.deck):
            ryukyoku_process()
            return False

        player.tenhou_flag = False
        player.chihou_flag = False
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

if __name__ == "__main__":
    field = Field()

    while True:
        field.start()


