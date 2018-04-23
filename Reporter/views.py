from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from Reporter.models import Detector, Sighting, CrimeNumber
from django.utils import timezone
from django.core.files.base import ContentFile
import base64


class LandingPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'landing.html', context=None)

    def post(self, request, **kwargs):
		# User Authentication
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
			# Logging the user in and redirecting to home page
            login(request, user)
            return redirect('HomePage')
        else:
			# Unsuccessful log in
            messages.error(request, "Login unsuccessful!")
            return render(request, 'landing.html', context=None)


class HomePage(TemplateView):
    def get(self, request, **kwargs):
		# Checking if user is authenticated before accessing home page
        if not request.user.is_authenticated:
            messages.error(request, "Please sign up or login!")
            return render(request, 'landing.html', context=None)
        else:
            return render(request, 'home.html', context={"user": request.user})


class LocBasedHomePage(TemplateView):
    def get(self, request, **kwargs):
		# Getting location of user
        if request.session.get('lat', None) is None:
            lat = float(request.GET.get('lat', ''))
            long = float(request.GET.get('long', ''))
            request.session['lat'] = str(lat)
            request.session['long'] = str(long)
        else:
            lat = float(request.session.get('lat'))
            long = float(request.session.get('long'))
		
		# Getting all the reported sightings and sorting them by distance
        sightings = Sighting.objects.all()
        sightings = sorted(sightings, key=lambda sighting: ((sighting.detector.latitude - lat) ** 2 + (
                    sighting.detector.longitude - long) ** 2)**0.5)

        return render(request, 'LocBasedHome.html', context={'sightings':sightings})


class DataPage(TemplateView):
    def get(self, request, **kwargs):
        messages.error(request, "Page inaccessible!")
        return render(request, 'landing.html', context=None)

    def post(self, request, **kwargs):
        try:
			# Creating a sighting if license plate number exists in crime database
            license_number = request.POST.get('license_number')
            number = CrimeNumber.objects.get(license_number=license_number)
            detector_id = request.POST.get('pk')
            encoded_image = request.POST.get('en_image')
            sighting = Sighting()
            sighting.license_number = license_number
            sighting.detector = Detector.objects.get(pk=detector_id)
            sighting.time = timezone.now()
            sighting.image = ContentFile(base64.b64decode(encoded_image), license_number + ".jpg")
            sighting.save()
        except:
            print("Detected number not in crime database!")

        return render(request, 'landing.html', context=None)


class AddNumbersPage(TemplateView):
    def get(self, request, **kwargs):
		# Checking if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "Please sign up or login!")
            return render(request, 'landing.html', context=None)
        else:
            return render(request, 'addNumber.html', context=None)

    def post(self, request, **kwargs):
		# Adding a license plate number to crime database
        license_number = request.POST.get('plate')
        crimeNumber = CrimeNumber()
        crimeNumber.license_number = license_number
        crimeNumber.date_added = timezone.now()
        crimeNumber.user = request.user.username
        crimeNumber.save()

        return redirect('CrimeDataPage')


class CrimeDataPage(TemplateView):
    def get(self, request, **kwargs):
		# Getting and sorting crime numbers by the data added
        numbers = CrimeNumber.objects.all().order_by(('-date_added'))

        return render(request, 'data.html', context={'CrimeNumbers':numbers})


def image(request):
	# Function to render an image
    pk = request.GET.get('pk', '')
    sighting = Sighting.objects.get(pk=pk)
    return render(request, 'image.html', context={'sighting':sighting})
