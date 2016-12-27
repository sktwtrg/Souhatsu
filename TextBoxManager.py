from sdl2 import *
import sdl2.ext as sdl2ext
import SouhatsuEnums
from PIL import Image
from sdl2systems import *

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
        button = SouhatsuEnums.TextBox.valueOf(button_name)
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

