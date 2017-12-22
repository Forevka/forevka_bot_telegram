import requests
import hashlib
import json
import time

#сначала отправляем файл через файл_сенд и одновременно получаем ша-256 и потом по этой ша-256 получаем проверенный файл
def sha256sum(filename):
    """
    Efficient sha256 checksum realization
    Take in 8192 bytes each time
    The block size of sha256 is 512 bytes
    """
    with open(filename, 'rb') as f:
        m = hashlib.sha256()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def generate_report(sh):
	url_report = 'https://www.virustotal.com/vtapi/v2/file/report'
	params = {'apikey': '0f047e7e815c9bad90e497be312219600db92818666c6dd5e4bcea90e7241132', 'resource': sh}

	response = requests.get(url_report, params=params)

	return response.json()

def send_file(res):
	url_send = 'https://www.virustotal.com/vtapi/v2/file/scan'
	params = {'apikey': '0f047e7e815c9bad90e497be312219600db92818666c6dd5e4bcea90e7241132'}
	files = {'file': (res, open(res, 'rb'))}
	response = requests.post(url_send, files=files, params=params)
	return response.json()

def parse(fil):
	reply=send_file(fil)
	return reply["resource"] 

def virus_check(fil):
	reply=parse(fil)
	time.sleep(20)
	reply=generate_report(reply)
	reply="Через "+str(reply["total"])+" антивірусів пройдено"+"\nВірусов знайдено: "+str(reply["positives"])
	return reply
	
#print(virus_check("GML.exe"))
