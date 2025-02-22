from django.shortcuts import render
import json
import random
from django.http import JsonResponse
from django.views import View
import os

# Charger les pays depuis le fichier JSON
def load_countries():
    file_path = os.path.join(os.path.dirname(__file__), 'data/countries.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

class GetRandomCountry(View):
    def get(self, request):
        countries = load_countries()
        selected_country = random.choice(countries)

        return JsonResponse({
            "country_name_fr": selected_country["name_fr"],  # Nom en français pour l'affichage
            "country_name_en": selected_country["name_en"]   # Nom en anglais pour Mapbox
        })

