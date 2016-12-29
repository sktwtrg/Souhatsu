import PIL.ImageDraw
import PIL.ImageFont
from PIL import Image
from sdl2 import *
import sdl2.ext as sdl2ext
from sdl2systems import *
import numpy
import SouhatsuEnums

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

def yaku_img(yaku_name):
    yaku = SouhatsuEnums.Yaku.valueOf(yaku_name)
    img_name = PIL.Image.new("RGBA", (240, 50))
    text = yaku.name
    text = str(yaku.hansu) + '飜'

def print_yaku_list(yaku_names):
    img = PIL.Image.new("RGBA", (320, 50 * len(yaku_names) + 25))
    for i, yaku_name in enumerate(yaku_names):
        yaku = SouhatsuEnums.Yaku.valueOf(yaku_name)
        text = yaku.name
        draw_text(img, text, 0, 50 * i + 25)
        if yaku.hansu > 0:
            text = str(yaku.hansu) + '飜'
        if yaku.hansu >= 100:
            text = '役満'
        draw_text(img, text, 200, 50 * i + 25)
    return img

def make_score_board(window = None, yaku_list = ['rinshan', 'pinfu'], fusu = 20, hansu = 2 , tensu = 2000):

    if window == None:
        sdl2ext.init()
        window = sdl2ext.Window("The Pong Game", size=(800, 600))
        window.show()

    img = print_yaku_list(yaku_list)

    window_surface = window.get_surface()
    surface = pilSurface(img)
    sdl2ext.fill(window_surface, sdl2ext.Color(0, 0, 0 ))
    rect_tes1 = rect.SDL_Rect(0, 0, 320, 500)
    rect_tes2 = rect.SDL_Rect(25, 0, 800, 600)
    SDL_BlitSurface(surface,rect_tes1,window_surface,rect_tes2)
    SDL_UpdateWindowSurface(window.window)

    rect_tes1 = rect.SDL_Rect(0, 0, 800, 600)
    rect_tes2 = rect.SDL_Rect(25, 550, 800, 600)
    img = PIL.Image.new("RGBA", (500, 35))

    if hansu >= 0:
        text_hansu = str(hansu) + '飜 '
    if hansu >= 13:
        text_hansu = '数え役満 '
    if hansu >= 100:
        text_hansu = '役満 '
    text = str(fusu) + '符 ' + text_hansu + str(tensu) + '点'
    draw_text(img, text, 0, 0)
    surface = pilSurface(img)
    SDL_BlitSurface(surface,
            rect_tes1,
            window_surface,
            rect_tes2)
    SDL_UpdateWindowSurface(window.window)
    while True:

        events = sdl2ext.get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
                break
            elif event.type == SDL_MOUSEBUTTONDOWN:
                return
#make_score_board()
