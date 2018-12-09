import requests #http requests
import json

BASE_URL = "http://127.0.0.1:8000/"

ENDPOINT = "api/updates/"

def get_list(id='122'):#--> lists all this out
	data = json.dumps({"id":id})
	r = requests.get(BASE_URL + ENDPOINT, data=data)
	print(r.status_code)
	status_code = r.status_code
	if status_code != 200:
		print('Probably not a good sign?')

	data = r.json()
	# print(data)
	# print(type(json.dumps(data)))
	# for obj in data:
	# 	#print(obj['content'])
	# 	if obj['id'] == 1:#--> user interaction
	# 		r2 = requests.get(BASE_URL + ENDPOINT + str(obj['id']))
	# 		print(r2.json())
	return data

print(get_list())

def create_update():
	new_data = {
	'user':1,
	'content': 'Amore cool content chirag'
	}
	r = requests.post(BASE_URL + ENDPOINT, data=json.dumps(new_data))
	print(r.headers)
	print(r.status_code)
	if r.status_code == requests.codes.ok:
		print(r.json())
		return r.json
	return r.text

#print(create_update())

def do_obj_update():
	new_data = {
	'id' : '19',
	'content': 'hello Buddy chirag'
	}
	r = requests.put(BASE_URL + ENDPOINT , data=json.dumps(new_data))
	
	print(r.headers)
	print(r.status_code)
	if r.status_code == requests.codes.ok:
		print(r.json())
		data = r.json()
		print(data['message'])
		return r.json
	return r.text

#print(do_obj_update())

def do_obj_delete():
	new_data = {
	'id' : '19' ,
	'content': 'New obj data'
	}
	r = requests.delete(BASE_URL + ENDPOINT , data=json.dumps(new_data))
	
	print(r.headers)
	print(r.status_code)
	if r.status_code == requests.codes.ok:
		print(r.json())
		# data = r.json()
		# print(data['message'])
		return r.json
	return r.text

#print(do_obj_delete())
