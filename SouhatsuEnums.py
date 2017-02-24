from sdl2 import *
import sdl2.ext as sdl2ext
from enum import Enum

from sdl2systems import Velocity, pilSurface
from PIL import Image

class TenbouEntity(sdl2ext.Entity):

    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy



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
    REACH = ('reach', (80, 50), (280, 480), './pai-images/reach.png')
    MY_TEN = ('my_ten_board', (150, 50), (600, 480), './pai-images/pon.png')
    OP_TEN = ('op_ten_board', (150, 50), (600, 180), './pai-images/kan.png')

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
    NONE = (-1, -1, 'None', 'None', './pai-images/ji6-66-90-l.png')

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

#    @property
#    def surface(self):
#        img_pil = Image.open(self.img_path)
#        img_pil = img_pil.resize((40,60))
#        return pilSurface(img_pil)


class Yaku(Enum):

    yakuhai = (0, "役", "yaku", 1)
    reach = (1, "立直", "reach", 1)
    double_reach = (2, "ダブル立直", "double_reach", 2)
    tannyao = (3, "断么九", "tannyao", 1)
    tsumo = (4, "面前自摸和", "tsumo", 1)
    chitoitsu = (5, "七対子", "chitoitsu", 2)
    ippatsu = (6, "一発", "ippatsu", 1)
    rinshan = (7, "嶺上開花", "rinshan", 1)
    pinfu = (8, "平和", "pinfu", 1)
    ryuiso = (9, "緑一色", "ryuiso", 100)
    tenhou = (10, "天和", "tenhou", 100)
    chihou = (11, "地和", "chihou", 100)
    renhou = (12, "人和", "renhou", 4)
    toitoihou = (13, "対々和", "toitoihou", 2)
    ryananko = (14, "二暗刻", "ryananko", 2)
    ipeiko = (15, "一盃口", "ipeiko", 1)
    chanta = (16, "全帯", "chanta", 2)
    junchan = (17, "純全帯", "junchan", 3)

    haitei = (18, "海底撈月", "haitei", 1)
    houtei = (19, "河底撈魚", "houtei", 1)
    honroutou = (20, "混老頭", "honroutou", 2)
    chankan = (21, "槍槓", "chankan", 1)

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

