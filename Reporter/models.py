from django.db import models


class Detector(models.Model):
    address = models.CharField(max_length=40)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.address


class Sighting(models.Model):
    detector = models.ForeignKey(Detector, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    time = models.DateTimeField()
    image = models.ImageField()

    def __str__(self):
        return self.license_number


class CrimeNumber(models.Model):
    license_number = models.CharField(max_length=10)
    date_added = models.DateTimeField()
    user = models.CharField(max_length=150)
	
	def __str__(self):
        return self.license_number