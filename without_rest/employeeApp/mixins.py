from django.http import HttpResponse
import json

class HttpResponseMixin(object):

    def return_http_response(self):
        DATA = {
            "employeeId": 10111,
            "employeeName": "Albert",
            "employeeLocation": "Somewhere",
            "employeeSalary": 1001010,
            "employeeDesignation": "Born",
        }
        
        json_data = json.dumps(DATA)
        return HttpResponse(json_data, content_type="application/json")