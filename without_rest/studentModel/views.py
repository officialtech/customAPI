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


######################################################## API ########################################################


"""
    As of now we learnt how to develop our own custom api from scratch
    but what `REST` or development approch says, ...is api should only have one `endpoint`
    but you can see here we used many `endpoints`
    like for:
        get all students ---> `/students/`
        get one student ---> `/student-detail/<int:id>/`
        post student data ---> `/post/`
        update student data ---> `/student-detail/<int:id>/`
        delete student data ---> `/student-detail/<int:id>/`

    As you can see we used 3 `endpoints` but we must and should have to use one
    
    ---------------------------- SO LET'S DO IT ----------------------------

    ----------------- for testing these, consider `test.py` -----------------
"""


@method_decorator(csrf_exempt, name="dispatch") # adding decorator to avoid CSRF 403
class StudentApiView(HttpResponseMixin, SerializeMixin, View):
    """
        from django.views.generic import View
    """
######################################################## GET ########################################################

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


    """
        Now we will perform `post` request, so be with me, try to map all of these with real scenario
        In POST request what we need only `data` to post nothing else

        to avoid CSRF 403 error first of all add:
            from django.utils.decorator import method_decorator
            from dajngo.views.decorator.csrf import csrf_exempt
            @method_decorator(csrf_exempt, name="dispatch)
    """
######################################################## POST ########################################################

    def post(self, request, *args, **kwargs):
        """
            1. Getting student POST data `student_data`
            2. check for vaild JSON `valid_json`
            3. converting to python dictonary from JSON `dict_data`
            4. Passing that data to the form Object (forms.py)
                if form is valid than save that
                if errors show that
        """
        student_data = request.body # 1
        
        valid_json = is_valid_json(student_data) # 2
        if not valid_json:
            json_data = json.dumps({"message": "Invalid JSON format"})
            return self.render_to_http_response(json_data, status=404)
        
        dict_data = json.loads(student_data) # 3

        form = StudentForm(dict_data) # 4
        if form.is_valid():
            form.save()
            json_data = json.dumps({"message": "Successfully created"})
            return self.render_to_http_response(json_data)
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status=404)
    

    """
        Now we will perform `PUT` request
        most of the code is already written in get and post method
        so we will get from that ctrl c, ctl v
    """
######################################################## PUT ########################################################

    def put(self, request, *args, **kwargs):
        send_data = request.body
        valid_json = is_valid_json(send_data)
        if not valid_json:
            json_data = json.dumps({"message": "Invalid JSON data"})
            return self.render_to_http_response(json_data, status=404)
        
        provided_dict = json.loads(send_data)
        id = provided_dict.get('id', None)
        

        if id is None:
            json_data = json.dumps({"message": "ID is required to update"})
            return self.render_to_http_response(json_data, status=404)

        student_data = get_object_by_id(id) # instanse
        if student_data is None:
            json_data = json.dumps({"message": "Requested data not available, check ID"})
            return self.render_to_http_response(json_data, status=404)

        original_data = {
            "roll_no": student_data.roll_no,
            "name": student_data.name,
            "address": student_data.address,
            "registration_no": student_data.registration_no,
        }
        original_data.update(provided_dict)
        form = StudentForm(original_data, instance=student_data) # never forget to pass instance else it will create new entry
        if form.is_valid():
            form.save()
            json_data = json.dumps({"message": "Updated successfully"})
            return self.render_to_http_response(json_data)
        
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status=404)


    """
        Now we will perform `delete` request
        as in PUT, in DELETE also we need ID to delete particular data

    """
######################################################## DELETE ########################################################

    def delete(self, request, *args, **kwargs):
        send_data = request.body
        if not is_valid_json(send_data):
            json_data = json.dumps({"message": "Invalid JSON data"})
            return self.render_to_http_response(json_data, status=404)
        
        in_dict = json.loads(send_data)
        id = in_dict.get('id', None)

        if id is None:
            json_data = json.dumps({"message": "ID is required to delete"})
            return self.render_to_http_response(json_data, status=404)

        student_data = get_object_by_id(id)
        if student_data is None:
            json_data = json.dumps({"message": "Requested data not available, Invalid ID"})
            return self.render_to_http_response(json_data, status=404)
        """
            When you delete then delete method return tuple, `(1, {'studentModel.Student': 1})`
            which contain `status = 0 or 1`
                0 or failed
                1 or success
            Second is deleted item {'studentModel.Student': 1}
        """
        status, deleted_item = student_data.delete()
        if status == 1:
            json_data = json.dumps({"message": "Deleted successfully"})
            return self.render_to_http_response(json_data)

        json_data = json.dumps({"message": "unable to delete, please cross check"})
        return self.render_to_http_response(json_data, status=404)
