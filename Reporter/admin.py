from django.contrib import admin
from .models import Detector, Sighting, CrimeNumber

admin.site.register(Detector)
admin.site.register(Sighting)
admin.site.register(CrimeNumber)