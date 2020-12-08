from os import listdir
import re
from numpy.linalg import norm
from numpy import dot
from os.path import join as pathJoin
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from collections import Counter
from zipfile import ZipFile
import shutil
import os


def unzip(filename):
    file_path = "media/{}".format(filename)
    with ZipFile(file_path, 'r') as zipfile:
        print("unzipping in progress....")
        if (os.path.isdir("unzipped")):
            shutil.rmtree("unzipped")
        os.mkdir("unzipped")
        zipfile.extractall("unzipped/")
        print("unzipping done")
    
    shutil.rmtree("media")

    return

def stubDownload(filename):
    file_path = "media/{}".format(filename)
    print("stub code present!")

    if (os.path.isdir("stubcode")):
        shutil.rmtree("stubcode")

    os.mkdir("stubcode")
    os.rename(file_path, 'stubcode/{}'.format(filename))

    return


def comment_remover(text):
    """This function removes comments of a C++ file.
    Code has been taken from https://stackoverflow.com/questions/241327/remove-c-and-c-comments-using-python.
    Parameters:
        Text - The C++ code from which you want to remove comments

    Return Values:
        This returns the text after removing comments"""
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "  # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


def reduce(f, func, final_func):

    added = ["main", f]
    num = 1
    while num > 0:
        num = 0
        p = re.compile('\w+')
        word_list = p.findall(final_func[f])
        for f1 in func.keys():
            c = word_list.count(f1)
            if f1 not in added and c > 0:
                num += 1
                final_func[f] += (c)*func[f1]
                added.append(f1)


def getdict(filename):
    keywords = ["int", "double", "long", "float", "bool", "string", "vector", "stack", "if", "for",
                "while", "else", "do", "switch", "std", "using", "namespace", "main", "return", "cin", "cout", "endl"]
    file = open(filename, "r", errors="ignore")
    text = file.read()
    final_text = comment_remover(text)

    glob = ""
    brackets = 0
    func = {}
    final_func = {}
    flag = 0

    for line in final_text.split("\n"):
        l1 = line.split(" ")
        if (l1[0] == "typedef"):
            keywords.append(l1[-1])
            continue

        if line.count("#") > 0:
            continue
        l = line.split('(')
        if (len(l) > 1) and (flag == 0):
            flag = 1
            l1 = l[0].split()
            func[l1[-1]] = ""

        if flag == 0:
            glob += (line+"\n")

        if flag == 1:
            c1 = line.count('{')
            c2 = line.count('}')
            c3 = line.count("'}'")
            c4 = line.count('"}"')
            c5 = line.count("'{'")
            c6 = line.count('"{"')

            if (c1 > 0):
                brackets += c1-(c5+c6)

            if (c2 > 0) and (brackets != 0):
                brackets -= c2-(c3+c4)

            key = list(func.keys())
            func[key[-1]] += (line+"\n")

            if (brackets == 0) and ((c1+c2-c3-c4-c5-c6) != 0):
                flag = 0

    func["main"] = glob + func["main"]

    p = re.compile('\w+')
    word_list = p.findall(func["main"])
    final_dict = dict(Counter(word_list))

    for f in func.keys():
        final_func[f] = func[f]

    for f in func.keys():
        if f != "main" and f in final_dict.keys():
            reduce(f, func, final_func)
            func["main"] += (final_dict[f])*final_func[f]

    word_list = p.findall(func["main"])
    final_dict = dict(Counter(word_list))

    for w in keywords:
        if w in final_dict.keys():
            del final_dict[w]

    for f in func.keys():
        if f != "main" and f in final_dict.keys():
            del final_dict[f]

    file.close()
    #print(func.keys())
    return final_dict

# import dictBuilder


''' issues:
    2. Checking file or dir 
'''


def dict2Vec(map):
    l = []
    for k in map.keys():
        l.append(map[k])
    l.sort(reverse=True)
    return l


def dictDiff(map1, map2):
    for x in map2.keys():
        if x in map1.keys():
            map1[x] -= map2[x]
    return


def calcPercent(map1, map2):
    # Send maps as inputs, returns plagPercent-folat

    l1 = dict2Vec(map1)
    l2 = dict2Vec(map2)

    m = max(len(l1), len(l2))

    l1_final = [0]*m
    l1_final[:len(l1)] = l1
    l2_final = [0]*m
    l2_final[:len(l2)] = l2

    y = 1-(norm(np.array(l1_final)-np.array(l2_final)) /
           max(norm(l1_final), norm(l2_final)))
    return (100*y)


def redPlag(inpath, outpath, cplusplus, stub, stubpath):
    
    if (os.path.isdir("rpoutput")):
        shutil.rmtree("rpoutput")
    os.mkdir("rpoutput")

    mypath = str(inpath)

    file_name = [f for f in listdir(mypath)]
    file_path = [pathJoin(mypath, f) for f in listdir(mypath)]
    file_name.sort()
    file_path.sort()

    if(stub):
        stubpath = "stubcode/"+(os.listdir("stubcode"))[0]

    # print((file_path))
    num_file_path = int(len(file_path))
    # print("Total File Count : ",num_file_path)

    data_PD = {"File A": [], "File B": [], "Plagiarism Percentage": []}

    data = np.zeros(num_file_path**2)
    data = data.reshape(num_file_path, -1)

    maps = []
    p = re.compile('\w+')

    if(cplusplus == True):
        for x in range(num_file_path):
            maps.append(getdict(file_path[x]))
    else:
        for x in range(num_file_path):
            file = open(file_path[x], "r", errors="ignore")
            text = file.read()
            maps.append(dict(Counter(p.findall(text))))
            file.close()

    if(stub == True):
        if(cplusplus == True):
            stub_map = getdict(stubpath)
        else:
            file = open(stubpath, "r", errors="ignore")
            text = file.read()
            stub_map = dict(Counter(p.findall(text)))
            file.close()
        for x in range(num_file_path):
            dictDiff(maps[x], stub_map)

    for x in range(num_file_path):
        for y in range(num_file_path):

            a = maps[x]
            b = maps[y]
            data[x][y] = calcPercent(a, b)
            if(x < y):
                data_PD["File A"].append(file_name[x])
                data_PD["File B"].append(file_name[y])
                data_PD["Plagiarism Percentage"].append(round(data[x][y], 2))

    PD = pd.DataFrame(data=data_PD, columns=[
                      "File A", "File B", "Plagiarism Percentage"])
    PD.sort_values(by="Plagiarism Percentage", inplace=True,
                   ascending=False, ignore_index=True)
    PD.to_csv(outpath + "/testing.csv")

    fig = plt.figure()  # Possible ERROR
    ax = fig.add_subplot(111)
    for (j, i), label in np.ndenumerate(data):
        ax.text(i, j, int(round(data[i][j], 0)),
                ha='center', va='center', size=8)

    img = plt.imshow(data, interpolation='nearest', cmap="RdYlGn_r",
                     vmin=0, vmax=100, alpha=0.8, origin="lower")
    plt.colorbar(img)
    plt.xticks(list(range(num_file_path)), file_name, rotation=90)
    plt.yticks(list(range(num_file_path)), file_name)
    plt.tight_layout()

    plt.savefig(outpath + '/testing.png')
    # plt.show()
    # plt.show(block=False)
    # plt.pause(3)
    # plt.close()
