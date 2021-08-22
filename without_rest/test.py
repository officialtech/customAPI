import requests
import json

BASE_URL = "http://localhost:8000/"
ENDPOINT = "api/student-data/"

# res = requests.get(BASE_URL+ENDPOINT)
# print(res) # <Response [200]>
# if res.status_code == requests.codes.ok:
    # data = res.json()
# else:
    # print("Soemthing Went Wrong...")
# print(data) # {'employeeId': 10111, 'employeeName': 'Julian', 'employeeLocation': 'Central Jail', 'employeeSalary': 1001010, 'employeeDesignation': 'God', 'by': 'from django.http import JsonResponse'}
# print(type(data))


print("-------------- sending post request ----------------")

def send_post_request():
    post_data = {
        "roll_no": -1,
        "name": "JB",
        "address": "Alabama",
        "registration_no": 1,
    }
    req = requests.post(BASE_URL+ENDPOINT, data=json.dumps(post_data))
    print(req.status_code)
    print(req.json())


print("-------------- sending put request ----------------")
def send_put_request(id):
    update_data = {
        "roll_no": 12,
        "name": "Moaana",
        "registration_no": 67544,
    }
    r = requests.put(BASE_URL+ENDPOINT+str(id), update_data)
    print(r.status_code)
    print(r.json())


print("-------------- sending delete request ----------------")

def send_delete_request(id):
    r = requests.delete(BASE_URL+ENDPOINT+str(id))
    print(r.status_code)
    print(r.json())

###########################################################################################################
#                                       API calls                                                         #
###########################################################################################################

print("********************* GET api/student-data/ *********************")
def get_api(id=None):
    data = {}
    if id is not None:
        data = {
            "id": id,
        }
    
    r = requests.get(BASE_URL+ENDPOINT, data=json.dumps(data))
    print(r.status_code)
    print(r.json())

# get_api()
# get_api(2)
# get_api(230)


print("********************* POST api/student-data/ *********************")

def post_api():
    """
        uncomment codes according to Numbers(1,2,3) and execute
    """
    # post_data = {
    #     "roll_no": 123,
    #     "name": "Boka",
    #     "address": "Nigiria",
    #     "registration_no": 855692,
    # }
    post_data = { # 3
        "roll_no": 0,
        "name": "The Leader",
        "address": "UAE",
        "registration_no": 90,
    }
    # r = requests.post(BASE_URL+ENDPOINT, json.dumps(post_data)) # 1 for success test
    # r = requests.post(BASE_URL+ENDPOINT, post_data) # 2 for failure test(Invalid JSON)
    r = requests.post(BASE_URL+ENDPOINT, json.dumps(post_data)) # 3 for form validation test
    print(r.status_code)
    print(r.json())

# post_api() # 1 2 3

""" 
# 1
python manage.py dumpdata studentModel.Student --indent 4
you can check data is successfully added by executing above command

"""  


print("********************* PUT api/student-data/ *********************")

def put_api(id):
    data = {
        "id": id,
        "name": "Dynamo",
        "address": "Manhatan London",
    }
    r = requests.put(BASE_URL+ENDPOINT, data=json.dumps(data))
    print(r.status_code)
    print(r.json())

# put_api(111)

print("********************* DELETE api/student-data/ *********************")

def delete_api(id):
    data = {
        "id": id,
    }

    r = requests.delete(BASE_URL+ENDPOINT, data=json.dumps(data))
    print(r.status_code)
    print(r.json())

# delete_api(3)
# delete_api(113)
