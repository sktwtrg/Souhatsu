from sdl2 import *
import sdl2.ext as sdl2ext
import PIL
import numpy

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

def draw_text(img, text, x, y, textsize = 32):
    draw = PIL.ImageDraw.Draw(img)
    draw.font = PIL.ImageFont.truetype("./Fonts/hiraginoM.ttc", textsize)
    img_size = numpy.array(img.size)
    txt_size = numpy.array(draw.font.getsize(text))
    pos = (img_size - txt_size) / 2
    pos[0] = x
    pos[1] = y

    draw.text(pos, text, (255, 255, 255))


def sprite_mouse_overlap(sprite, mouse):
    left, top, right, bottom = sprite.area
    mx = mouse.x
    my = mouse.y
    print('overlap_test',end='')
    print(left,mx,right,top,my,bottom)
    return left < mx < right and top < my< bottom

def make_entity(img_path, size, world, factory, movement):
    img_pil = Image.open(img_path)
    img_pil = img_pil.resize(size)
    img_surface = pilSurface(img_pil)
    entity = SouhatsuEnums.HaiEntity(world,
            factory.from_surface(img_surface.contents),
            temp_tsumohai,
            player.hand_pos[0] + 41 * (len(player.hand.hand) - 1),
            player.hand_pos[1]
            )
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

class Velocity:

    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0

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

class SoftwareRenderer(sdl2ext.SoftwareSpriteRenderSystem):

    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2ext.fill(self.surface, sdl2ext.Color(50, 100, 50))
        rect_tes1 = rect.SDL_Rect(0,0,800,600)
        super(SoftwareRenderer, self).render(components)

