import myapp.models as md
import datetime as dt
import random


def run():
    district = md.District(DistrictID=12345,
                           DistrictName=helper("DistrictName"),
                           CoordinationX=helper_int(3),
                           CoordinationY=helper_int(3),
                           Population=helper_int(10 ** 3, 10 ** 9))
    district.save()
    for i in range(0, 100):
        district = md.District(DistrictID=generate_id(md.District),
                               DistrictName=helper("DistrictName"),
                               CoordinationX=helper_int(3),
                               CoordinationY=helper_int(3),
                               Population=helper_int(10 ** 3, 10 ** 9))
        district.save()

        victim = md.Victim(VictimID=generate_id(md.Victim),
                           Name=helper("Victim"),
                           Surname=helper("Surname"),
                           Address=helper("Address", 6),
                           PhoneNumber=helper_int(12),
                           DistrictID=pick_random(md.District))
        victim.save()

        req = md.Request(RequestID=generate_id(md.Request),
                         RequestTime=helper_date(),
                         CurrentStatus=["Pending", "On-time", "Late"][random.randint(0, 2)],
                         RequesterID=pick_random(md.Victim))
        req.DeliveryTime = helper_date(req.RequestTime)
        req.save()

        cour = md.Courier(CourierID=generate_id(md.Courier),
                          Name=helper("Courier"),
                          Surname=helper("Surname"),
                          Phone=helper("+", 12),
                          LicenseType=helper("License"))
        cour.save()

        veh = md.Vehicle(VehicleID=generate_id(md.Vehicle),
                         VehicleType=helper("Vehicle"),
                         Capacity=helper_int(3))
        veh.save()

        rhc = md.Request_Vehicle_Courier_Assignment(RequestID=pick_random(md.Request),
                                                    CourierID=pick_random(md.Courier),
                                                    VehicleID=pick_random(md.Vehicle))
        rhc.DeliveryTime = md.Request.objects.get(pk=rhc.RequestID.RequestID).DeliveryTime
        rhc.save()

        lc = md.LogisticsCompany(CompanyID=generate_id(md.LogisticsCompany),
                                 CompanyName=helper("LogisticsCompany"),
                                 Phone=helper("+", 12))
        lc.save()

        lcd = md.LogisticsCompany_has_Districts(CompanyID=pick_random(md.LogisticsCompany),
                                                DistrictID=pick_random(md.District),
                                                CostOfOutsource=helper_int(2))
        lcd.save()

        rlc = md.Request_has_LogisticsCompany(RequestID=pick_random(md.Request),
                                              CompanyID=pick_random(md.LogisticsCompany),
                                              )
        rlc.DeliveryTime = rlc.RequestID.DeliveryTime
        rlc.save()


def helper(root, number=5):
    ret_string = root + str(random.randint(10 ** number, 10 ** (number + 1) - 1))
    return ret_string


def helper_int(number=5, limit=None):
    if limit is None:
        return random.randint(10 ** number, 10 ** (number + 1) - 1)
    else:
        return random.randint(number, limit)

def helper_date(start=dt.datetime.now(), max_addition=14*24):
    return start + dt.timedelta(hours=random.randint(max_addition//2, max_addition))

def generate_id(model, number=5):
    id_val = random.randint(10 ** number, 10 ** (number + 1) - 1)
    while id_val in model.objects.values_list("pk", flat=True):
        id_val = random.randint(10 ** number, 10 ** (number + 1) - 1)
    return id_val

def pick_random(model):
    pk_list = list(model.objects.values_list("pk", flat=True))
    picked_pk = pk_list[random.randint(0, len(pk_list) - 1)]
    return model.objects.get(pk=picked_pk)
