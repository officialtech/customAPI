from django.views.generic import View
import requests
from .models import Student
import json
from django.http import HttpResponse
from django.core.serializers import serialize
from .mixins import SerializeMixin, HttpResponseMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import is_valid_json, get_object_by_id ############# custom utils ###########
from .forms import StudentForm
from pprint import pprint as p


class StudentView(View):
    def get(self, request, id, *args, **kwargs):
        student = Student.objects.get(id=id)
        student_dict_data = {
            'id': student.id,
            'roll_no': student.roll_no,
            'name': student.name,
            'address': student.address,
            'registration_no': student.registration_no,
        }
        student_json_data = json.dumps(student_dict_data)
        return HttpResponse(student_json_data, content_type="application/json")

################### Using Django Inbuilt serializers.serialize ############################

@method_decorator(csrf_exempt, name="dispatch")
class StudentDetailSerializeView(HttpResponseMixin, View):

    def get(self, request, id, *args, **kwargs):
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            json_data = json.dumps({'message': 'Object does not exist'})
            return self.render_to_http_response(json_data, status=404)

        else:
            json_data = serialize('json', [student, ], fields=['roll_no', 'name', 'address'])
            return self.render_to_http_response(json_data)


    def put(self, request, id, *args, **kwargs):
        student_data = request.body
        if not is_valid_json(student_data): # checking if given data is valid JSON data
            json_data = json.dumps({"message": "Invalid JSON format"})
            return self.render_to_http_response(json_data, status=404)

        student = get_object_by_id(id) # checking for is ID available in DB
        # if ID isn't available in DB
        if student is None:
            json_data = json.dumps({"message": "ID is not available"})
            return self.render_to_http_response(json_data, status=404)
        # if available then getting request data
        # if valid JSON data than converting that into Python Dictonary
        python_data = json.loads(student_data)
        # Below one is DB original data which will updated soon
        original_data = {
            "roll_no": student.roll_no,
            "name": student.name,
            "address": student.address,
            "registration_no": student.registration_no,
        }
        # updated data till now
        original_data.update(python_data)
        # to save data creating form (new*) object
        # form = StudentForm(original_data) # if you will keep it like this then it will create every time new entry to DB
        form = StudentForm(original_data, instance=student) # we are passing same instance, so it will update particular one only
        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({"message": "Updated Successfully"})
            return self.render_to_http_response(json_data)
        if form.errors():
            json_data = json.loads(form.errors)
            return self.render_to_http_response(json_data, status=404)


    ############################# delete ###########################
    def delete(self, request, id, *args, **kwargs):
        is_id_available = get_object_by_id(id)
        if not is_id_available:
            json_data = json.dumps({"message": "%s does not exist" % id})
            return self.render_to_http_response(json_data, status=404)
        status, deleted_item = is_id_available.delete() # beacuse it returns tuple of status and deleted object
        if status == 1:
            json_data = json.dumps({"message": "%s deleted successfully" % id})
            return self.render_to_http_response(json_data)
        
        json_data = json.dumps({"message": "unable to delete %s ... please try again" % id})
        return self.render_to_http_response(json_data, status=404)


            


#####################################################################

class StudentListSerializeView(HttpResponseMixin, SerializeMixin, View):

    def get(self, request, *args, **kwargs):
        list_queryset = Student.objects.all()
        json_data = self.serialize(list_queryset)
        return self.render_to_http_response(json_data)

######################################################################
@method_decorator(csrf_exempt, name='dispatch')
class StudentSerializePostView(HttpResponseMixin, View):
    def post(self, request, *args, **kwargs):
        data = request.body
        # print(dir(request))
        # p(data)
        if not is_valid_json(data):
            json_data = json.dumps({'message': 'Invalid JSON data'})
            return self.render_to_http_response(json_data, status=404)

        ################## now it's turn to save data, for that we need form ###################
        student_data = json.loads(data)
        form = StudentForm(student_data)
        # print(form)
        if form.errors:
            p(form.errors)
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status=404)
        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({"message": "Success"})
            return self.render_to_http_response(json_data)





"""
    As of now we learnt how to develop our own custom api from scratch
    but what `REST` or development approch says, is api should only have one `endpoint`
    but you can see here we used many `endpoints`
    like for:
        get all students ---> `/students/`
        get one student ---> `/student-detail/<int:id>/`
        post student data ---> `/post/`
        update student data ---> `/student-detail/<int:id>/`
        delete student data ---> `/student-detail/<int:id>/`

    As you can see we used 3 `endpoints` but we must and should have to use one
    -------------- SO LET'S DO THAT --------------
"""



class StudentApiView(HttpResponseMixin, SerializeMixin, View):
    """
        from django.views.generic import View
    """
    def get(self, request, *args, **kwargs):
        """
            1. Store send data `student_data`
            2. from .utils import is_valid_json
                check if given data is valid JSON or not
                from .mixins import `HttpResponseMixin`
            3. extract `ID` from that `student_data` else give `None`
            4. from .utils import get_object_by_id
                if `db_student` is none return json respose
                else return that particular ID related student
                from .mixins import SerializeMixin
            5. if `ID` is not available, it means we have to send all students data
        """
        student_data = request.body
        if not is_valid_json(student_data):
            json_data = json.dumps({"message": "Invalid JSON format"})
            return self.render_to_http_response(json_data, status=404)
        
        id = json.loads(student_data).get('id', None) # converting JSON into dictonary and getting ID
        if id is not None:
            # if ID is given
            db_student = get_object_by_id(id) # check if ID is present in DB or not
            if db_student is None:
                # if data is not available in DB
                json_data = json.dumps({"message": "%s is not available or Invalid" % id})
                return self.render_to_http_response(json_data, status=404)
            # else data is available in DB
            json_data = self.serialize([db_student, ]) # Never forget to pass list if you have one object only
            return self.render_to_http_response(json_data)
        # else ID is not given
        all_students_data = Student.objects.all()
        json_data = self.serialize(all_students_data) # if you have `list of objects` no need to pass list
        return self.render_to_http_response(json_data)
