from .models import Student
from django.views.generic import View
import json
from django.http import HttpResponse
from django.core.serializers import serialize
from .forms import StudentForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name="dispatch")
class StudentApi(View):
    
    def get(self, request, *args, **kwargs):
        sender_data = request.body
        print(">>>>>>>>>>>>>>", sender_data, ">>>>>>>>>>>>>>>>>")
        student_dict = json.loads(sender_data) 
        valid_json = True if student_dict else False
        if not valid_json:
            json_data = json.dumps({"message": "invalid JSON format"})
            return HttpResponse(json_data, content_type="application/json", status=404)
        
        id = student_dict.get('id', None)
        if id is not None:
            try:
                student = Student.objects.get(id=id)
            except Student.DoesNotExist:
                student = None

            
            if not student:
                json_data = json.dumps({"message": "Resource not available for given ID"})
                return HttpResponse(json_data, content_type="application/json", status=404)
            json_data = serialize('json', [student, ])
            p_dict = json.loads(json_data)
            final_list=[]
            for _ in p_dict:
                final_list.append(_['fields'])
            
            json_data = json.dumps(final_list)
            return HttpResponse(json_data, content_type="application/json", status=200)
        
        all_student = Student.objects.all()
        json_data = serialize('json', all_student)
        p_dict = json.loads(json_data)
        final_list=[]
        for _ in p_dict:
            final_list.append(_['fields'])
        json_data=json.dumps(final_list)
        return HttpResponse(json_data, content_type="application/json", status=200)



    def post(self, request, *agrs, **kwargs):

        sender_data = request.body
        print(">>>>>>>>>>>>>>", sender_data, ">>>>>>>>>>>>>>>>>")
        student_dict = json.loads(sender_data) 
        valid_json = True if student_dict else False
        if not valid_json:
            json_data = json.dumps({"message": "invalid JSON format"})
            return HttpResponse(json_data, content_type="application/json", status=404)
        
        form = StudentForm(student_dict)
        if form.is_valid():
            form.save()
            json_data = json.dumps({"message": "Successfully submitted"})
            return HttpResponse(json_data, content_type="application/json", status=200)

        json_data = json.dumps(form.errors)
        return HttpResponse(json_data, content_type="application/json", status=404)
    

    def put(self, request, *args, **kwargs):

        sender_data = request.body
        student_dict = json.loads(sender_data)
        valid_json = True if student_dict else False

        if not valid_json:
            json_data = json.dumps({"message": "invalid JSON format"})
            return HttpResponse(json_data, content_type="application/json", status=404)
        
        id = student_dict.get("id", None)

        if id is None:                  
            json_data = json.dumps({"message": "Invalid request, ID is required"})
            return HttpResponse(json_data, content_type="application/json", status=404)
        
        try:
            student = Student.objects.get(id=id) # instance
        except Student.DoesNotExist:
            student = None

        if student is None:
            json_data = json.dumps({"message": "No resource found for given ID"})
            return HttpResponse(json_data, content_type="application/json", status=404)
            
        original_data = {
            "name": student.name,
            "roll_number": student.roll_number,
            "gender": student.gender,
            "address": student.address,
        }

        original_data.update(student_dict)
        form = StudentForm(original_data, instance=student)

        if form.is_valid():
            form.save()
            json_data = json.dumps({"message": "Successfully updated"})
            return HttpResponse(json_data, content_type="application/json", status=200)

        json_data = json.dumps(form.errors)
        return HttpResponse(json_data, content_type="application/json", status=404)  



    def delete(self, request, *args, **kwargs):

        sender_data = request.body
        student_dict = json.loads(sender_data)
        valid_json = True if student_dict else False

        if not valid_json:
            json_data = json.dumps({"message": "invalid JSON format"})
            return HttpResponse(json_data, content_type="application/json", status=404)
        
        id = student_dict.get("id", None)

        if id is None:                  
            json_data = json.dumps({"message": "Invalid request, ID is required"})
            return HttpResponse(json_data, content_type="application/json", status=404)
        
        try:
            student = Student.objects.get(id=id) # instance
        except Student.DoesNotExist:
            student = None

        if student is None:
            json_data = json.dumps({"message": "No resource found for given ID"})
            return HttpResponse(json_data, content_type="application/json", status=404)
        
        status, deleted_student = student.delete()
        if status == 1:
            json_data = json.dumps({"message": "Deleted successfully"})
            return HttpResponse(json_data, content_type="application/json", status=200)

        json_data = json.dumps({"message": "Something went, try again"})
        return HttpResponse(json_data, content_type="application/json", status=404)      
