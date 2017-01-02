import souhatsu
import SouhatsuEnums

class Hand:

    #sizeなど外部か
    hai_size = (40, 60)

    def __init__(self, deck, player, world = None, factory = None, movement = None, initnum = 8, test = None, gui = True):

        self.player = player
        self.hand = list()
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

        self.gui = gui
        self.entities = list()
        self.world = world
        self.factory = factory
        self.movement = movement

        if test != None:
            for i in test:
                self.test_tsumo(i)
            return

        for i in range(initnum):
            self.tsumo(deck)
        return

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
        self.contents[hai.number] -= 1
        self.hand.remove(hai)

    def tsumo(self, deck):
        self.tsumohai = deck.draw()
        self.hand.append(self.tsumohai)
        self.contents[self.tsumohai.number] += 1

        if not self.gui:
            return self.tsumohai
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
        if not self.gui:
            return self.tsumohai

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

    def rihai_move(self):
        if not self.gui:
            return
        for i, entity in enumerate(self.entities):
            entity.move(self.player.hand_pos[0] + (Hand.hai_size[0] + 1) * i, self.player.hand_pos[1])

    def pon(self, hai):
        self.hand.append(hai)
        num = hai.number
        self.contents[num] -= 2
        block_hais = []
        for i in range(3):
            self.hand.remove(hai)
            block_hais.append(hai)

#        self.entities.append(entity)
#        block_entities = []
#        for i in range(3):
#            for entity in self.entities:
#                if entity.hai.number != num:
#                    continue
#                self.entities.remove(entity)
#                block_entities.append(entity)
#                break
        block = souhatsu.Block(block_hais, block_type = "minko")
#        block.set_entities(block_entities)
#        self.pon_move(block_entities)
        self.mensen = False
        self.furo.append(block)
#        self.world.process()

    def pon_move(self, entities):
        position = (self.player.hand_pos[0] + len(self.player.hand.hand) * self.hai_size[0] + 20, self.player.hand_pos[1])
        entities[0].move(position[0], position[1])
        entities[1].move(position[0] + self.hai_size[0], position[1])
        entities[2].move(position[0] + self.hai_size[0] * 2 , position[1])
        self.rihai_move()

    # ツモはせずターンを飛ばして普通のツモをする（ツモはFieldで行う）
    def daiminkan(self, hai, deck):
        self.hand.append(hai)
        num = hai.number
        self.contents[num] -= 3
        block_hais = []
        for i in range(4):
            self.hand.remove(hai)
            block_hais.append(hai)
        block = souhatsu.Block(block_hais, block_type = "daiminkan")
        self.furo.append(block)
        self.mensen = False
        self.show_hand()
#        self.entities.append(entity)
#        block_entities = []
#        for i in range(4):
#            for entity in self.entities:
#                if entity.hai.number != num:
#                    continue
#                self.entities.remove(entity)
#                block_entities.append(entity)
#                break
#        block.set_entities(block_entities)
#        self.daiminkan_move(block_entities)
#        self.world.process()

    def daiminkan_move(self, entities):
        position = (self.player.hand_pos[0] + (len(self.player.hand.hand) + 1) * self.hai_size[0] + 20, self.player.hand_pos[1])
        entities[0].move(position[0], position[1])
        entities[1].move(position[0] + self.hai_size[0], position[1])
        entities[2].move(position[0] + self.hai_size[0] * 2 , position[1])
        entities[3].move(position[0] + self.hai_size[0] * 3 , position[1])
        self.rihai_move()

    def ankan(self, hai, deck):
        num = hai.number
        self.contents[num] -= 4
        block_hais = []
        block_entities = []
        for i in range(4):
            self.hand.remove(hai)
            block_hais.append(hai)
        self.tsumo(deck)
        block = souhatsu.Block(block_hais, block_type = "ankan")
        self.furo.append(block)
        self.show_hand()
#        for i in range(4):
#            for entity in self.entities:
#                if entity.hai.number != num:
#                    continue
#                self.entities.remove(entity)
#                block_entities.append(entity)
#                break
#        block.set_entities(block_entities)
#        self.ankan_move(block_entities)
#        self.world.process()

    def ankan_move(self, entities):
        position = (self.player.hand_pos[0] + (len(self.player.hand.hand) + 1) * self.hai_size[0] + 20, self.player.hand_pos[1])
        entities[0].move(position[0], position[1])
        entities[1].move(position[0] + self.hai_size[0], position[1])
        entities[2].move(position[0] + self.hai_size[0] * 2 , position[1])
        entities[3].move(position[0] + self.hai_size[0] * 3 , position[1])
        self.rihai_move()

    #ron後 hora処理
    def ron(self, hai):
        self.ronhai = hai
        self.tsumohai = -1
        self.contents[hai.number] += 1
        self.hand.append(hai)
        self.agarihai = hai

if __name__ == "__main__":
    deck = souhatsu.Deck()
    player = souhatsu.Player('aaa')
    hand = Hand(deck, player, test=[0,0,0,1,1,1,1,2], gui=False)
    hand.show_hand()
