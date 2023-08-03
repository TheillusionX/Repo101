import matplotlib.pyplot as plt
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def district_data(district, requests_to_district):
    district_id = district.DistrictID
    district_name = district.DistrictName

    print(requests_to_district)

    fig, ax = plt.subplots()

    pie_parts = [requests_to_district["Pending"],
                 requests_to_district["On-time"],
                 requests_to_district["Late"]]
    labels = list(requests_to_district)
    colors = ["gray", "green", "red"]
    ax.pie(pie_parts, labels=labels, autopct="%1.f%%", colors=colors)
    ax.set_title(f"Request Status of District {district_name} (ID: {district_id})\nTotal: {sum(pie_parts)}",
                 fontsize=16)
    plt.savefig(os.path.join(BASE_DIR, 'static\\district_pie.png'),
                bbox_inches="tight")


def company_data(districts_data, requests_status, company_id, name):
    fig, (ax1, ax2) = plt.subplots(1, 2, layout="constrained")
    pie_parts_requests = [requests_status["Pending"],
                          requests_status["On-time"],
                          requests_status["Late"]]

    labels = list(requests_status)
    colors = ["gray", "green", "red"]
    ax1.pie(pie_parts_requests, labels=labels, colors=colors, autopct="%1.f%%")
    ax1.set_title(f"Request Status\nTotal: {sum(pie_parts_requests)}")

    pie_parts_districts = [i for i in districts_data.values()]
    labels = list(districts_data)
    ax2.pie(pie_parts_districts, labels=labels, autopct="%1.f%%")
    ax2.set_title(f"Requests Completed to Districts\nTotal: {sum(pie_parts_districts)}")

    fig.suptitle(f"Performance of {name} (ID: {company_id})")

    plt.savefig(os.path.join(BASE_DIR, 'static\\company_pie.png'),
                bbox_inches="tight")
