from django.http import JsonResponse
from django.shortcuts import render

from .forms import QueryForm, UserPreferencesForm
from .logic import intents, suggestions
from .models import Response, UserPreferences

from collections import defaultdict

import json
import os
import requests

import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '/../../scraper'))


def index(request):
    """
    :param request: A HTTP request
    :return: A rendering of the index.html template
    """
    return render(request, 'index.html')


def chat(request):
    """
    :param request: A HTTP request
    :return: Either a rendering of chat.html, or JSON containing the response to a user's query.
    """
    history = Response.objects.all()
    response = defaultdict()

    # get the user's preferences model, or create a default one if UserPreferences do not exist
    preferences = UserPreferences.objects.all().first()

    if preferences == None:
        preferences = UserPreferences.objects.create()
        preferences.save()

    attributes = []

    for field in preferences._meta.get_fields():
        if field.get_internal_type() == 'BooleanField' \
                and field.name != 'voice' and getattr(preferences, field.name):
            attributes.append(field.name)

    try:
        if request.method == 'POST':
            form = QueryForm(request.POST)

            if form.is_valid():
                query = form.save()
                question = form.cleaned_data['question']

                dialogflow_key = os.environ.get('DIALOGFLOW_CLIENT_ACCESS_TOKEN')
                dialogflow_api = 'https://api.dialogflow.com/v1/query?v=20150910'
                headers = {'Authorization': 'Bearer ' + dialogflow_key,
                           'Content-Type': 'application/json'}
                payload = json.dumps({
                    "lang": "en",
                    "query": question,
                    "sessionId": "12345",
                    "timezone": "Africa/Casablacontent_type='application/xhtml+xml'nca"
                })

                r = requests.post(dialogflow_api, headers=headers, data=payload)
                r = r.json()

                # SubSector must come before Sector!
                intent = r['result']['metadata']['intentName']

                if r['result']['action'] == "input.unknown":
                    response['text'] = r['result']['fulfillment']['speech']
                    response['type'] = 'simple.response'
                    response['speech'] = r['result']['fulfillment']['speech']
                else:
                    if 'Footsie' in intent:
                        response = intents.footsie_intent(r, preferences.days_old)
                    elif 'ComparisonIntent' in intent:
                        response = intents.comparison_intent(r)
                    elif 'SubSectorQuery' in intent:
                        response = intents.sector_query_intent(r, False, preferences.days_old)
                    elif 'SectorQuery' in intent:
                        response = intents.sector_query_intent(r, True, preferences.days_old)
                    elif 'TopRisers' in intent:
                        response = intents.top_risers_intent(r)
                    elif 'Daily Briefing' in intent:
                        response = intents.daily_briefings_intent(preferences.companies,
                                   preferences.sectors, attributes, preferences.days_old)
                    else:
                        response['text'] = r['result']['fulfillment']['speech']
                        response['speech'] = r['result']['fulfillment']['speech']
                        response['type'] = 'simple.response'

                reply = Response(query=query, response=json.dumps(response))
                reply.save()

                if response['type'] not in ('comparison', 'briefing', 'input.unknown', 'incomplete', 'simple.response'):
                    response = suggestions.add_suggestions(response, r)

                form = QueryForm()
        else:
            form = QueryForm()
    except:
        message = 'Ooops. Something went wrong.'
        response['text'] = message
        response['speech'] = message
        response['type'] = 'error'

    if request.is_ajax():
        return JsonResponse(response)
    else:
        return render(request, 'chat.html',
                      {'form': form, 'history': history, 'colour_scheme': preferences.colour_scheme})


def settings(request):
    """
    :param request: A HTTP request.
    :return: JSON containing the status of saving the preferences if the request was from AJAX or a rendering of the
    settings page if it as a GET request.
    """
    status = None

    try:
        preferences = UserPreferences.objects.all().first()
    except:
        preferences = UserPreferences.objects.create()
        preferences.save()

    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=preferences)

        if form.is_valid():
            form.save()
            status = "Preferences saved!"
        else:
            status = "Preferences couldn't be saved!"
    else:
        form = UserPreferencesForm(instance=preferences)

    if request.is_ajax():
        return JsonResponse({"status": status})
    else:
        return render(request, 'settings.html', {'form': form, 'colour_scheme': preferences.colour_scheme})


def get_companies(request):
    """
    :param request: A HTTP request.
    :return: JSON containing the user's saved companies, and JSON containing all of the companies in the FTSE100.
    """
    saved_companies = []

    try:
        preferences = UserPreferences.objects.all().first()
        for company in preferences.companies.split(', '):
            if company:
                saved_companies.append({"name": company})
    except:
        preferences = None

    with open(os.path.dirname(__file__) + '/' + '/../../scraper/data/profiles.json') as f:
        companies = json.load(f)
        return JsonResponse({"companies": companies, "saved_companies": saved_companies})


def get_sectors(request):
    """
    :param request: A HTTP request
    :return: JSON containing the user's saved sectors, and JSON containing all of the sectors in the FTSE100.
    """

    saved_sectors = []

    try:
        preferences = UserPreferences.objects.all().first()
        for sector in preferences.sectors.split(', '):
            if sector:
                saved_sectors.append({"name": sector})
    except:
        preferences = None

    with open(os.path.dirname(__file__) + '/' + '/../../scraper/data/sectors.json') as f:
        sectors = json.load(f)
        return JsonResponse({"sectors": sectors, "saved_sectors": saved_sectors})


def get_preferences(request):
    """
    :param request: A HTTP request.
    :return: JSON containing the user's voice preference and colour scheme preference.
    """
    preferences = UserPreferences.objects.all().first()

    return JsonResponse({'voice': preferences.voice, 'colour_scheme': preferences.colour_scheme})
