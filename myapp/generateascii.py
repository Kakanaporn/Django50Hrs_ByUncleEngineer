#generate ascii
import random
import string
def GenerateToken(domain='http://localhost:8000/confirm/'):
	allchar = [ i for i in list(string.ascii_letters)]
	allchar.extend([str(i) for i in range(10)])
	emailtoken = ''
	for i in range(40):
		emailtoken += random.choice(allchar)

	url = domain + emailtoken
	#print(url)
	return url

gurl = GenerateToken('https://uncle-friut.com/confirm/')
print(gurl)


'''
allchar = []
for i in range(65,91):
	allchar.append(chr(i))
for i in range(97,123):
	allchar.append(chr(i))
for i in range(10):
	allchar.append(chr(i))

print(allchar)

import string
print(list(string.ascii_letters))
print('----')
allchar = [ i for i in list(string.ascii_letters)]
allchar.extend([str(i) for i in range(10)])
print(allchar)
'''