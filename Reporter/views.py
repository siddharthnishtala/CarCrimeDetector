from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from Reporter.models import Detector, Sighting
from django.utils import timezone
from django.core.files.base import ContentFile
import base64


class LandingPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'landing.html', context=None)

    def post(self, request, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('HomePage')
        else:
            messages.error(request, "Login unsuccessful!")
            return render(request, 'landing.html', context=None)


class HomePage(TemplateView):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please sign up or login!")
            return render(request, 'landing.html', context=None)
        else:
            return render(request, 'home.html', context={"user": request.user})


class LocBasedHomePage(TemplateView):
    def get(self, request, **kwargs):

        lat = float(request.GET.get('lat',''))
        long = float(request.GET.get('long',''))

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
            license_number = request.POST.get('license_number')
            detector_id = request.POST.get('pk')
            encoded_image = request.POST.get('en_image')
            sighting = Sighting()
            sighting.license_number = license_number
            sighting.detector = Detector.objects.get(pk=detector_id)
            sighting.time = timezone.now()
            sighting.image = ContentFile(base64.b64decode(encoded_image), license_number + ".jpg")
            sighting.save()
        except:
            print("Could not process request!")

        return render(request, 'landing.html', context=None)


def image(request):
    pk = request.GET.get('pk', '')
    sighting = Sighting.objects.get(pk=pk)
    return render(request, 'image.html', context={'sighting':sighting})
