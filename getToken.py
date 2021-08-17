from re import findall
from os import getenv, listdir
from ntpath import isdir, isfile

try:
	import requests
	requests_installed = True
	requests.urllib3.disable_warnings(requests.urllib3.exceptions.InsecureRequestWarning)
except ImportError:
	requests_installed = False

map = lambda func, arr: [func(i) for i in arr]
roaming = getenv('APPDATA')

##### Get Discord Token #####
discords = {
	'Discord': roaming + '\\Discord',
	'Discord PTB': roaming + '\\discordptb',
	'Discord Canary': roaming + '\\discordcanary'
}
temp = {}
for i in discords:
	if isdir(discords[i]):
		temp[i] = discords[i]

discords = temp; del temp

if len(discords) == 0:
	print('Discord is not installed.')
elif len(discords) == 1:
	chosen = discords
else:
	print('You have multiple versions of discord installed, please choose one from the list below')
	ix = 0
	for i in discords:
		ix += 1
		print(f'{ix}. {i} (in `{discords[i]}`)')

	while 1:
		try:
			chosen = int(input('> '))
			if chosen in range(1, len(discords) + 1): break
		except Exception:
			pass

	chosen = {list(discords.keys())[chosen - 1]: list(discords.values())[chosen - 1]}

print('\n\n')

if chosen:
	name = list(chosen.keys())[0]
	path = chosen[name] + '\\Local Storage\\leveldb'

	tokens = []

	for fn in listdir(path):
		if not fn.endswith('.log') and not fn.endswith('.ldb'):
			continue

		lines = open(f'{path}\\{fn}', mode='r', encoding='utf-8', errors='ignore').readlines()
		lines = map(str.strip, lines)

		for line in lines:
			for token in findall(r'mfa.[\w-]{84}', line):
				tokens.append(token)

	print(f'{name}: {", ".join(tokens)}')

##### Get Yare.io Token #####
if requests_installed:
	if isfile('yare.txt'):
		yare = open('yare.txt', 'r')
		lines = yare.readlines()
		yare.close()
		username, password = map(str.strip, lines)
	else:
		username = input('Username: ')
		password = input('Password: ')
		yare = open('yare.txt', 'w')
		yare.write(f'{username}\n{password}')
		yare.flush()
		yare.close()
	resp = requests.post('https://yare.io/validate', json={ 'user_name': username, 'password': password }, verify=0)
	if resp.ok:
		print(f'Yare: {resp.json()["data"]}')
else:
	print('Yare: install requests')