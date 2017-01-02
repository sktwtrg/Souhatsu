
class HandAnalyzer:

    def __init__(self, hand):
        self.hand = hand

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

    def yaku_check(self):
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

    def hora_flag(self):
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


