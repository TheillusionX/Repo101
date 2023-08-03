from django.db import models
from django.core.exceptions import ValidationError
from .validators import *
from django.utils.translation import gettext as _

# Create your models here.
class Victim(models.Model):
    VictimID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=225)
    Surname = models.CharField(max_length=225)
    Address = models.CharField(max_length=225)
    PhoneNumber = models.PositiveIntegerField(unique=True)
    DistrictID = models.ForeignKey("District", on_delete = models.DO_NOTHING)

    def clean(self):
        ID = self.VictimID
        if validate_int(ID, 5):
            raise ValidationError(_(f"ID ({ID}) should be between {10**5} and {10**6 - 1}"))

class Request(models.Model):
    RequestID = models.IntegerField(primary_key=True)
    RequestTime = models.DateTimeField()
    CurrentStatus = models.CharField(max_length=45)
    DeliveryTime = models.DateTimeField()
    RequesterID = models.ForeignKey("Victim", on_delete=models.CASCADE)

    def clean(self):
        ID = self.RequestID
        if validate_int(ID, 5):
            raise ValidationError(_(f"ID ({ID}) should be between {10**5} and {10**6 - 1}"))

    def __str__(self):
        return str(self.RequestID)

class Items(models.Model):
    ItemID = models.CharField(primary_key=True, max_length=45)
    ItemCategory = models.CharField(max_length=45)
    Amount = models.IntegerField()


class Donation(models.Model):
    DonationID = models.IntegerField(primary_key=True)
    DonationTime = models.DateTimeField()
    DonationDeliveryTime = models.DateTimeField()
    RequestID = models.ForeignKey("Request", on_delete=models.CASCADE)
    DonorID = models.ForeignKey("Donor", on_delete=models.CASCADE)

    def clean(self):
        ID = self.DonationID
        if validate_int(ID, 5):
            raise ValidationError(_(f"ID ({ID}) should be between {10**5} and {10**6 - 1}"))


class Purchase(models.Model):
    PurchaseID = models.IntegerField(primary_key=True)
    TransactionCost = models.DecimalField(max_digits=4, decimal_places=1)

    def clean(self):
        ID = self.PurchaseID
        if validate_int(ID, 5):
            raise ValidationError(_(f"ID ({ID}) should be between {10**5} and {10**6 - 1}"))


class Request_has_Items(models.Model):
    RequestID = models.ForeignKey("Request", on_delete=models.CASCADE)
    ItemID = models.ForeignKey("Items", on_delete=models.CASCADE)
    Quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['RequestID', 'ItemID'],
                                    name='unique_request_item')
        ]

class Donation_has_Items(models.Model):
    DonationID = models.ForeignKey("Donation", on_delete=models.CASCADE)
    ItemID = models.ForeignKey("Items", on_delete=models.CASCADE)
    Quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['DonationID', 'ItemID'],
                                    name='unique_donation_item')
        ]

class Purchase_has_Items(models.Model):
    PurchaseTransactionID = models.ForeignKey("Purchase", on_delete=models.CASCADE)
    ItemID = models.ForeignKey("Items", on_delete=models.CASCADE)
    Amount = models.IntegerField()
    UnitItemCost = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['PurchaseTransactionID', 'ItemID'],
                                    name='unique_transaction_item')
        ]

class District(models.Model):
    DistrictID = models.IntegerField(primary_key=True)
    DistrictName = models.CharField(max_length=45)
    CoordinationX = models.PositiveIntegerField()
    CoordinationY = models.PositiveIntegerField()
    Population = models.IntegerField()

    def clean(self):
        ID = self.DistrictID
        if validate_int(ID, 5):
            raise ValidationError(_(f"ID ({ID}) should be between {10**5} and {10**6 - 1}"))



class Donor(models.Model):
    DonorID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=225)
    Surname = models.CharField(max_length=225)
    Phone = models.CharField(max_length=45)

    def clean(self):
        ID = self.DonorID
        if validate_int(ID, 5):
            raise ValidationError(_(f"ID ({ID}) should be between {10**5} and {10**6 - 1}"))


class Supplier(models.Model):
    SupplierID = models.IntegerField(primary_key=True)
    SupplierName = models.CharField(max_length=45)
    Phone = models.CharField(max_length=45)

    def clean(self):
        ID = self.SupplierID
        if validate_int(ID, 5):
            raise ValidationError(_(f"ID ({ID}) should be between {10**5} and {10**6 - 1}"))


class LogisticsCompany(models.Model):
    CompanyID = models.IntegerField(primary_key=True)
    CompanyName = models.CharField(max_length=45)
    Phone = models.CharField(max_length=45)

    def clean(self):
        ID = self.CompanyID
        if validate_int(ID, 5):
            raise ValidationError(_(f"ID ({ID}) should be between {10**5} and {10**6 - 1}"))


class LogisticsCompany_has_Districts(models.Model):
    CompanyID = models.ForeignKey("LogisticsCompany", on_delete=models.CASCADE)
    DistrictID = models.ForeignKey("District", on_delete=models.CASCADE)
    CostOfOutsource = models.DecimalField(max_digits=4, decimal_places=1)

class Courier(models.Model):
    CourierID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=45)
    Surname = models.CharField(max_length=45)
    Phone = models.CharField(max_length=45)
    LicenseType = models.CharField(max_length=45)

    def clean(self):
        ID = self.CourierID
        if validate_int(ID, 5):
            raise ValidationError(_(f"ID ({ID}) should be between {10**5} and {10**6 - 1}"))


class Vehicle(models.Model):
    VehicleID = models.IntegerField(primary_key=True)
    VehicleType = models.CharField(max_length=45)
    Capacity = models.IntegerField()

    def clean(self):
        ID = self.VehicleID
        if validate_int(ID, 5):
            raise ValidationError(_(f"ID ({ID}) should be between {10**5} and {10**6 - 1}"))



class Request_Vehicle_Courier_Assignment(models.Model):
    RequestID = models.ForeignKey("Request", on_delete=models.CASCADE)
    CourierID = models.ForeignKey("Courier", on_delete=models.CASCADE)
    VehicleID = models.ForeignKey("Vehicle", on_delete=models.CASCADE)
    DeliveryTime = models.DateTimeField()

class Request_has_LogisticsCompany(models.Model):
    RequestID = models.ForeignKey("Request", on_delete=models.CASCADE)
    CompanyID = models.ForeignKey("LogisticsCompany", on_delete=models.CASCADE)
    DeliveryTime = models.DateTimeField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['CompanyID', 'RequestID'],
                                               name='unique_company_request')]

class Currency(models.Model):
    CurrencyID = models.IntegerField(primary_key=True)
    ExchangeRate = models.DecimalField(max_digits=3, decimal_places=1)

    def clean(self):
        ID = self.CurrencyID
        if validate_int(ID, 5):
            raise ValidationError(_(f"ID ({ID}) should be between {10**5} and {10**6 - 1}"))


class Donation_has_Currency(models.Model):
    DonationID = models.OneToOneField("Donation", primary_key=True, on_delete=models.CASCADE)
    CurrencyType = models.ForeignKey("Currency", on_delete=models.CASCADE)
    Amount = models.IntegerField()

class Purchase_has_Supplier(models.Model):
    PurchaseTransactionID = models.OneToOneField("Purchase",
                                                 on_delete=models.CASCADE)
    SupplierID = models.ForeignKey("Supplier", on_delete=models.CASCADE)
