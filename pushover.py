import urllib, json
import urllib.parse
import urllib.request
import os

from configloader import getconfig
config = getconfig()


def sanitizeStringEncoding(s, encoding='utf-8'):
	try: s = s.decode(encoding, errors="replace")
	except: pass
	try: s = s.encode(encoding, errors="replace")
	except: pass
	return s

class PushoverError(Exception): pass

def pushover(message, token=config["PUSHOVER_TOKEN"], user=config["PUSHOVER_USER"]):
	try:
		if not config["USE_PUSHOVER"]:
			return

		kwargs = {}
		kwargs['token'] = token
		kwargs['user'] = user
		kwargs['message'] = sanitizeStringEncoding(message)
		
		url = urllib.parse.urljoin(config["PUSHOVER_API"], "messages.json")
		data = urllib.parse.urlencode(kwargs)
		response = requests.post(url, kwargs)
		data = response.json()
		if data['status'] != 1:
			raise PushoverError()
		return True
	except PushoverError:
		print("Rejected by Pushover")
		return False
	except:
		print("Pushover error ocurred")
		return False
