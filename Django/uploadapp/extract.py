#!/usr/bin/python
# -*- coding: utf-8 -*-
from zipfile import ZipFile
import shutil
import os


def unzip(filename):
    file_path = 'media/{}'.format(filename)
    with ZipFile(file_path, 'r') as zipfile:
        print ('unzipping in progress...')
        shutil.rmtree("unzipped")
        os.mkdir("unzipped")
        zipfile.extractall('unzipped/')
        print ('unzipping done')
    return


import re
from collections import Counter


# code from https://stackoverflow.com/questions/241327/remove-c-and-c-comments-using-python

def comment_remover(text):

    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ' '  # note: a space and not an empty string
        else:
            return s

    pattern = \
        re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"'
                   , re.DOTALL | re.MULTILINE)
    return re.sub(pattern, replacer, text)


def reduce(f, func):
    added = ['main', f]
    num = 1
    while num > 0:
        num = 0
        p = re.compile('\w+')
        word_list = p.findall(func[f])
        for f1 in func.keys():
            c = word_list.count(f1)
            if f1 not in added and c > 0:
                num += 1
                func[f] += c * func[f1]
                added.append(f1)


def getdict(filename):
    file = open(filename, 'r')
    text = file.read()
    final_text = comment_remover(text)

    glob = ''
    brackets = 0
    func = {}
    flag = 0

    for line in final_text.split('\n'):
        if line.count('#') > 0:
            continue
        l = line.split('(')
        if len(l) > 1 and flag == 0:
            flag = 1
            l1 = l[0].split()
            func[l1[-1]] = ''

        if flag == 0:
            glob += line + '\n'

        if flag == 1:
            c1 = line.count('{')
            c2 = line.count('}')
            c3 = line.count("'}'")
            c4 = line.count('"}"')
            c5 = line.count("'{'")
            c6 = line.count('"{"')

            if c1 > 0:
                brackets += c1 - (c5 + c6)

            if c2 > 0 and brackets != 0:
                brackets -= c2 - (c3 + c4)

            key = list(func.keys())
            func[key[-1]] += line + '\n'

            if brackets == 0 and c1 + c2 - c3 - c4 - c5 - c6 != 0:
                flag = 0

    func['main'] = glob + func['main']

    p = re.compile('\w+')
    word_list = p.findall(func['main'])
    final_dict = dict(Counter(word_list))

    for f in func.keys():
        if f != 'main' and f in final_dict.keys():
            reduce(f, func)
            func['main'] += final_dict[f] * func[f]

    word_list = p.findall(func['main'])
    final_dict = dict(Counter(word_list))

    keywords = [
        'int',
        'double',
        'long',
        'float',
        'bool',
        'string',
        'vector',
        'stack',
        'if',
        'for',
        'while',
        'else',
        'do',
        'switch',
        'std',
        'using',
        'namespace',
        'main',
        'return',
        'cin',
        'cout',
        'endl',
        ]

    for w in keywords:
        if w in final_dict.keys():
            del final_dict[w]

    for f in func.keys():
        if f != 'main' and f in final_dict.keys():
            del final_dict[f]

    file.close()
    return final_dict


import numpy as np
from scipy.stats import pearsonr  # for correlation coefficent
from numpy import dot
from numpy.linalg import norm  # norm of a vector

print ()


def vec(map):

    # vectorising a dictionary

    l = []
    for k in map.keys():
        l.append(map[k])
    l.sort(reverse=True)
    return l


def outputter(a, b):  # send dictionary as inputs

    l1 = vec(a)
    l2 = vec(b)

    # print(a)
    # print(b)

    m = max(len(l1), len(l2))

    l1_final = [0] * m
    l1_final[:len(l1)] = l1
    l2_final = [0] * m
    l2_final[:len(l2)] = l2

    # print(l1_final)
    # print(l2_final)

    z = np.array(l1_final) - np.array(l2_final)

    # print(z)

    (corr, _) = pearsonr(l1_final, l2_final)

    # print("corr is : ",corr)

    x = dot(l1_final, l2_final) / (norm(l1_final) * norm(l2_final))

    # print(x)

    y = 1 - norm(z) / max(norm(l1_final), norm(l2_final))

    # print(100*y)

    return 100 * y


    # w = dot(l1_final, z)/(norm(l1_final)*norm(z))
    # print(w)

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from os import listdir
from os.path import join as pathJoin


def redPlag(path):

    mypath = str(path)

    file_name = [f for f in listdir(mypath)]
    file_path = [pathJoin(mypath, f) for f in listdir(mypath)]
    file_name.sort()
    file_path.sort()

    print (file_name)

    num_file_path = int(len(file_path))

    # print("Total File Count : ",num_file_path)

    a = getdict(file_path[0])
    b = getdict(file_path[2])
    ans = outputter(a, b)

    # print("Testing Value : ", ans)

    data_PD = {'File A': [], 'File B': [], 'Plagiarism Percentage': []}

    data = np.zeros(num_file_path ** 2)
    data = data.reshape(num_file_path, -1)

    # x_data = np.zeros(num_file_path**2)
    # x_data = x_data.reshape(num_file_path, -1)
    # y_data = np.zeros(num_file_path**2)
    # y_data = y_data.reshape(num_file_path, -1)

    for x in range(num_file_path):
        for y in range(num_file_path):

            a = getdict(file_path[x])

            # print("x is : ",x)

            b = getdict(file_path[y])

            # print("y is : ",y)

            data[x][y] = outputter(a, b)

            # x_data[x][y] = x
            # y_data[x][y] = y

            if x < y:
                data_PD['File A'].append(file_name[x])
                data_PD['File B'].append(file_name[y])
                data_PD['Plagiarism Percentage'
                        ].append(round(data[x][y], 2))

                # data_PD.append([file_name[x], file_name[y], data[x][y]])

    PD = pd.DataFrame(data=data_PD, columns=['File A', 'File B',
                      'Plagiarism Percentage'])
    PD.sort_values(by='Plagiarism Percentage', inplace=True,
                   ascending=False, ignore_index=True)
    PD.to_csv('part1/testing.csv')

    # print(PD)
    # print(data)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for ((j, i), label) in np.ndenumerate(data):
        ax.text(
            i,
            j,
            int(round(data[i][j], 0)),
            ha='center',
            va='center',
            size=8,
            )

    img = plt.imshow(
        data,
        interpolation='nearest',
        cmap='RdYlGn_r',
        vmin=0,
        vmax=100,
        alpha=0.8,
        origin='lower',
        )
    plt.colorbar(img)
    plt.xticks(list(range(num_file_path)), file_name, rotation=90)
    plt.yticks(list(range(num_file_path)), file_name)
    plt.tight_layout()

    plt.savefig('part1/testing.png')


    # plt.show()
    # plt.show(block=False)
    # plt.pause(3)
    # plt.close()
