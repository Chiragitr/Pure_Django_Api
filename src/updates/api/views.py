import json

from django.views.generic import View
from django.http import HttpResponse
from updates.models import Update as UpdateModel
from updates.forms import UpdateModelForm

from .mixins import CSRFExemptMixin
from cfeapi.mixins import HttpResponseMixin
from .utils import is_json

#Creating ,Updating, Deleteing, Retrieving(1) -- Update Model


class UpdateModelDetailAPIView(HttpResponseMixin, CSRFExemptMixin, View):
	'''
	Retrieve, Update, Delete ---> Objects
	'''
	is_json = True

	def get_object(self, id=None):
		# Method 1		
		# try:
		# 	obj = UpdateModel.objects.get(id=id)
		# except UpdateModel.DoesNotExist:
		# 	obj = None
		# return obj
		
		# Method 2
		"""
		Below handles a Does Not Exist Exception too
		"""
		qs = UpdateModel.objects.filter(id=id)
		if qs.count() == 1:
			return qs.first()
		return None		


	def get(self, request, id, *args, **kwargs):
		#obj = UpdateModel.objects.get(id=id)
		obj = self.get_object(id=id)
		if obj is None:
			error_data = json.dumps({"message":"update not found"})
			return self.render_to_response(error_data, status=404)
		json_data = obj.serialize()
		#return HttpResponse(json_data, content_type='application/json') #json
		return self.render_to_response(json_data)

	def post(self, request, *args, **kwargs):
		json_data = json.dumps({"message" : "Not Allowed, Please use the api/updates/ endpoint"})
		#return HttpResponse({}, content_type='application/json')#json
		return self.render_to_response(json_data, status=403)

	def put(self, request, id, *args, **kwargs):
		valid_json = is_json(request.body)
		if not valid_json:
			error_data = json.dumps({"message":"Invalid data sent, please send using JSON"})
			return self.render_to_response(error_data, status=400)

		print("hello inside Put")
		obj = self.get_object(id=id)
		if obj is None:
			error_data = json.dumps({"message":"update not found"})
			return self.render_to_response(error_data, status=404)
		
		data = json.loads(obj.serialize())
		passed_data = json.loads(request.body)
		for key, value in passed_data.items():
			data[key] = value

		print("passed_data:", passed_data)
		print("serialize + passed_data: ", data)
		form = UpdateModelForm(data)
		
		if form.is_valid():
			obj = form.save(commit=True) #get obj back
			#obj_data = obj.serialize()
			obj_data = json.dumps(data)
			return self.render_to_response(obj_data, status=201)
		if form.errors:
			data = json.dumps(form.errors)
		#return HttpResponse(data, content_type='application/json')#json
			return self.render_to_response(data, status=400)

		print(dir(request))
		print(request.body)
			

		# new_data = json.loads(request.body)
		# print(new_data['content'])
		# print(request.POST)

		# wrong print(request.data)
		json_data = json.dumps({"message" : "Something"})
		#return HttpResponse({}, content_type='application/json')#json
		return self.render_to_response(json_data)

	def delete(self, request, id, *args, **kwargs):
		print("inside delete")
		obj = self.get_object(id=id)
		if obj is None:
			error_data = json.dumps({"message":"update not found"})
			return self.render_to_response(error_data, status=404)
		deleted_, item_deleted = obj.delete()
		print(deleted_)
		print(item_deleted)
		#print(x) not enough value to unpack
		if deleted_ == 1:
			json_data = json.dumps({"message" : "Successfully deleted"})
		#return HttpResponse({}, content_type='application/json')#json			
			return self.render_to_response(json_data, status=200)

		error_data = json.dumps({"message":"Could not delete item, please try again later"})
		return self.render_to_response(error_data, status=403)
			
'''
NOW We Have one END-POINT for all the CRUD 
/api/updates
'''
# AUTH / Permissions -- DJANGO REST FRAMEWORK we will do in DRF -- Don't USE Tastypie


class UpdateModelListAPIView(HttpResponseMixin, CSRFExemptMixin, View):
	'''
	List View --> Retrieve -- Detail View
	Create View
	Update
	Delete
	'''
	# def render_to_response(data, status=200):
	# 	return HttpResponse(data, content_type='application/json', status=status)#json
	is_json = True
	queryset = None

	def get_queryset(self):
		qs = UpdateModel.objects.all()
		self.queryset = qs
		return qs

	def get_object(self, id=None):
		# Method 1		
		# try:
		# 	obj = UpdateModel.objects.get(id=id)
		# except UpdateModel.DoesNotExist:
		# 	obj = None
		# return obj
		
		# Method 2
		"""
		Below handles a Does Not Exist Exception too
		"""

		if id is None:
			return None
		qs = self.get_queryset().filter(id=id)
		if qs.count() == 1:
			return qs.first()
		return None


	def get(self, request, *args, **kwargs):
		data = json.loads(request.body)
		passed_id = data.get('id', None)
		if passed_id is not None:
			print(passed_id)
			obj = self.get_object(id=passed_id)
			print(obj)
			if obj is None:
				error_data = json.dumps({"message":"Object not found"})
				return self.render_to_response(error_data, status=404)
			json_data = obj.serialize()
		#return HttpResponse(json_data, content_type='application/json') #json
			return self.render_to_response(json_data)
		else:
			qs = self.get_queryset()
			json_data = qs.serialize()
			#return HttpResponse(json_data, content_type='application/json')#json
			return self.render_to_response(json_data)

	def post(self, request, *args, **kwargs):
		print("Inside post")
		print(request.POST)
		
		valid_json = is_json(request.body)
		if not valid_json:
			error_data = json.dumps({"message":"Invalid data sent, please send using JSON"})
			return self.render_to_response(error_data, status=400)
		
		data = json.loads(request.body)
		form = UpdateModelForm(data)
		
		if form.is_valid():
			obj = form.save(commit=True) #get obj back
			obj_data = obj.serialize()
			return self.render_to_response(obj_data, status=201)
		if form.errors:
			data = json.dumps(form.errors)
		#return HttpResponse(data, content_type='application/json')#json
			return self.render_to_response(data, status=400)

		data = {"Message":"Not Allowed"}
		return self.render_to_response(data, status=400)

	# def delete(self, request, *args, **kwargs):
	# 	data = json.dumps({"message":"You cannot delete an entire list"})
	# 	#return HttpResponse(data, content_type='application/json')#json
	# 	return self.render_to_response(data, status=403)

	
	def put(self, request, *args, **kwargs):
		valid_json = is_json(request.body)
		if not valid_json:
			error_data = json.dumps({"message":"Invalid data sent, please send using JSON"})
			return self.render_to_response(error_data, status=400)

		passed_data = json.loads(request.body)
		passed_id = passed_data.get('id', None)

		if not passed_id:
			error_data = json.dumps({"id":"This is a required field to update an item"})
			return self.render_to_response(error_data, status=400)

		print("hello inside Put")
		obj = self.get_object(id=passed_id)
		if obj is None:
			error_data = json.dumps({"message":"Object not found"})
			return self.render_to_response(error_data, status=404)
		
		data = json.loads(obj.serialize())
		passed_data = json.loads(request.body)
		for key, value in passed_data.items():
			data[key] = value

		print("passed_data:", passed_data)
		print("serialize + passed_data: ", data)
		form = UpdateModelForm(data)
		
		if form.is_valid():
			obj = form.save(commit=True) #get obj back
			#obj_data = obj.serialize()
			obj_data = json.dumps(data)
			return self.render_to_response(obj_data, status=201)
		if form.errors:
			data = json.dumps(form.errors)
		#return HttpResponse(data, content_type='application/json')#json
			return self.render_to_response(data, status=400)

		print(dir(request))
		print(request.body)
			

		# new_data = json.loads(request.body)
		# print(new_data['content'])
		# print(request.POST)

		# wrong print(request.data)
		json_data = json.dumps({"message" : "Something"})
		#return HttpResponse({}, content_type='application/json')#json
		return self.render_to_response(json_data)

	def delete(self, request, *args, **kwargs):
		valid_json = is_json(request.body)
		if not valid_json:
			error_data = json.dumps({"message":"Invalid data sent, please send using JSON"})
			return self.render_to_response(error_data, status=400)

		passed_data = json.loads(request.body)
		passed_id = passed_data.get('id', None)

		if not passed_id:
			error_data = json.dumps({"id":"This is a required field to update an item"})
			return self.render_to_response(error_data, status=400)
		#print("hello inside Put")
		
		obj = self.get_object(id=passed_id)
		if obj is None:
			error_data = json.dumps({"message":"Object not found"})
			return self.render_to_response(error_data, status=404)
	

		# print("inside delete")
		# obj = self.get_object(id=id)
		# if obj is None:
		# 	error_data = json.dumps({"message":"update not found"})
		# 	return self.render_to_response(error_data, status=404)
		deleted_, item_deleted = obj.delete()
		print(deleted_)
		print(item_deleted)
		#print(x) not enough value to unpack
		if deleted_ == 1:
			json_data = json.dumps({"message" : "Successfully deleted"})
		#return HttpResponse({}, content_type='application/json')#json			
			return self.render_to_response(json_data, status=200)

		error_data = json.dumps({"message":"Could not delete item, please try again later"})
		return self.render_to_response(error_data, status=403)