from django.http import HttpResponse, JsonResponse
import json
from django.views.generic import View # for class based views
from .mixins import HttpResponseMixin


def employeeDataView(request):
    data = {
        "employeeId": 10111,
        "employeeName": "Julian",
        "employeeLocation": "Central Jail",
        "employeeSalary": 1001010,
        "employeeDesignation": "God",
    }

    return HttpResponse("<h1> This is just a HTML response, which can't understood by another application except browser </h1>")


def employeeDataJsonView(request):
    data = {
        "employeeId": 10111,
        "employeeName": "Julian",
        "employeeLocation": "Central Jail",
        "employeeSalary": 1001010,
        "employeeDesignation": "God",
        "by": "import json",
    }
    json_data = json.dumps([data, ])
    return HttpResponse(json_data, content_type="application/json")


def employeeDataDjangoJsonView(request):
    data = {
        "employeeId": 10111,
        "employeeName": "Julian",
        "employeeLocation": "Central Jail",
        "employeeSalary": 1001010,
        "employeeDesignation": "God",
        "by": "from django.http import JsonResponse",
    }
    return JsonResponse(data)

#############################################  Below one have so much duplicate code ###############################

class JSONdata(View):

    def get(self, request, *args, **kwargs):
        data = {
        "employeeId": 10111,
        "employeeName": "Albert",
        "employeeLocation": "Somewhere",
        "employeeSalary": 1001010,
        "employeeDesignation": "Born",
        "by": "from django.views.generic import View",
        "from": "GET",
        }
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type="application/json")
        
    
    def post(self, request, *args, **kwargs):
        data = {
        "employeeId": 10111,
        "employeeName": "Albert",
        "employeeLocation": "Somewhere",
        "employeeSalary": 1001010,
        "employeeDesignation": "Born",
        "by": "from django.views.generic import View",
        "from": "POST",
        }
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type="application/json")
            
    def put(self, request, *args, **kwargs):
        data = {
        "employeeId": 10111,
        "employeeName": "Albert",
        "employeeLocation": "Somewhere",
        "employeeSalary": 1001010,
        "employeeDesignation": "Born",
        "by": "from django.views.generic import View",
        "from": "PUT",
        }
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type="application/json")
            
    def delete(self, request, *args, **kwargs):
        data = {
        "employeeId": 10111,
        "employeeName": "Albert",
        "employeeLocation": "Somewhere",
        "employeeSalary": 1001010,
        "employeeDesignation": "Born",
        "by": "from django.views.generic import View",
        "from": "DELETE",
        }        
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type="application/json")




################################# For above lets define mixins, to remove duplicate code ##############################



class JsonDataWithMixinView(HttpResponseMixin ,View):

    def get(self, request, *args, **kwargs):
        return self.return_http_response()

    def post(self, request, *args, **kwargs):
        return self.return_http_response()
        
    def put(self, request, *args, **kwargs):
        return self.return_http_response()
        
    def delete(self, request, *args, **kwargs):
        return self.return_http_response()
        