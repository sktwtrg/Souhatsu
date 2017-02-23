import souhatsu
from hand import Hand
import SouhatsuEnums
from souhatsu import Block

class HandAnalyzer:

    def __init__(self):
        pass

    def analyze(self):
        self.mentsu = []
        self.hansu = int()
        self.fu = int()
        self.ten = int()
        self.yaku_list = []
        self.head = int()
        self.machi_type= ''
        self.machi_type_candidate = []

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

    def yaku_check(self, hand):
        # hand.head, hand.ronhai, hand.mentsu, hand.machi_type_candidateなどが必要
        # なので、analyzerでmachi_type や hora_flagで計算後setの必要
        # hand.yaku, hand.fu, hand.hansuの変更を行わず、返す
        yaku_list = []
        hansu = 0
        fu = 0

        def double_reach(player):
            if player.double_reach == True:
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("double_reach"))

        def reach(player):
            if player.reach == True and \
                    player.double_reach == False:
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("reach"))

        def yakuhai():
            if hand.contents[0] == 3:
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("yaku"))
            for block in hand.furo:
                if 0 in block.numbers:
                    yaku_list.append(SouhatsuEnums.Yaku.valueOf("yaku"))

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
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("tannyao"))


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
            yaku_list.append(SouhatsuEnums.Yaku.valueOf("pinfu"))

            if hand.ronhai == -1:
                fu = 20

        def tsumo():
            if hand.ronhai == -1 \
                    and hand.mensen:
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("tsumo"))

        def ippatsu(player):
            if player.ippatsu_flag == True:
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("ippatsu"))

        def chitoitsu():
            if hand.mentsu[0].type == 'chitoitsu':
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("chitoitsu"))
                fu = 25

        def rinshan(player):
            if player.rinshan == True:
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("rinshan"))

        def ryuiso():
            for hai in hand.hand:
                if not hai.is_ryuhai:
                    break
            else:
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("ryuiso"))

        def tenhou(player):
            if player.tenhou_flag:
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("tenhou"))

        def chihou(player):
            if player.chihou_flag and\
                    hand.ronhai == -1:
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("chihou"))

        def renhou(player):
            if player.chihou_flag and\
                    hand.ronhai != -1:
                yaku_list.append(SouhatsuEnums.Yaku.valueOf("renhou"))

        def toitoihou():
            for block in hand.mentsu:
                if block.type not in ('minko', 'anko', 'ankan', 'daiminkan'):
                    return
            yaku_list.append(SouhatsuEnums.Yaku.valueOf("toitoihou"))

        def ryananko():
            for block in hand.mentsu:
                if block.type not in ('anko', 'ankan'):
                    return
            yaku_list.append(SouhatsuEnums.Yaku.valueOf("ryananko"))

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
                    yaku_list.append(SouhatsuEnums.Yaku.valueOf("honroutou"))
                    return

            for block in hand.mentsu:
                if block.numbers[0] != 1 and\
                        block.numbers[2] != 9:
                    break
            else:
                if hand.head.numbers[0]in (1,9):
                    yaku_list.append(SouhatsuEnums.Yaku.valueOf("junchan"))
                    return

            for block in hand.mentsu:
                if block.numbers[0] not in (0,1) and\
                        block.numbers[2] != 9:
                    break
            else:
                if hand.head.numbers[0]in (0,1,9):
                    yaku_list.append(SouhatsuEnums.Yaku.valueOf("chanta"))
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


    @staticmethod
    def chitoitsu_check(contents):
        toitsu_num = 0
        for num in contents:
            if num == 2:
                toitsu_num += 1
            if toitsu_num == 4:
                return True

    def mentsu_list_func(self):
        mentsu_list = []
        self.result_dict = {(0,)*10 : True}
        self.history = []
        def result_update(check_contents, result):
            check_contents = tuple(check_contents)
            self.history.append(check_contents)
            self.result_dict[check_contents] = result
            if len(self.history) > 50000:
                del self.result_dict[self.history[0]]
                self.history.pop(0)

        def mentsu_check(check_contents, ronhai, count):
            if tuple(check_contents) in self.result_dict:
                return self.result_dict[tuple(check_contents)]
            mentsu_hais = []
            if check_contents[0] >= 3:
                check_contents[0] -= 3
                for x in range(3):
                    mentsu_hais.append(
                            SouhatsuEnums.Hai.valueAt(0)
                            )
                if ronhai != -1:
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
                if mentsu_check(check_contents, ronhai, count+1):
                    result_update(check_contents, mentsu_list)
                    return mentsu_list
                del mentsu_list[-1]

            for i in range(1,10):
                if check_contents[i] >= 3:
                    check_contents[i] -= 3
                    for x in range(3):
                        mentsu_hais.append(SouhatsuEnums.Hai.valueAt(i))
                    if ronhai != -1:
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
                    if mentsu_check(check_contents, ronhai, count+1):
                        result_update(check_contents, mentsu_list)
                        return mentsu_list
                    del mentsu_list[-1]
                #8,9,10の順子は存在しないのでcontinue
                elif i >= 8:
                    continue
                elif check_contents[i] > 0 and check_contents[i+1] > 0 and check_contents[i+2] > 0:
                    for x in range(3):
                        check_contents[i + x] -= 1
                        mentsu_hais.append(SouhatsuEnums.Hai.valueAt(i + x))
                    mentsu_list.append(Block(mentsu_hais, block_type = "shuntsu"))
                    #順子を抜いて面子チェック
                    if mentsu_check(check_contents, ronhai, count+1):
                        result_update(check_contents, mentsu_list)
                        return mentsu_list
                    del mentsu_list[-1]
            else:
                result_update(check_contents, False)
                return False
        return mentsu_check

    def hora_flag(self, contents, ronhai, furo):
        #contents, ronhai, furo を破壊しないはず。。
        #mentsu_list_funcは上がってない場合Falseを返す
        mentsu_list_func = self.mentsu_list_func()
        mentsu_list = []
        if self.chitoitsu_check(contents):
            block = Block([SouhatsuEnums.Hai.valueAt(0)], block_type = "chitoitsu")
            mentsu_list.append(block)
            head = Block([SouhatsuEnums.Hai.valueAt(0)], block_type = "head")
            return (head, mentsu_list)

        for i, number in enumerate(contents):
            contents_check = contents[:]
            if contents_check[i] >= 2:
                contents_check[i] -= 2
                head = Block([SouhatsuEnums.Hai.valueAt(i)]*2, block_type = "head")
                #一つ目の面子チェック
                mentsu_list = mentsu_list_func(contents_check, ronhai, 0)
                if mentsu_list:
                    mentsu_list += furo
                    return (head, mentsu_list)
        else:
            return False

    def tenpai_flag(self, contents, ronhai, furo):
        #contents, ronhai, furo を破壊しないはず。。
        #ronhai, furoは必要ないので決していいと思う
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
                    if self.hora_flag(contents, ronhai, furo):
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
            if self.hora_flag(contents, ronhai, furo):
                if None not in matinums:
                    matinums[None] = []
                matinums[None].append(i)
            contents[i] -= 1
        if matinums != {}:
            return matinums
        return False

    def nakipattern(self, contents, hai, IsReach):
        def pon_check(hai):
            return (not IsReach) and contents[hai.number] >= 2
        def kan_check(hai):
            return (not IsReach) and contents[hai.number] >= 3
        def ron_check(hai):
            contents = contents[:]
            contents[hai.number] += 1
            return self.hora_flag(contents, hai)
        nakipattern = []
        if pon_check(hai): nakipattern.append("pon")
        if kan_check(hai): nakipattern.append("kan")
        if ron_check(hai): nakipattern.append("ron")
        return nakipattern

if __name__ == "__main__":
    deck = souhatsu.Deck()
    player = souhatsu.Player('aaa')
    a = HandAnalyzer()
    #和了でない例
    hand = Hand(deck, player, test=[0,0,1,2,2,3,3,8], gui=False)
    hand.show_hand()
    print('テンパイ')
    print(a.tenpai_flag(hand.contents, hand.ronhai, hand.furo))
    print('和了')
    print(a.hora_flag(hand.contents, hand.ronhai, hand.furo))
    print()

    #和了例
    hand = Hand(deck, player, test=[0,0,0,1,1,1,2,2], gui=False)
    hand.show_hand()
    print('テンパイ')
    print(a.tenpai_flag(hand.contents, hand.ronhai, hand.furo))
    print('和了')
    print(a.hora_flag(hand.contents, hand.ronhai, hand.furo))
    print()

    #テンパイ例
    hand = Hand(deck, player, test=[0,0,0,1,1,1,1,2], gui=False)
    hand.show_hand()
    print('テンパイ')
    print(a.tenpai_flag(hand.contents, hand.ronhai, hand.furo))
    print('和了')
    print(a.hora_flag(hand.contents, hand.ronhai, hand.furo))
    print()

