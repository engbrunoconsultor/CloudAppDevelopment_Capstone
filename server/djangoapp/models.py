from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    founded_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'SEDAN'
    SUV = 'SUV'
    WAGON = 'WAGON'
    CONVERTIBLE = 'CONVERTIBLE'
    COUPE = 'COUPE'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (CONVERTIBLE, 'Convertible'),
        (COUPE, 'Coupe'),
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dealer_id = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    year = models.DateField()

    def __str__(self):
        # String representation of the CarModel object
        return f"{self.name} - {self.type} ({self.year.year})"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    st = models.CharField(max_length=2)
    zip = models.CharField(max_length=12)
    lat = models.FloatField()
    long = models.FloatField()

    def __str__(self):
        return f"{self.city}, {self.state}"

# <HINT> Create a plain Python class `DealerReview` to hold review data
class Review(models.Model):
    name = models.CharField(max_length=100)
    dealership = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    review = models.TextField()
    purchase = models.BooleanField()
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.dealership}"
