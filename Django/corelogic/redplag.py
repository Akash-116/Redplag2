import dictbuilder
import numpy as np
import pandas as pd
import matplotlib as mpl
import sys
import matplotlib.pyplot as plt
from os import listdir 
from os.path import join as pathJoin
from numpy import dot
from numpy.linalg import norm
import re
from collections import Counter

def dict2vec(map):
	"""! Converts a dictionary to a sorted list containing the values of the key-value pairs from the dictionary.

	@param map : python-dict - Dictionary of the form {<string> : <int>}.

	@retval l : python-list - List containing values, sorted in decreasing order.

	"""
	l = []
	for k in map.keys():
		l.append(map[k])
	l.sort(reverse=True)
	return l

def calcPercent(map1, map2): # Send dictionary as inputs
	"""!Takes two dictionaries as input and calculates their percentage of similarity based on the values in key-value pairs.

	@param map1 : python-dict - Dictionary containing word frequencies of file1
	@param map2 : python_dict - Dictionary containing word frequencies of file2

	@return : float - a measure of similarity between the two files, as a percentage.

	-> Convert the dictionaries into sorted lists and pad the smaller vector with 0s. \n
	-> The similarity between 2 files must be a property of the files i.e. should not depend on the other files in the directory. \n
	-> The final metric for similarity is calculated as distance between the padded vectors, divided by the max of norm(vector1), norm(vector2).\n
	(we felt distance between the vectors (distance betwen endpoints) was a better metric to measure similarity than the angle between them, and we used max( norm(vector1), norm(vector2) ) in the denominator for normalization.)
	"""
	l1 = dict2vec(map1)
	l2 = dict2vec(map2)

	m = max(len(l1), len(l2))

	l1_final = [0]*m
	l1_final[:len(l1)] = l1
	l2_final = [0]*m
	l2_final[:len(l2)] = l2

	y = 1-(norm(np.array(l1_final)-np.array(l2_final))/max(norm(l1_final), norm(l2_final)))
	return (100*y)

def dictDiff(map1, map2):
	"""!Subtracts map2 from map1.

	@param map1 : python-dict - Main dictionary containing word frequencies of file
	@param map2 : python-dict - Auxillary dictionary containing word frequencies of stub code.

	@return : void - This function modifies map1.

	Typically used to deal with the cases when there is a stub code given, and this similarity (which shouldn't count under plagiarism) is migitated by subtracting the dict of stub code from the dict of each file.
	"""
	for x in map2.keys():
		if x in map1.keys():
			map1[x] -= map2[x]

def redPlag(inpath, outpath, cplusplus, stub, stubpath):
	"""! Core Function, which creates a .csv and a .png file, for interpreting the results of RedPlag Plagiarism Checker.

	@param inpath : string - path of directory containing the files to be checked for plagiarism.
	@param outpath : string - path of directory to output the result files. Preferably empty.
	@param cplusplus : bool - a boolean value informing whether the files are c++ code or simple text.
	@param stub : bool - a boolean parameter informing whether a stub code is used. 
	@param stubpath : string - path of the stub code file (not the directory), if a stub code was given. Can be any valid string, in case no stub code is used.

	@return : void - this function creates a .csv and a .png file in 'outpath' directory

	-> Store names (and their paths) of all files in the 'inpath' dir.\n
	-> Depending on bool:cpluscplus, use either getdict() in dictbuilder.py or just use simple bag-of-words to build the dict. \n
	-> (if bool:stub is TRUE) Find the word-freq-dict for the stub code and subtract this from all other file's corresponding dictionaries. \n
	-> Calculate the percentage similarity for each pair of files and store in a numpy array. \n
	-> Using this data, an appropiate .csv file and a heatmap image is plotted using matplotlib; and saved in the 'outpath' dir.\n
	The csv file has "File A", "File B" and "Plagiarism Percentage" as columns (values in "Plagiarism Percentage" column being descendingly sorted).
	"""
	mypath = str(inpath)

	file_name = [f for f in listdir(mypath)]
	file_path = [pathJoin(mypath, f) for f in listdir(mypath)]
	file_name.sort()
	file_path.sort()

	# print((file_path))
	num_file_path = int(len(file_path))
	# print("Total File Count : ",num_file_path)

	data_PD = {"File A":[], "File B":[], "Plagiarism Percentage":[]}

	data = np.zeros(num_file_path**2)
	data = data.reshape(num_file_path, -1)

	maps = []
	p = re.compile('\w+')

	for x in range(num_file_path):
		if(cplusplus == True):
			maps.append(dictbuilder.getdict(file_path[x]))
		else:
			file = open(file_path[x], "r", errors='ignore')
			text = file.read()
			maps.append(dict(Counter(p.findall(text))))
			file.close()

	if(stub == True):
		if(cplusplus == True):
			stub_map = dictbuilder.getdict(stubpath)
		else:
			file = open(stubpath, "r", errors='ignore')
			text = file.read()
			stub_map = dict(Counter(p.findall(text)))
			file.close()

		for x in range(num_file_path):
			dictDiff(maps[x], stub_map)

	for x in range(num_file_path):
		for y in range(num_file_path):

			a = maps[x]
			# print("x is : ",x)
			b = maps[y]
			# print("y is : ",y)
			data[x][y] = calcPercent(a, b)
			if(x<y):
				data_PD["File A"].append(file_name[x])
				data_PD["File B"].append(file_name[y])
				data_PD["Plagiarism Percentage"].append(round(data[x][y],2))

	PD = pd.DataFrame(data = data_PD, columns = ["File A", "File B", "Plagiarism Percentage"])
	PD.sort_values(by="Plagiarism Percentage", inplace=True, ascending=False, ignore_index=True)
	PD.to_csv(outpath + "/results.csv")
	# print(PD)
	# print(data)

	fig = plt.figure()
	ax = fig.add_subplot(111)

	for (j,i),label in np.ndenumerate(data):
	    ax.text(i,j, int(round(data[i][j],0)),ha='center',va='center', size=8)

	img = plt.imshow(data, interpolation='nearest', cmap = "RdYlGn_r", vmin = 0, vmax = 100, alpha = 0.8, origin = "lower")
	plt.colorbar(img)
	plt.xticks(list(range(num_file_path)), file_name, rotation = 90)
	plt.yticks(list(range(num_file_path)), file_name)
	plt.tight_layout()

	plt.savefig(outpath + '/results.png')
	# plt.show()
	# plt.show(block=False)
	# plt.pause(3)
	# plt.close()

if(__name__=="__main__"):
	redPlag(str(sys.argv[1]), str(sys.argv[2]), bool(int(sys.argv[3])), bool(int(sys.argv[4])), str(sys.argv[5]))