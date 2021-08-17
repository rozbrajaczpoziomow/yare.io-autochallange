try:
	import requests
except ImportError:
	print('To use this script, please install the requests module')
	exit(3)
try:
	from pyperclip import copy
except ImportError:
	print('If you want the Challange URL to be automatically copied to clipboard, please install the pyperclip module')
	copy = lambda text: True
from sys import argv
from time import sleep
from webbrowser import open_new_tab as firefox
from random import randint

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

argv = argv[1:]

def discord(mfa, cid, content):
	global proxies
	json = {
		'content': content,
		'nonce': randint(9328952, 298595282590),
		'tts': False
	}
	headers = {
		'Host': 'discord.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
		'Accept': '*/*',
		'Accept-Language': 'en-US',
		'Accept-Encoding': 'gzip, deflate, br',
		'Content-Type': 'application/json',
		'Authorization': mfa,
		'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjkxLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTEuMCIsImJyb3dzZXJfdmVyc2lvbiI6IjkxLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6Imh0dHBzOi8vd3d3LnlvdXR1YmUuY29tLyIsInJlZmVycmluZ19kb21haW4iOiJ3d3cueW91dHViZS5jb20iLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTM2ODksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
		'X-Debug-Options': 'bugReporterEnabled',
		'Origin': 'https://discord.com',
		'Alt-Used': 'discord.com',
		'Connection': 'keep-alive',
		'Referer': 'https://discord.com/channels/604382795745198081/604382796332662787',
		'Cookie': 'OptanonConsent=isIABGlobal=false&datestamp=Tue+Aug+17+2021+01%3A11%3A39+GMT%2B0200+(czas+%C5%9Brodkowoeuropejski+letni)&version=6.17.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1&AwaitingReconsent=false; __stripe_mid=7cdb1822-4994-4e12-8d13-52e6cca7ae5493f158; __dcfduid=319a30ef1c408f620a4874bc2f57e3c7; locale=en-US; __cfruid=bba7811baac6c5e643a7bee5e57149b0bb236a5a-1609763689; __sdcfduid=1e072510fee611ebbd7bf9d9b56d00712f58bd720699648bc1d41a902369c5d47f2748c74bf7e028dd1d09f92bede144',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'TE': 'trailers'
	}
	url = f'https://discord.com/api/v9/channels/{cid}/messages'
	requests.post(url, json=json, headers=headers, proxies=proxies, verify=0)

def _input(p):
	global argv
	if len(argv) > 0:
		resp = argv[0]
		argv = argv[1:]
		print(f'{p}{resp}')
	else:
		resp = input(p)
	return resp

session_id = _input('Session token: ')
user_id    = _input('Username: ')
shape      = _input('Shape [(c)ircle, (s)quare, (t)riangle]: ')
color      = _input('Color [(b)lue, (p)urple, (r)ed, (y)ellow, (g)reen]: ')

use_proxy  = _input('Use a proxy? [yes/no] ').startswith('y')
if use_proxy:
	proxy_ip   = _input('Proxy IP: ')
	proxy_port = _input('Proxy Port: ')

post_discord = _input('Post to discord? [yes/no] ').startswith('y')
if post_discord:
	discord_token      = _input('Discord MFA Token: ')
	discord_channel_id = _input('Channel ID: ')
	discord_content    =  input('What should be posted to discord (Any $$ found will be replaced with the challange link): ')

if shape.startswith('c'): shape = 'circles'
elif shape.startswith('s'): shape = 'squares'
elif shape.startswith('t'): shape = 'triangles'

if color.startswith('b'): color = 'gblue'
elif color.startswith('p'): color = 'purply'
elif color.startswith('r'): color = 'redish'
elif color.startswith('y'): color = 'yerange'
elif color.startswith('g'): color = 'pistagre'

cookies = {
	'session_id': session_id,
	'user_id': user_id
}

json = {
	'user_id': user_id,
	'user_shape': shape,
	'user_color': color,
	'session_id': session_id,
	'type': 'challenge'
}

if use_proxy:
	proxies = {
		'https': f'http://{proxy_ip}:{proxy_port}',
		'http':  f'http://{proxy_ip}:{proxy_port}'
	}
else:
	proxies = {}

headers = {
	'User-Agent': 'https://github.com/rozbrajaczpoziomow/yare.io-autochallange Agent'
}

resp = requests.post('https://yare.io/new-game', cookies=cookies, json=json, proxies=proxies, headers=headers, verify=0)
print('\n\n\n')

if not resp.ok:
	print('Something went wrong!')
	print(resp)
	print(resp.content)
	exit(1)

game = resp.json()['g_id']
url = f'https://yare.io/challenge/{game}'
copy(url)
if post_discord: discord(discord_token, discord_channel_id, discord_content.replace('$$', url))
print(f'URL: {url}')
print('\nWaiting for someone to join')

json = {
	'data': 'status check'
}

while 1:
	try: resp = requests.post(f'https://yare.io/check-status/{game}', cookies=cookies, json=json, proxies=proxies, headers=headers, verify=0)
	except: pass
	print(resp.status_code, end=',', flush=1)
	try:
		if resp.json()['data'] != 'not yet': break
	except: pass
	sleep(1.5)

server = resp.json()["server"]
game_url = f'https://yare.io/{server}/{game}'

print(f'\n{resp.json()["player2"]} joined!')

json = {
	'user_id': user_id,
	'session_id': session_id
}

requests.get(game_url.replace(f'/{server}/', f'/{server}n/'),   cookies=cookies, proxies=proxies, headers=headers, verify=0)
requests.post(game_url.replace(f'/{server}/', f'/{server}ns/'), cookies=cookies, json=json, proxies=proxies, headers=headers, verify=0)
requests.get(game_url, cookies=cookies, proxies=proxies, headers=headers, verify=0)

print(f'Game URL: {game_url}')
firefox(game_url)