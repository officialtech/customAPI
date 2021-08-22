
import json
from .models import Student # hard

def is_valid_json(data):
    try:
        json_data = json.loads(data)
        valid = True
    except ValueError:
        valid = False
    
    return valid


def get_object_by_id(id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        student = None
    return student
