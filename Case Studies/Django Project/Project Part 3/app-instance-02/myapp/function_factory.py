import myapp.data_manipulator as mp
import myapp.data_populator as pp
import myapp.image_factory as im_f
import myapp.validators as vld
import random

# Test
def test(request, *args):
    pp.run()

# Sign Up Page
def sign_up(request):

    data = request.POST
    name = data.get("name")
    surname = data.get("surname")
    phone_number = vld.validate_phone_number(data.get("phone_number"))
    district_id = int(data.get("districtID"))
    address = data.get("address")

    new_user = {
        "name": name,
        "surname": surname,
        "address": address,
        "phone_number": phone_number,
        "district_id": district_id,
    }

    new_user, created = mp.sign_up(new_user)

    return new_user, created

# Log in Page
def log_in(request):
    data = request.POST
    name = data.get("name")
    surname = data.get("surname")
    phone_number = vld.validate_phone_number(data.get("phone_number"))

    return mp.log_in(name, surname, phone_number)

# Requests Page
def add_item(request, req_list):
    data = request.POST
    item = data.get("items")
    try:
        quantity = int(data.get("quantity"))
        if item not in ["none", "", "None"]:
            if "No items as of now" in req_list:
                req_list = {item: quantity}
            else:
                req_list = req_list | {item: quantity}
    except:
        pass
    return req_list

def list_items(request, items_in_cat, items_per_cat):
    data = request.POST
    category = data.get("categories")
    try:
        items_in_cat = items_per_cat[category]
    except:
        pass

    return items_in_cat

def submit_request(request_list, user_det):
    requester_id = user_det["ID"]
    mp.add_request(request_list, requester_id)

    req_list = {"No items as of now": 0}
    return req_list, "Your request has been received."

# Inventory Page
def update_table():
    return mp.grab_inventory()

# Performance Page
def get_districts_n_companies():
    districts = mp.get_districts()
    companies = mp.get_companies()
    return districts, companies

def load_district_data(request):
    data = request.POST
    district_id = int(data.get("district_id"))
    district = mp.get_district(district_id)

    name = district.DistrictName
    coordination = (district.CoordinationX, district.CoordinationY)
    population = district.Population

    requests_to_district = mp.get_requests_to_districts(district)

    print(requests_to_district)

    im_f.district_data(district, requests_to_district)

    return {"id": district_id,
            "Name": name,
            "Coordination": coordination,
            "Population": population}

def load_company_data(request):
    data = request.POST
    company_id = int(data.get("company"))
    name = "Logisticality Man"
    phone_number = 234

    districts_data = {123: 45, 678: 9, 621: 65}
    requests_status = {"Pending": 34,
                       "On-time": 59,
                       "Late": 13}
    im_f.company_data(districts_data, requests_status, company_id, name)

    # SQL queries to get company name and phone number,
    # and number of requests and their status
    return company_id, name, phone_number
