#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import PrintCipher96_model_3way
import time
import os

if __name__ == "__main__":

    cd = dict()

    cd["cipher_name"] = "PrintCipher96_3way"

    cd["cipher_size"] = 96
    cd["sbox_size"] = 3
    cd["sbox_num"] = 32

    cd["mode"] = 1

    folder = cd["cipher_name"] + "_mode_{}_1".format(cd["mode"])

    if not os.path.exists(folder):
        os.mkdir(folder)

    distinguish_find = True

    search_space = list()
    bs = []
    es = []
    for i in range(0, 6):
        b1 = [0 for bii in range(0, cd["cipher_size"])]
        b1[i] = 1
        bs.append(PrintCipher96_model_3way.perm_wire_value(copy.deepcopy(b1)))

    for j in range(0, 96):
        e1 = [0 for eii in range(0, cd["cipher_size"])]
        e1[j] = 1
        es.append(e1)

    for i1 in range(0, len(bs)):
        for i2 in range(i1 + 1, len(bs)):
            b1 = copy.deepcopy(bs[i1])
            b2 = copy.deepcopy(bs[i2])
            for j1 in range(0, len(es)):
                for j2 in range(j1 + 1, len(es)):
                    e1 = copy.deepcopy(es[j1])
                    e2 = copy.deepcopy(es[j2])
                    search_space.append(copy.deepcopy([b1, b2, e1, e2]))

    round_i = 0
    cd["record_file"] = folder + "////" + cd["cipher_name"] + "_record_mode{}.txt".format(cd["mode"])
    cd["time_record"] = folder + "////" + cd["cipher_name"] + "_time_record_mode{}.txt".format(cd["mode"])
    total_search = len(search_space)
    ttt1 = time.time()
    while distinguish_find:
        distinguish_find = False
        round_i += 1
        cd["solve_file"] = folder + "////" + cd["cipher_name"] + "_round{}.stp".format(round_i)
        t1 = time.time()
        search_count = 0
        for ss in search_space:
            cd["b1"] = copy.deepcopy(ss[0])
            cd["b2"] = copy.deepcopy(ss[1])
            cd["e1"] = copy.deepcopy(ss[2])
            cd["e2"] = copy.deepcopy(ss[3])
            mode = [cd["mode"], [0, round_i]]
            t11 = time.time()
            search_count += 1
            PrintCipher96_model_3way.model_build(cd, mode)
            flag = PrintCipher96_model_3way.solver(cd["solve_file"])
            t22 = time.time()
            print(t22 - t11)
            if flag:
                rf = open(cd["record_file"], "a")
                rf.write("*" * 20)
                rf.write("{} round impossible 3-polytopic trans found\n".format(round_i))
                rf.write("when the values:\n")
                rf.write("b1 = {}\n".format(str(cd["b1"])))
                rf.write("b2 = {}\n".format(str(cd["b2"])))
                rf.write("e1 = {}\n".format(str(cd["e1"])))
                rf.write("e2 = {}\n".format(str(cd["e2"])))
                rf.close()
                distinguish_find = True
                break
            else:
                print("testing: round = {}, search_count = {}, total_search = {}".format(round_i, search_count, total_search))
        t2 = time.time()
        tf = open(cd["time_record"], "a")
        if distinguish_find:
            tf.write("After " + str(t2 - t1) + "time, we found {} rounds impossible 3-polytopic trans.\n\n".format(round_i))
        else:
            tf.write("After " + str(t2 - t1) + "time, we show no {} round impossible 3-polytopic trans.\n\n".format(round_i))
        tf.close()
