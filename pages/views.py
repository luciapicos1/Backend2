from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import Itinerary, Destination, Accommodation
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

from .forms import ItineraryForm

def create_itinerary(request):
    if request.method == 'POST':
        form = ItineraryForm(request.POST)
        if form.is_valid():
            itinerary = form.save(commit=False)
            itinerary.save()
            return redirect('itinerary-list')  # Redirect to the itinerary list view
    else:
        form = ItineraryForm()
    return render(request, 'itinerary_create.html', {'form': form})

class DestinationListView(ListView):
    model = Destination
    template_name = 'destination_list.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        pais = self.request.GET.get('pais')  # Obtener el valor del parámetro 'pais' de la URL
        if pais:
            queryset = queryset.filter(pais__icontains=pais)  # Filtrar por país 
        return queryset

from django.db.models import Q
class AccommodationListView(ListView):
    model = Accommodation
    template_name = 'accommodation_list.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if min_price and max_price:
            queryset = queryset.filter(price__range=(min_price, max_price))
        elif min_price:
            queryset = queryset.filter(price__gte=min_price)
        elif max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile

from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Autenticar y loguear al usuario automáticamente
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            User.objects.create_user(username=username, password=password)
            user = authenticate(request, username=username, password=password)
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'register.html', context=context)



def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = UserLoginForm(request)
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home') 

@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'user_profile': user_profile})
 