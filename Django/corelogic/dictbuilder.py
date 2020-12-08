import re
from collections import Counter

def comment_remover(text):
	"""! Trims out comments from a cpp file.
	@param text : string - the c++ code read from file.

	@return : string - returns the string/text after removing comments (in c++ context).

	Code inspired from https://stackoverflow.com/questions/241327/remove-c-and-c-comments-using-python.
	"""
	def replacer(match):
		s = match.group(0)
		if s.startswith('/'):
			return " " # note: a space and not an empty string
		else:
			return s
	pattern = re.compile(
		r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
		re.DOTALL | re.MULTILINE
	)
	return re.sub(pattern, replacer, text)

def reduce(f, func, final_func):
	"""!Reduces a c++ function in the c++ code into simpler form.

	@param f : string - name of the function in c++ code.
	@param func : python-dict - dictionary containing (function name : function code) as key-value pairs.
	@param final_func : python-dict - dictionary containing final reduced forms of the function definitions.

	@return : void - We modify the final_func dictionary in this function.

	-> Say, if in the definition of a function f(), some other function f1() is called 'c1' times, then the definition of f1() is made explicit in the definition of f() 'c1' times.\n
	-> To tackle the problem of recursive functions, a list of the function names which were already replaced is maintained, and this list contains "main" and "f" initially. \n
	"""
	added = ["main", f]
	num = 1
	while num>0:
		num=0
		p = re.compile('\w+')
		word_list = p.findall(final_func[f])
		for f1 in func.keys():
			c = word_list.count(f1)
			if f1 not in added and c>0:
				num+=1
				final_func[f]+=(c)*func[f1]
				added.append(f1)

def getdict(filename):
	"""! Builds a dictionary containing (word : word frequency) as key-value pairs.

	@param filename : string - name/path of the c++ file 

	@retval final_dict : python-dict - a dictionary containing words and their frequencies.

	-> The comments are trimmed out from the code using comment_remover().\n
	-> The C++ code is split into functions: A function is recognised by '(' and the function code is extracted using '{' and '}'. \n
	-> These functions are reduced into simpler forms using reduce(), and appended to the main code for each function call made.\n
	-> Global code which is not part of any function is appended to the main code.\n
	-> The keywords are removed and the dictionary is built, by calculating the word count. \n

	"""
	keywords = ["int", "double", "long", "float", "bool", "string", "vector", "stack", "if", "for", "while", "else", "do", "switch", "std", "using", "namespace", "main", "return", "cin", "cout", "endl"]
	file = open(filename, "r", errors='ignore')
	text = file.read()
	final_text = comment_remover(text)

	glob = ""
	brackets = 0
	func = {}
	final_func = {}
	flag = 0

	for line in final_text.split("\n"):
		l1 = line.split(" ")
		if (l1[0]=="typedef"):
			keywords.append(l1[-1])
			continue

		if line.count("#")>0: continue
		l = line.split('(')
		if (len(l)>1) and (flag==0):
			flag = 1
			l1 = l[0].split()
			func[l1[-1]] = ""

		if flag==0: glob += (line+"\n")

		if flag==1:
			c1 = line.count('{')
			c2 = line.count('}')
			c3 = line.count("'}'")
			c4 = line.count('"}"')
			c5 = line.count("'{'")
			c6 = line.count('"{"')

			if (c1>0): brackets += c1-(c5+c6)		

			if (c2>0) and (brackets != 0): brackets -= c2-(c3+c4)

			key = list(func.keys())
			func[key[-1]] += (line+"\n")

			if (brackets==0) and ((c1+c2-c3-c4-c5-c6)!=0): flag=0

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