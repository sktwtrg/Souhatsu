import math
import souhatsu
from hand import Hand
from block import Block
from souhatsu_enums import Hai, Yaku, Kaze

class HandAnalyzer:

    def __init__(self):
        pass

    def analyze(self):
        self.mentsu = []
        self.hansu = int()
        self.fu = int()
        self.ten = int()
        self.yaku_list = []

    def machi_type_check(self, hand):
        #TODO:描き方変？
        #agarihaiいつセットされるか問題 head問題
        # hand.mentsu それぞれのタイプがsetされてる必要あり
        # hand.agarihai がsetされてる必要性
        machi_type_candidate = []
        machi_type = ''
        if hand.mentsu[0].type == 'chitoitsu':
            machi_type_candidate.append('tanki')
            machi_type= 'tanki'
        elif hand.agarihai.number in hand.head.numbers:
            machi_type_candidate.append('tanki')
            machi_type= 'tanki'

        for block in hand.mentsu:
            if block.type in ['minko','daiminkan']:
                pass
            if block.type == 'shuntsu':
                if hand.agarihai.number == block.numbers[1]:
                    machi_type_candidate.append('kanchan')
                    machi_type= 'kanchan'
                elif (block.numbers[0] == 1 and hand.agarihai.number == 3)\
                        or (block.numbers[2] == 9 and hand.agarihai.number == 7):
                    machi_type_candidate.append('penchan')
                    machi_type= 'penchan'
                elif hand.agarihai.number in block.numbers:
                    machi_type_candidate.append('ryanmen')
                    machi_type = 'ryanmen'
            elif hand.agarihai.number in block.numbers:
                machi_type_candidate.append('shabo')
                machi_type = 'shabo'
        return (machi_type_candidate, machi_type)

    def yaku_check(self, hand, player):
        # hand.head, hand.ronhai, hand.mentsu, hand.machi_type_candidateなどが必要
        # なので、analyzerでmachi_type や hora_flagで計算後setの必要
        # 特にmachi_typeが重要
        # hand.yaku, hand.fu, hand.hansuの変更を行わず、返す
        yaku_list = []
        hansu = 0
        fu = 0

        def double_reach(player):
            if player.double_reach == True:
                yaku_list.append(Yaku.valueOf("double_reach"))

        def reach(player):
            if player.reach == True and \
                    player.double_reach == False:
                yaku_list.append(Yaku.valueOf("reach"))

        def yakuhai():
            if hand.contents[0] == 3:
                yaku_list.append(Yaku.valueOf("yaku"))
            for block in hand.furo:
                if 0 in block.numbers:
                    yaku_list.append(Yaku.valueOf("yaku"))

        def tannyao():
            if hand.contents[0] == 0 \
                    and hand.contents[1] == 0 \
                    and hand.contents[9] == 0:
                pass
            else:
                return
            for block in hand.furo:
                if 0 in block.numbers or\
                        1 in block.numbers or\
                        9 in block.numbers:
                    return
            else:
                yaku_list.append(Yaku.valueOf("tannyao"))


        def pinfu():
            if not hand.mensen:
                return

            if 'ryanmen' not in hand.machi_type_candidate:
                return
            for block in hand.mentsu:
                if block.fu != 0:
                    return
            if hand.head.fu != 0:
                return
            yaku_list.append(Yaku.valueOf("pinfu"))

            if hand.ronhai.number == -1:
                fu = 20

        def tsumo():
            if hand.ronhai.number == -1 \
                    and hand.mensen:
                yaku_list.append(Yaku.valueOf("tsumo"))

        def ippatsu(player):
            if player.ippatsu_flag == True:
                yaku_list.append(Yaku.valueOf("ippatsu"))

        def chitoitsu():
            if hand.mentsu[0].type == 'chitoitsu':
                yaku_list.append(Yaku.valueOf("chitoitsu"))
                fu = 25

        def rinshan(player):
            if player.rinshan == True:
                yaku_list.append(Yaku.valueOf("rinshan"))

        def ryuiso():
            for hai in hand.hand:
                if not hai.is_ryuhai:
                    break
            else:
                yaku_list.append(Yaku.valueOf("ryuiso"))

        def tenhou(player):
            if player.tenhou_flag:
                yaku_list.append(Yaku.valueOf("tenhou"))

        def chihou(player):
            if player.chihou_flag and\
                    hand.ronhai.number == -1:
                yaku_list.append(Yaku.valueOf("chihou"))

        def renhou(player):
            if player.chihou_flag and\
                    hand.ronhai.number != -1:
                yaku_list.append(Yaku.valueOf("renhou"))

        def toitoihou():
            for block in hand.mentsu:
                if block.type not in ('minko', 'anko', 'ankan', 'daiminkan'):
                    return
            yaku_list.append(Yaku.valueOf("toitoihou"))

        def ryananko():
            for block in hand.mentsu:
                if block.type not in ('anko', 'ankan'):
                    return
            yaku_list.append(Yaku.valueOf("ryananko"))

        def ipeiko():
            #TODO:未実装、必要？
            return

        def chanta_etc():
            if hand.mentsu[0].type == 'chitoitsu':
                return

            for block in hand.mentsu:
                if not (block.type in ('anko', 'minko', 'ankan', 'minkan')\
                        and block.numbers[0] in (0,1,9)):
                    break
            else:
                if hand.head.numbers[0]in (0,1,9):
                    yaku_list.append(Yaku.valueOf("honroutou"))
                    return

            for block in hand.mentsu:
                if block.numbers[0] != 1 and\
                        block.numbers[2] != 9:
                    break
            else:
                if hand.head.numbers[0]in (1,9):
                    yaku_list.append(Yaku.valueOf("junchan"))
                    return

            for block in hand.mentsu:
                if block.numbers[0] not in (0,1) and\
                        block.numbers[2] != 9:
                    break
            else:
                if hand.head.numbers[0]in (0,1,9):
                    yaku_list.append(Yaku.valueOf("chanta"))
                    return



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

        for yaku in yaku_list:
            hansu += yaku.hansu
        return(yaku_list, hansu, fu)

    def fu_check(self, hand):
        if hand.fu in (20,25):
            return hand.fu
        if hand.ronhai.number == -1:
            fu = 22
        elif hand.mensen:
            fu = 30
        else:
            fu = 20

        for block in hand.mentsu:
            fu += block.fu

        fu += hand.head.fu

        if hand.machi_type_candidate[0] in ['penchan', 'kanchan', 'tanki']:
            fu += 2
        fu = int(10 * math.ceil(float(fu) * 0.1))
        return fu

    def ten_check(self, hand, player):
        #ハネマン以上
        kaze = player.kaze
        if hand.hansu >= 6:
            if hand.hansu in (6,7):
                ten = 12000
            elif hand.hansu in (8,9,10):
                ten = 16000
            elif hand.hansu in (11,12):
                ten = 24000
            else:
                ten = 32000
            if kaze.enname == 'oya':
                ten = int(1.5 * ten)
                if hand.ronhai.number == -1:
                    ten = int(2.0 * ten / 3)
            elif hand.ronhai.number == -1:
                ten = int(3.0 * ten / 4)
            return ten

        #満貫以下
        if kaze.enname == 'ko':
            ten = int(100 * math.ceil(0.01 * hand.fu * 4 * float(pow(2, 2 + hand.hansu))))
            if ten >= 8000:
                ten = 8000
        elif kaze.enname == 'oya':
            ten = int(100 * math.ceil(0.01 * hand.fu * 6 * float(pow(2, 2 + hand.hansu))))
            if ten >= 12000:
                ten = 12000

        if hand.ronhai.number != -1:
            ten = int(1000 * math.ceil(0.001 * float(ten)))
        else:
            if kaze.enname == 'ko':
                ten = int(1000 * math.ceil(0.001 * (float(ten)/4))) + int(1000 * math.ceil(0.001 * (float(ten)/2)))
            elif kaze.enname == 'oya':
                ten = int(1000 * math.ceil(0.001 * (float(ten)/3))) * 2
        return ten


    @staticmethod
    def chitoitsu_check(contents):
        toitsu_num = 0
        for num in contents:
            if num == 2:
                toitsu_num += 1
            if toitsu_num == 4:
                return True

    def mentsu_check(self, check_contents, ronhai, count, mentsu_list):
        mentsu_hais = []
        if check_contents[0] >= 3:
            check_contents[0] -= 3
            for x in range(3):
                mentsu_hais.append(
                        Hai.valueAt(0)
                        )
            if ronhai.number == 0:
                mentsu_list.append(
                        Block(
                            mentsu_hais,
                            block_type = "minko"
                            )
                        )
            else:
                mentsu_list.append(
                        Block(
                            mentsu_hais,
                            block_type = "anko"
                            )
                        )
            #発面子を抜いて面子チェック
            if self.mentsu_check(check_contents, ronhai, count+1, mentsu_list):
                return mentsu_list
            del mentsu_list[-1]

        for i in range(1,10):
            if check_contents[i] >= 3:
                check_contents[i] -= 3
                for x in range(3):
                    mentsu_hais.append(Hai.valueAt(i))
                if ronhai.number == i:
                    mentsu_list.append(
                            Block(
                                mentsu_hais,
                                block_type = "minko"
                                )
                            )
                else:
                    mentsu_list.append(
                            Block(
                                mentsu_hais,
                                block_type = "anko"
                                )
                            )
                if self.mentsu_check(check_contents, ronhai, count+1, mentsu_list):
                    return mentsu_list
                del mentsu_list[-1]
            #8,9,10の順子は存在しないのでcontinue
            elif i >= 8:
                continue
            elif check_contents[i] > 0 and check_contents[i+1] > 0 and check_contents[i+2] > 0:
                for x in range(3):
                    check_contents[i + x] -= 1
                    mentsu_hais.append(Hai.valueAt(i + x))
                mentsu_list.append(Block(mentsu_hais, block_type = "shuntsu"))
                #順子を抜いて面子チェック
                if self.mentsu_check(check_contents, ronhai, count+1, mentsu_list):
                    return mentsu_list
                del mentsu_list[-1]
        else:
            return False

    def hora_flag(self, contents, ronhai=Hai.valueAt(-1), furo=[]):
        #contents, ronhai, furo を破壊しないはず。。
        #mentsu_list_funcは上がってない場合Falseを返す
        mentsu_list = []
        if self.chitoitsu_check(contents):
            block = Block([Hai.valueAt(0)], block_type = "chitoitsu")
            mentsu_list.append(block)
            head = Block([Hai.valueAt(0)], block_type = "head")
            return (head, mentsu_list)

        for i, number in enumerate(contents):
            contents_check = contents[:]
            if contents_check[i] >= 2:
                contents_check[i] -= 2
                head = Block([Hai.valueAt(i)]*2, block_type = "head")
                #一つ目の面子チェック
                self.mentsu_check(contents_check, ronhai, 0, mentsu_list)
                if mentsu_list:
                    mentsu_list += furo
                    return (head, mentsu_list)
        else:
            return False

    def tenpai_flag(self, contents):
        #contents, ronhai, furo を破壊しないはず。。
        contents = contents[:]
        matinums = {}
        if sum(contents) in set((2, 5, 8)):
            for i in range(10):
                if contents[i] > 0:
                    contents[i] -= 1
                else:
                    continue
                for j in range(10):
                    contents[j] += 1
                    if self.hora_flag(contents):
                        if i not in matinums:
                            matinums[i] = []
                        matinums[i].append(j)
                    contents[j] -= 1
                contents[i] += 1
            if matinums != {}:
                return matinums
            return False

        for i in range(10):
            contents[i] += 1
            if self.hora_flag(contents):
                if None not in matinums:
                    matinums[None] = []
                matinums[None].append(i)
            contents[i] -= 1
        if matinums != {}:
            return matinums
        return False

    def naki_candidates(self, hand, player, hai):
        def pon_check(hai):
            return (not player.reach) and hand.contents[hai.number] >= 2
        def kan_check(hai):
            return (not player.reach) and hand.contents[hai.number] >= 3
        def ron_check(hai):
            check_contents = hand.contents[:]
            check_contents[hai.number] += 1
            return self.hora_flag(check_contents, hai, hand.furo)
        naki_candidates = []
        if pon_check(hai): naki_candidates.append("pon")
        if kan_check(hai): naki_candidates.append("kan")
        if ron_check(hai): naki_candidates.append("ron")
        return naki_candidates

if __name__ == "__main__":
    deck = souhatsu.Deck()
    player = souhatsu.Player('aaa')
    a = HandAnalyzer()
    #TODO player.make_hand player.kaze変
    #和了でない例
    hand = Hand(deck, test=[0,0,0,0,2,3,8,9])
    hand.show_hand()
    print('テンパイ')
    print(a.tenpai_flag(hand.contents))
    print('和了')
    print(a.hora_flag(hand.contents, hand.ronhai, hand.furo))
    print()

    #和了例
    hand = Hand(deck, player, test=[0,0,0,1,1,1,2,2])
    hand.show_hand()
    print('テンパイ')
    print(a.tenpai_flag(hand.contents))
    print('和了')
    print(a.hora_flag(hand.contents, hand.ronhai, hand.furo))
    print()

    #テンパイ例
    hand = Hand(deck, player, test=[0,0,0,1,1,1,1,2])
    hand.show_hand()
    player.kaze = Kaze.valueOf("oya")
    player.make_hand(hand)
    print('テンパイ')
    print(a.tenpai_flag(hand.contents))
    print('和了')
    print(a.hora_flag(hand.contents, hand.ronhai, hand.furo))

    #テンパイ例
    hand = Hand(deck, player, test=[0,0,0,1,1,1,2])
    hand.show_hand()
    player.kaze = Kaze.valueOf("oya")
    player.make_hand(hand)
    print('テンパイ')
    print(a.tenpai_flag(hand.contents))
    print('和了')
    print(a.hora_flag(hand.contents, hand.ronhai, hand.furo))

    #鳴きチェック
    print('鳴き')
    hand.trash(Hai.valueAt(2))
    print(a.naki_candidates(hand,
            player,
            Hai.valueAt(0)))
    print()

    #点数チェック
    hand = Hand(deck, player, test=[0,0,0,1,1,1,2,3])
    player.kaze = Kaze.valueOf("oya")
    player.make_hand(hand)
    hand.show_hand()
    hand.head, hand.mentsu = a.hora_flag(hand.contents, hand.ronhai, hand.furo)
    print("aaa")
    print(type(hand.head))
    hand.agarihai = Hai.valueAt(1)
    hand.machi_type_candidate, hand.machi_type = a.machi_type_check(hand)
    hand.yaku, hand.hansu ,hand.fu = a.yaku_check(hand, player)
    hand.fu = a.fu_check(hand)
    hand.ten = a.ten_check(hand, player)
    print(hand.ten)


