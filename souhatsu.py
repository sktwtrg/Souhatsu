import random
import math
from enum import Enum
from PIL import Image
from sdl2 import *
import sdl2.ext as sdl2ext

buf = []
def pilSurface(img):
  buf.append(img.tobytes())
  return SDL_CreateRGBSurfaceFrom(
    buf[-1], img.size[0], img.size[1],
    8 * len(img.mode), img.size[0] * len(img.mode),
    0x000000ff,
    0x0000ff00,
    0x00ff0000,
    0xff000000)

def sprite_mouse_overlap(sprite, mouse):
    left, top, right, bottom = sprite.area
    mx = mouse.x
    my = mouse.y
    return left < mx < right and top < my< bottom

def MakeEntity():
    img_pil = Image.open(img_path)
    img_pil = img_pil.resize(size)
    img_surface = pilSurface(img_pil)
    entity = HaiEntity(world, factory.from_surface(img_surface.contents), temp_tsumohai, player.hand_pos[0] + 41 * (len(player.hand.hand) - 1), player.hand_pos[1])
    self.movement.hais.append(entity) 
    player.hand.entities.append(entity)
    world.process()

class World(sdl2ext.World):

    def __init__(self):
        super(World, self).__init__()
        self.hai_entities = list()

    def del_all(self):
        self.delete_entities(self.hai_entities)
        self.hai_entities = list()

class MovementSystem(sdl2ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = (Velocity, sdl2ext.Sprite)
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.hais = []

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size
            sprite.x += velocity.vx
            sprite.y += velocity.vy

            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)

            pmaxx = sprite.x + swidth
            pmaxy = sprite.y + sheight
            if pmaxx > self.maxx:
                sprite.x = self.maxx - swidth
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight

            #TODO:位置情報を変数化
            for hai in self.hais:
                if hai.sprite.y < 400 - 30:
                    hai.velocity.vy = 0
                    continue
                elif hai.sprite.y < 400 - 8:
                    hai.velocity.vy = 0
                    hai.sprite.y += 1
                elif hai.sprite.y > 400:
                    hai.velocity.vy = 0
                    hai.sprite.y -= 1
#
class Velocity:

    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0


class SoftwareRenderer(sdl2ext.SoftwareSpriteRenderSystem):

    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2ext.fill(self.surface, sdl2ext.Color(50, 100, 50))
        rect_tes1 = rect.SDL_Rect(0,0,800,600)
        super(SoftwareRenderer, self).render(components)

class TextBoxEntity(sdl2ext.Entity):

    def __init__(self, world, sprite, textbox, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.textbox = textbox

class TextBoxManager:

    def __init__(self, world, factory):
        self.world = world
        self.factory = factory
        self.entity_dict = dict()

    def make_button(self, button_name, size = None, position = None):
        #TODO: サイズ指定も可能にする
        button = TextBox.valueOf(button_name)
        img_pil = Image.open(button.img_path)
        img_pil = img_pil.resize(button.size)
        img_surface = pilSurface(img_pil)
        entity = TextBoxEntity(
                self.world,
                self.factory.from_surface(
                    img_surface.contents
                    ),
                button,
                button.position[0],
                button.position[1]
                )
        self.entity_dict[button_name]  = entity
        self.world.process()

    def del_button(self, button_name):
        self.world.delete(self.entity_dict[button_name])
        del self.entity_dict[button_name]
        self.world.process()


class HaiEntity(sdl2ext.Entity):

    def __init__(self, world, sprite, hai, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.hai = hai
        self.velocity = Velocity()

    def move(self,x,y):
        self.sprite.x = x
        self.sprite.y = y


class TextBox(Enum):

    TSUMO = ('tsumo', (80, 50), (500, 400), './pai-images/tsumo.png')
    PON = ('pon', (80, 50), (110, 480), './pai-images/pon.png')
    KAN = ('kan', (80, 50), (195, 480), './pai-images/kan.png')
    RON = ('ron', (80, 50), (280, 480), './pai-images/ron.png')

    def __init__(self, _name, _size, _position, _img_path):
        self._name = _name
        self._size = _size
        self._position = _position
        self._img_path = _img_path

    @classmethod
    def valueOf(cls, name):
        for textbox in cls:
            if textbox.name == name:
                return textbox
        return None

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size

    @property
    def position(self):
        return self._position

    @property
    def img_path(self):
        return self._img_path


class Hai(Enum):


    SU1 = (1, 1, '一索', 'yi', './pai-images/sou1-66-90-l-emb.png')
    SU2 = (2, 2, '二索', 'er', './pai-images/sou2-66-90-l-emb.png')
    SU3 = (3, 3, '三索', 'san', './pai-images/sou3-66-90-l-emb.png')
    SU4 = (4, 4, '四索', 'si', './pai-images/sou4-66-90-l-emb.png')
    SU5 = (5, 5, '五索', 'wu', './pai-images/sou5-66-90-l-emb.png')
    SU6 = (6, 6, '六索', 'liu', './pai-images/sou6-66-90-l-emb.png')
    SU7 = (7, 7, '七索', 'qi', './pai-images/sou7-66-90-l-emb.png')
    SU8 = (8, 8, '八索', 'ba', './pai-images/sou8-66-90-l-emb.png')
    SU9 = (9, 9, '九索', 'jiu', './pai-images/sou9-66-90-l-emb.png')
    HATSU = (0, 0, '發', 'fa', './pai-images/ji5-66-90-l.png')
    DS5 = (10, 5, '赤五', 'rw', './pai-images/aka2-66-90-l-emb.png')

    def __init__(self, _id, _number, _hainame, _chiname, _img_path):
        self._id = _id
        self._number = _number
        self._hainame = _hainame
        self._img_path = _img_path

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
    def img_path(self):
        return self._img_path

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



class Hand:

    hai_size = (40, 60)

    def __init__(self, deck, player, world, factory, initnum = 8, test = None):

        self.player = player
        self.world = world
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
            self.tsumohai = -1
            for j, hai in enumerate(self.hand):
                img_pil = Image.open(hai.img_path)
                img_pil = img_pil.resize(self.hai_size)
                img_surface = pilSurface(img_pil)
                entity = HaiEntity(world, factory.from_surface(img_surface.contents), hai, self.player.hand_pos[0] + 41 * j, self.player.hand_pos[1])
                self.entities.append(entity)
                self.world.hai_entities.append(entity)
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

    def machi_type_check(self):
        if self.agarihai.number in self.head.numbers:
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
        def reach(player):
            if player.reach == True:
                self.yaku.append(Yaku.valueOf("reach"))

        def yakuhai():
            if self.contents[0] == 3:
                self.yaku.append(Yaku.valueOf("yaku"))
            for block in self.furo:
                if 0 in block.numbers:
                    self.yaku.append(Yaku.valueOf("yaku"))

        def tannyao():
            if self.contents[0] == 0 \
                    and self.contents[1] == 0 \
                    and self.contents[9] == 0\
                    and self.furo == []:
                self.yaku.append(Yaku.valueOf("tannyao"))

        def pinfu():
            for block in mentsu:
                pass

        def tsumo():
            if self.ronhai == -1 \
                    and self.furo == []:
                self.yaku.append(Yaku.valueOf("tsumo"))

        def ippatsu(player):
            if player.ippatsu_flag == True:
                self.yaku.append(Yaku.valueOf("ippatsu"))

        def chitoitsu():
            if self.mentsu[0] == 'chitoitsu':
                self.yaku.append(Yaku.valueOf("chitoitsu"))

        def rinshan(player):
            if player.rinshan == True:
                self.yaku.append(Yaku.valueOf("rinshan"))

        hand = list(self.hand)
        reach(player)
        yakuhai()
        tannyao()
        tsumo()
        ippatsu(player)
        chitoitsu()
        rinshan(player)

        for yaku in self.yaku:
            self.hansu += yaku.hansu

    def fu_check(self):
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
        self.ten = int(self.fu * 4 * 100 * math.ceil(float(pow(2, 2 + self.hansu))  * 0.01))
        self.ten = int(100 * math.ceil(0.01 * self.fu * 4 * float(pow(2, 2 + self.hansu))))


    def hora_process(self,player):
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

    def hora_flag(self,contents):
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
                mentsu_hais.append(Hai.valueAt(0))
                mentsu_hais.append(Hai.valueAt(0))
                mentsu_hais.append(Hai.valueAt(0))
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
                    #順子を抜いて面子チェック
                    if mentsu_check(check_contents, count+1):
                        return True
                    del self.mentsu[-1]
            else:
                return False

#        print(contents)
        if chitoitsu_check(contents):
            #TODO:change this
            self.mentsu.append("chitoitsu")
            return True

        for i, number in enumerate(contents):
            contents_check = list(contents)[:]
            if contents_check[i] >= 2:
                contents_check[i] -= 2
                self.head = Block([Hai.valueAt(i)]*2, block_type = "head")
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

    def tsumo(self, deck, world):
        self.tsumohai = deck.draw()
        self.hand.append(self.tsumohai)
        self.contents[self.tsumohai.number] += 1
        return self.tsumohai
        
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
        print(block_hais)
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
        for i in range(4):
            for hai in self.hand:
                if hai.number != num:
                    continue
                self.hand.remove(hai)
                block_hais.append(hai)
                break
        self.tsumo(deck)
        block = Block(block_hais, block_type = "ankan")
        self.furo.append(block)
        self.show_hand()

    def ron(self, entity):
        self.ronhai = entity.hai
        self.tsumohai = -1
        self.contents[entity.hai.number] += 1
        self.hand.append(entity.hai)
        self.entities.append(entity)
        self.agarihai = entity.hai

class Deck:

    def __init__(self):
        self.deck = Hai.AllHai()
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
        self.score = int()

        self.player_pos = player_pos
        if player_pos == 'up':
            self.hand_pos = (180, 100)
            self.river_pos = (150, 200)
        if player_pos == 'down':
            self.hand_pos = (120,400)
            self.river_pos = (150,300)

    def make_hand(self, hand):
        self.hand = hand
        self.river = []
        self.river_entities = []
        self.reach = False
        self.tsumo = False
        self.ron = False
        self.rinshan = False
        self.naki_status = None
        self.ippatsu_flag = False


class Command:
    
    def __init__(self, cmd, player, river, gui = False, world = None):
        if gui:
            self.gui_trash_parse(player, river, world)
            return

        if len(cmd) == 0: 
            self.state = False
            return

        if "5r" in cmd:
            self.reach  = False
            self.number = int(5)
            self.kan = False
            self.hai = Hai.valueAt(10)
        elif cmd[-1] in [str(x) for x in range(10)]:
            self.reach = False
            self.number = int(cmd[-1])
            self.kan = False
            self.hai = Hai.valueAt(self.number)
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

    def gui_trash_parse(self, player, river, world):
        self.reach = False
        self.kan = False
        self.state = True
        while True:
            events = sdl2ext.get_events()
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
                            hai.move(player.river_pos[0] + len(river) * 41, player.river_pos[1])
                            self.hai = hai.hai
                            self.hai_entity = hai

                            #TODO:臨時でこう
#                            river.append(1)
                            player.river_entities.append(hai)
                            player.hand.entities.pop(i)

                            for j in range(i,len(player.hand.entities)):
                                player.hand.entities[j].move(player.hand.entities[j].sprite.x - 41 , player.hand_pos[1])
                            world.process()
                            return
            SDL_Delay(10)
            world.process()

class NakiCommand:
    
    def __init__(self, naki_pattern, textbox_manager, world):
        self.naki_pattern = naki_pattern
        self.textbox_manager = textbox_manager
        self.world = world

        for pattern in naki_pattern:
            self.textbox_manager.make_button(pattern)
        self.buttons = self.textbox_manager.entity_dict.values()
        self.button_names = list(self.textbox_manager.entity_dict.keys())
        world.process()

        while True:
            events = sdl2ext.get_events()
            for event in events:
                if event.type == SDL_QUIT:
                    running = False
                    break
                elif event.type == SDL_MOUSEMOTION:
                    continue

                    #TODO:ちゃんと消す
                    for hai in player.hand.entities:
                        if hai.sprite.y < 440:
                            continue
                        elif (hai.sprite.x < event.motion.x < hai.sprite.x + hai.sprite.size[0]) and (hai.sprite.y < event.motion.y < hai.sprite.y + hai.sprite.size[1]):
                            hai.velocity.vy = -1
                        else:
                            hai.velocity.vy = 1
                elif event.type == SDL_MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        print(button)
                        print(button.sprite)
                        if sprite_mouse_overlap(button.sprite, event.button):
                            self.command = button.textbox.name
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
        self.window = sdl2ext.Window("The Pong Game", size=(800, 600))
        self.window.show()
#        self.world = sdl2ext.World()
        self.world = World()
        self.movement = MovementSystem(0, 0, 800, 600)
        self.spriterenderer = SoftwareRenderer(self.window)

        self.world.add_system(self.movement)
        self.world.add_system(self.spriterenderer)
        self.factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)

        self.textbox_manager = TextBoxManager(self.world, self.factory)

        self.yourplayer = Player("You", 'down')
        self.op_player= Player("OP", 'up')
        self.previous_winner = None

    def start(self):
        while self.onesession():
            self.movement.hais = []
            self.deck = Deck()
            self.yourplayer.make_hand(Hand(self.deck, self.yourplayer, self.world, self.factory, test = [2,5,5,10,9,9,9,9]))
            self.op_player.make_hand(Hand(self.deck, self.op_player, self.world, self.factory, initnum=7, test = [2,2,2,4,4,6,5]))
            self.movement.hais += self.yourplayer.hand.entities
            self.movement.hais += self.op_player.hand.entities
            

#            self.textbox_manager.make_button('pon')
#            self.textbox_manager.make_button('ron')
#            self.textbox_manager.make_button('kan')

            self.turn = 1
            self.whos_turn = Kaze.valueOf("oya")
            self.who_priority()

            self.world.process()
            while self.oneturn():
                self.world.process()
                pass
            print("HAIPAI!!\n")
            input()
            self.world.del_all()
            self.world.process()
            input()

    def who_priority(self):

        if self.previous_winner != None:
            #前の親がいない時、
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


    def oneturn(self): 
        def tsumo_phase():
            pass

        def hora_process(player):
            player.hand.machi_type_check()
            player.hand.yaku_check(player)
            player.hand.fu_check()
            player.hand.ten_check()
            player.hand.hora_process(player)
            self.previous_winner = player
            player.score += 1
            print("player score : " + str(player.score))

        def hora_check_phase(player):

            if player.hand.hora_flag(player.hand.contents)\
                    and player.naki_status in [None,'kan']:
                print("You Tsumo?")
                self.textbox_manager.make_button('tsumo')
                while True:

                    events = sdl2ext.get_events()
                    for event in events:
                        if event.type == SDL_QUIT:
                            running = False
                            break
                        elif event.type == SDL_MOUSEBUTTONDOWN:
                            if (self.textbox_manager.entity_dict['tsumo'].sprite.x < event.button.x < self.textbox_manager.entity_dict['tsumo'].sprite.x + self.textbox_manager.entity_dict['tsumo'].sprite.size[0]) and (self.textbox_manager.entity_dict['tsumo'].sprite.y < event.button.y < self.textbox_manager.entity_dict['tsumo'].sprite.y + self.textbox_manager.entity_dict['tsumo'].sprite.size[1]):

                                player.hand.agarihai = player.hand.tsumohai
                                print("")
                                print()
                                hora_process(player)
                                return True
                            else:
                                self.world.delete(self.textbox_manager.entity_dict['tsumo'])
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
            naki_pattern = (self.nextplayer.hand.nakipattern(self.thisplayer.sutehai))
            if naki_pattern != []:
                print("\n\n\n\n" + self.nextplayer.name)
                print("sutehai:", self.thisplayer.sutehai.hainame)
                self.nextplayer.hand.show_hand()
                print(naki_pattern)
                if self.thisplayer.name == "You":
#                    command = str(input())
                    command = NakiCommand(naki_pattern, self.textbox_manager, self.world)
                    command = command.command
                else:
#                    command = str(input())
                    command = NakiCommand(naki_pattern, self.textbox_manager, self.world)
                    command = command.command
                naki_option = naki_process(command, naki_pattern)
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
                command = Command(None, player, player.river, gui = True, world = self.world)
                while not command.state:
#                    command = Command(str(input()), player)
                    command = Command(None, player, gui = True)
                if command.reach == True:
                    player.reach = True
                    player.ippatsu_flag = True
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
                    player.sutehai_entity = command.hai_entity
                    player.sutehai = command.hai

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
            temp_tsumohai = player.hand.tsumo(self.deck, self.world)

            #TODO:ここを関数化
            img_pil = Image.open(temp_tsumohai.img_path)
            img_pil = img_pil.resize(Hand.hai_size)
            img_surface = pilSurface(img_pil)
            entity = HaiEntity(self.world, self.factory.from_surface(img_surface.contents), temp_tsumohai, player.hand_pos[0] + 41 * (len(player.hand.hand) - 1), player.hand_pos[1])
            self.movement.hais.append(entity) 
            player.hand.entities.append(entity)
            self.world.hai_entities.append(entity)
            self.world.process()
            #TODO:ここまでなんとかする

        self.show_field()

        if hora_check_phase(player):
            return False

        if not trash_phase(player, self.deck):
            #嶺上開花の時のみ終わる
            return False

        if not naki_phase():
            return False
        #鳴き、ロンの処理naki_phasaeはronの時False

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

if __name__ == "__main__":
    field = Field()
    field.start()


