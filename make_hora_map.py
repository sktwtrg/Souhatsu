from hand_analyzer import HandAnalyzer
from souhatsu_enums import Hai
import struct
import json
import sys

def int2list(number):
    string = '{0:08d}'.format(number)
    result = [0] * 10
    flag = False
    for s in string:
        if s != '0':
            flag = True
        if not flag:
            continue
        result[int(s)] += 1
    return list(result)

#a = HandAnalyzer()
#print(a.hora_flag(int2list(11100028)))
#

def all_haipai(maisu = 7):
    def tsumo(contents_list, count=0):
        global output
        if count == maisu :
            output = contents_list[:]
            return True
        contents_list_out = []
        for contents in contents_list:
            for i in range(10):
                contents_temp = contents[:]
                if contents_temp[i] > 3:
                    continue
                contents_temp[i] += 1
                contents_list_out.append(tuple(contents_temp))
        contents_list_out = list(set(contents_list_out))
        contents_list_out = [list(item) for item in contents_list_out]
        count += 1
        if tsumo(contents_list_out, count = count):
            return True
    contents_list = [[0] * 10]
    tsumo(contents_list)
    return output

# 結果欲しいもの L型 1bit ron 1 tsumo 0 数ビット上がり牌番号 手牌 -> 0 or L型 headnum, (blockid, blocknum) * 2 , machi_type, ipeiko_pinfu, sutoitsu

# 19[10bit]

# hora or not : 0 or 1,
# blockid 0:head(not used), 1: shuntsu, 2 : anko, 3 :minkko, 4 : ankan, 5: minkan, 6 : sutoitsu
# blocknum shuntsuのとき, 1~7
# machi_type , 0 : ryanmen , 1 : shabo, 2 : penchan, 3 : kanchan, 4 : tanki
# ipeiko_pinfu_sutoitsu , 0 : None,  1 : sutoitsu, 2 : ipeiko_pinfu,

blocktype2id = {'shuntsu' : 1,
        'anko' : 2,
        'minko' : 3,
        'ankan' : 4,
        'minkan' : 5,
        'chitoitsu' : 6}

machi_type2id = {'ryanmen' : 0,
        'shabo' : 1,
        'penchan' : 2,
        'kanchan' : 3,
        'tanki' : 4}

def hand2result(contents, agarihai, isRon):
    haipai = contents
    string = ''.join([str(x) for x in haipai])
    string_ron = str(isRon)
    string_agarihai = str(agarihai)
    string = string_ron + string_agarihai + string

    if haipai[agarihai] == 0:
        return False
    if isRon == 1:
        horahand = a.hora_flag(haipai, Hai.valueAt(agarihai))
    else:
        horahand = a.hora_flag(haipai)

    if horahand == False:
        result = '0' * 8
        return string, result, horahand
    else:
        result = '1'
        result += str(horahand.head.numbers[0])
        for mentsu in horahand.mentsu_list:
            result += str(blocktype2id[mentsu.type])
            result += str(mentsu.numbers[0])
        candi, machi_type = a.machi_type_check(horahand.head, horahand.mentsu_list, Hai.valueAt(agarihai))
        result += str(machi_type2id[machi_type])
        if horahand.chitoitsu:
            result = '10111141'
        elif horahand.ipeiko:
            result += '2'
        else:
            result += '0'
    return string, result, horahand

bbb = all_haipai(1)
bbb = all_haipai(8)
a = HandAnalyzer()
f = open('./hand.bin','wb')
for isRon in [0, 1]:
    for agarihai in range(10):
        for haipai in all_haipai(8):
            result = hand2result(haipai, agarihai, isRon)
            if not result:
                continue
            string, result, horahand = result
            if horahand:
                print(string)
                print(horahand.string)
                print(result)
            f.write(struct.pack('q', int(string)))
            f.write(struct.pack('q', int(result)))
