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


print("********************* GET *********************")
def get_api(id=None):
    data = {}
    if id is not None:
        data = {
            "id": id,
        }
    
    r = requests.get(BASE_URL+ENDPOINT, data=json.dumps(data))
    print(r.status_code)
    print(r.json())

get_api()