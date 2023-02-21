import requests
from bs4 import BeautifulSoup
import pandas

price = []
areas = []
addresses = []
bed_num = []
full_bath_num = []
half_bath_num = []
lot_size = []

r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/",
                 headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content
c = BeautifulSoup(c, "html.parser")
div = c.find_all("div", {"class" : "propertyRow"})
# print(div[0])

for part in div:
    # to get prices
    price.append(part.find("h4", {"class" : "propPrice"}).text.replace("\n", "").replace(" ", ""))
    # to get areas
    try:
        areas.append(part.find("span", {"class" : "infoSqFt"}).text.replace(",", "").replace(" Sq. Ft", ""))
    except:
        areas.append("No info on area")
    # to get addresses
    addresses.append(f'{part.find_all("span", {"class" : "propAddressCollapse"})[0].text}; {part.find_all("span", {"class" : "propAddressCollapse"})[1].text}')
    # to get number of bedrooms
    try:
        bed_num.append(part.find("span", {"class" : "infoBed"}).text)
    except:
        bed_num.append("No information on beds")
    # to get number of full baths
    try:
        full_bath_num.append(part.find("span", {"class" : "infoValueFullBath"}).text)
    except:
        full_bath_num.append("0 full baths")
    # to get number of half baths
    try:
        half_bath_num.append(part.find("span", {"class" : "infoValueHalfBath"}).text)
    except:
        half_bath_num.append("0 half baths")

    i = 0
    for column in part.find_all("div", {"class" : "columnGroup"}):
        for feature_group, feature_name in zip(column.find_all("span", {"class" : "featureGroup"}), column.find_all("span", {"class" : "featureName"})):
            #print(feature_group.text)
            if "Lot Size" in feature_group.text:
                i = i + 1
                lot_size.append(f"Lot Size: {feature_name.text.replace(',', '')}")
    if i == 0:
        lot_size.append("No lot or no info")

"""""
print(price)
print(areas)
print(addresses)
print(bed_num)
print(full_bath_num)
print(half_bath_num)
print(lot_size)
"""

data = pandas.DataFrame(columns = ["Pricing", "Area", "Address", "Beds", "Baths", "Lot Size"])
data["Pricing"] = price
data["Area"] = areas
data["Address"] = addresses
data["Beds"] = bed_num
data["Baths"] = [f"{full} and {half}" for full, half in zip(full_bath_num, half_bath_num)]
data["Lot Size"] = lot_size

data.to_csv("RealEstate.csv")