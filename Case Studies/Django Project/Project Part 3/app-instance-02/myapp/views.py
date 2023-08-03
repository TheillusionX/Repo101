from django.shortcuts import render
import myapp.function_factory as ff

# globals variables

category = ""
request_list = {"No items as of now": 0}
items_per_category = {
    "": ["--Choose Category--"],
    "Money": ["money1", "money2"],
    "Food/Consumables": ["food1", "food2"],
    "Shelter": ["shelter1", "shelter2"],
    "Hygienic and Self-care Products": ["hygiene1", "hygiene2"],
    "Clothing/Wearables": ["cloth1", "cloth2"],
    "Medical Supplies": ["med1", "med2", "med3"]
}
user = {}
items_in_category = items_per_category[category]
signed_in = False

# view functions

def main_page(request):
    global signed_in, user

    if request.method == "POST" and "log_out" in request.POST:
        signed_in = False
    elif request.method == "POST" and "test" in request.POST:
        ff.test(request)

    return render(request, "main_page.html", {"signed_in": signed_in, "user": user})


def sign_up_page(request):
    message = ""
    clicked = False
    if request.method == "POST" and "name" in request.POST:
        global user, signed_in
        user, created = ff.sign_up(request)
        clicked = True
        signed_in = created
        if created:
            message = f"You are now signed in as {user['name']} {user['surname']}"
        else:
            message = f"Account with the same phone number already exists. Please log in."
    return render(request, "sign_up_page.html", {"user": user,
                                                 "clicked": clicked,
                                                 "message": message,
                                                 })


def log_in_page(request):
    global user, signed_in
    message = ""
    if request.method == "POST" and "name" in request.POST:
        user, signed_in = ff.log_in(request)
        if signed_in: message = f"You are now logged in as {user['name']} {user['surname']}."
        else: message = f"Incorrect or mismatching credentials, please try again."
    return render(request, "log_in_page.html", {"signed_in": signed_in,
                                                "message": message})


def inventory_page(request):
    inventory = ff.update_table()

    if request.method == "POST" and "update_table" in request.POST:
        inventory = ff.update_table()
    return render(request, "inventory_page.html", {"inventory": inventory,
                                                   })


def requests_page(request):
    global category, request_list, items_per_category, items_in_category, user
    request_received_message = ""

    if request.method != "POST":
        request_list = {"No items as of now": 0}
    elif request.method == "POST" and "categories" in request.POST:
        items_in_category = ff.list_items(request, items_in_category, items_per_category)
    elif request.method == "POST" and "add_item" in request.POST:
        request_list = ff.add_item(request, request_list)
    elif request.method == "POST" and "submit_request" in request.POST:
        request_list, request_received_message = ff.submit_request(request_list, user)

    return render(request, "requests_page.html", {"category": category,
                                                  "request_list": request_list,
                                                  "items_per_category": items_per_category,
                                                  "items_in_category": items_in_category,
                                                  "request_received_message": request_received_message})


def performance_page(request):
    districts, companies = ff.get_districts_n_companies()
    chosen_district = 0
    chosen_company = 0

    if request.method == "POST" and "district_id" in request.POST:
        chosen_district = ff.load_district_data(request)
    elif request.method == "POST" and "company" in request.POST:
        chosen_company = ff.load_company_data(request)
    else:
        chosen_district = 0
        chosen_company = 0
    return render(request, "performance_page.html", {"districts": districts,
                                                     "chosen_district": chosen_district,
                                                     "companies": companies,
                                                     "chosen_company": chosen_company})


'''{"districts": districts,
                                                     "name": name,
                                                     "coordination": coordination,
                                                     "population": population,
                                                     "district_id": district_id,
                                                     "companies": companies,
                                                     ""}'''

