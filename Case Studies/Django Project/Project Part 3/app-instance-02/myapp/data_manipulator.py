from django.db.models import Prefetch
import myapp.models as md
import datetime as dt
import random


def random_id(num_of_digits, model):
    rand_id = random.randint(10 ** num_of_digits, 10 ** (num_of_digits + 1))
    pks = model.objects.values_list('pk', flat=True)
    primary_keys = list(pks)
    while rand_id in primary_keys:
        rand_id = random.randint(10 ** num_of_digits, 10 ** (num_of_digits + 1))
    return rand_id


def sign_up(new_user):
    if md.Victim.objects.filter(PhoneNumber=new_user["phone_number"]).exists():
        created = False
        new_user = {}
    else:
        v = md.Victim(VictimID=12345,
                      Name=new_user["name"],
                      Surname=new_user["surname"],
                      Address=new_user["address"],
                      PhoneNumber=new_user["phone_number"],
                      DistrictID=md.District.objects.get(pk=new_user["district_id"]))
        v.save()
        new_user["ID"] = v.VictimID
        created = True
    return new_user, created


def log_in(name, surname, phone_number):
    v = md.Victim.objects.get(PhoneNumber=phone_number)
    db_name = v.Name
    db_surname = v.Surname

    if name.lower() == db_name.lower() and surname.lower() == db_surname.lower():
        user = {
            "name": name,
            "surname": surname,
            "address": v.Address,
            "phone_number": phone_number,
            "district_id": v.DistrictID,
        }

        valid = True
    else:
        user = {}
        valid = False

    return user, valid


def add_request(request_list, requester_id):
    request_id = random_id(5, md.Request)
    r = md.Request(RequestID=request_id,
                   RequestTime=dt.date.today(),
                   CurrentStatus="Pending",
                   DeliveryTime=dt.date.today() + dt.timedelta(days=random.randint(10, 20)),
                   RequesterID=md.Victim.objects.get(pk=requester_id))
    r.save()
    for item, amount in request_list.items:
        req = md.Request_has_Items(RequestID=r,
                                   ItemID=item,
                                   Quantity=amount)
        req.save()


def grab_inventory():
    ret_dict = {}
    for item in md.Items.objects.all():
        ret_dict[item.ItemID] = {"Name": item.ItemID,
                                 "Category": item.ItemCategory,
                                 "Amount": item.Amount}
    return ret_dict


def get_districts():
    districts = md.District.objects.all()
    ret_dict = {}
    for dist in districts:
        ret_dict[dist.DistrictID] = dist.DistrictName
    return ret_dict


def get_companies():
    companies = md.LogisticsCompany.objects.all()
    ret_dict = {}
    for company in companies:
        ret_dict[company.CompanyID] = company.CompanyName
    return ret_dict


def get_district(district_id):
    return md.District.objects.get(pk=district_id)


def get_company(company_id):
    return md.LogisticsCompany.objects.get(pk=company_id)


def get_requests_to_districts(district):
    def status_grabber(status):
        q = md.Request.objects.prefetch_related(
            Prefetch("Victim",
                     queryset=md.Victim.objects.filter(DistrictID=district.DistrictID))
        ).filter(CurrentStatus=status)
        print(q.query, "\n")
        return q.count()

    return {"Pending": status_grabber("Pending"),
            "On-time": status_grabber("On-time"),
            "Late": status_grabber("Late")}

def get_requests_to_companies(company):
    def status_grabber(status):
        return md.Request.objects.filter(CurrentStatus=status,
                                         logisticscompany_has_districts__companyid=company.companyID).count()

    return {"Pending": status_grabber("Pending"),
            "On-time": status_grabber("On-time"),
            "Late": status_grabber("Late")}
