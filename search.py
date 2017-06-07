def hora_flag(contents):
    mentsu_list = []

    def chitoitsu_check(contents):
        toitsu_num = 0
        for num in contents:
            if num == 2:
                toitsu_num += 1
            if toitsu_num == 4:
                return True

    def mentsu_check(check_contents, count, mentsu_list):
        if check_contents == [0]*10:
            return True
        if check_contents[0] >= 3:
            check_contents[0] -= 3
            mentsu_list.append(0)
            if mentsu_check(check_contents,count+1, mentsu_list):
                return True

        for i in range(1,10):
            if check_contents[i] >= 3:
                check_contents[i] -= 3
                mentsu_list.append(i)
                if mentsu_check(check_contents, count+1, mentsu_list):
                    return True
            elif i >= 8:
                continue
            elif check_contents[i] > 0 and check_contents[i+1] > 0 and check_contents[i+2] > 0:
                check_contents[i] -= 1
                check_contents[i+1] -= 1
                check_contents[i+2] -= 1
                mentsu_list.append(i+10)
                if mentsu_check(check_contents, count+1, mentsu_list):
                    return True
        else:
            del mentsu_list[:]
            return False

    if chitoitsu_check(contents):
        return True

    for i, number in enumerate(contents):
        contents_check = list(contents)[:]
        if contents_check[i] >= 2:
            contents_check[i] -= 2
            if mentsu_check(contents_check, 0, mentsu_list):
                return mentsu_list
    else:
            return False


def tenpai_flag2(contents, hand2count_dict):
    for j in range(10):
        contents_temp = contents[:]
        contents_temp[j] += 1
        if hora_flag(contents_temp):
            hand2count_dict[tuple(contents)] = 0
            return True
#            continue
    return False


def tenpai_flag(contents_list, hand2count_dict, count=1):
    matihais = []
    contents_list_output = []
    for contents in contents_list:
        for i in range(10):
            contents_reduced = contents[:]
            if contents[i] > 0:
                contents_reduced[i] -= 1
            else:
                continue
            for j in range(10):
                contents_temp = contents_reduced[:]
                contents_temp[j] += 1
                if hora_flag(contents_temp):
                    contents_list_output.append(contents_temp)
                    matihais.append(i)
                    hand2count_dict[tuple(contents)] = count
                    continue
        else:
            continue
            tenpai_flag(contents,count)

        if matihais != []:
            print(matihais)
            return True
        else:
            return False

def shanten_check(contents, hand2count_dict):

    if tuple(contents) in hand2count_dict:
        return hand2count_dict[tuple(contents)]
    for i in range(10):
        contents_reduced = contents[:]
        contents_reduced[i] += 1
        for j in range(10):
#            print(i,j)
            contents_temp = contents_reduced[:]
            if contents_temp[j] > 0:
                contents_temp[j] -= 1
            else:
                continue
            if tuple(contents_temp) in hand2count_dict:
                if hand2count_dict[tuple(contents_temp)] == 0:
                    hand2count_dict[tuple(contents)] = 1
                    return hand2count_dict[tuple(contents)]
                    
#                shanten_candidates.append(hand2count_dict[tuple(contents)] + 1)
#                hand2count_dict[tuple(contents)] = hand2count_dict[tuple(contents_temp)] + 1
#                print(hand2count_dict[tuple(contents)])

    return None

output = []
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

ordict = {}
contents = [4,1,0,0,0,0,0,2,0,0]
contents2 = [4, 1, 0, 0, 0, 1, 0, 0, 0, 2]
contents3 = [0, 1, 2, 2, 1, 2, 0, 0, 0, 0]
print(hora_flag(contents3))
print(tenpai_flag2(contents,ordict))
print(shanten_check(contents2,ordict))
input()

haipailist = all_haipai()
hora_counter = 0
tenpai_counter = 0
ishanten_counter = 0
hand2dict = {}
for haipai in haipailist:
#    print(haipai)
    if hora_flag(haipai):
        hora_counter += 1
for haipai in haipailist:
    if tenpai_flag2(haipai,hand2dict):
        tenpai_counter += 1
for haipai in haipailist:
    if shanten_check(haipai,hand2dict):
        ishanten_counter += 1
print(haipailist[0])
tenpai_flag(list(haipailist),hand2dict)
#
print('hora_counter')
print(hora_counter)
print('tenpai_counter')
print(tenpai_counter)
print('ishanten_counter')
print(ishanten_counter)
print('all')
print(len(haipailist))
#print(len(hand2dict))
#for haipai in haipailist:
#    if tuple(haipai) not in hand2dict:
#        print(haipai)

#
#contents2 = [4, 0, 0, 0, 0, 1, 0, 0, 0, 2]
#print(1)
#print(hand2dict[tuple(contents2)]) 
