import os
import json
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from research import models
from research.models import Event, Group, Region, Relationship, Theme, Meta
from timeline import settings


def index(request):
    return render(request, "index.html")


def events(request, slug):
    try:
        metadata = Meta.objects.get(slug=slug)
    except models.Meta.DoesNotExist:
        raise Http404('Timeline not found')

    with open(os.path.join(settings.DB_DIR, 'json/events-%s.json' % metadata.slug), 'r') as f:
        all_events = f.read()
    return HttpResponse(all_events, content_type='application/json')


def event(request, event_id, slug):
    try:
        metadata = Meta.objects.get(slug=slug)
    except models.Meta.DoesNotExist:
        raise Http404('Timeline not found')

    event_obj = Event.objects.get(id=event_id)
    relationships = {
        "preceding": [],
        "succeeding": []
    }
    for relationship in Relationship.objects.filter(event_one__id=event_obj.id):
        rel = relationship.event_two
        if rel.start_date > event_obj.start_date:
            relationships['succeeding'].append(rel.as_json())
        else:
            relationships['preceding'].append(rel.as_json())
    for relationship in Relationship.objects.filter(event_two__id=event_obj.id):
        rel = relationship.event_one
        if rel.start_date > event_obj.start_date:
            relationships['succeeding'].append(rel.as_json())
        else:
            relationships['preceding'].append(rel.as_json())

    def sort_by_date(e):
        return e['start_date']

    relationships['preceding'].sort(key=sort_by_date)
    relationships['succeeding'].sort(key=sort_by_date)
    context = {
        'event': event_obj.as_json(),
        'related_events': relationships
    }
    return HttpResponse(json.dumps(context), content_type='application/json')


def years(request, slug):
    try:
        metadata = Meta.objects.get(slug=slug)
    except models.Meta.DoesNotExist:
        raise Http404('Timeline not found')
    # get all active years
    all_events = Event.objects.filter(hide=False, timeline=slug).order_by('start_date')
    all_years = set()
    # if an event takes several years, add all years between start year and end year
    for event_instance in all_events:
        if event_instance.end_date:
            try:
                years = range(event_instance.start_date.year, event_instance.end_date.year + 1)
                all_years = all_years.union(set(years))
            except Exception as err:
                print(err, event_instance)
        else:
            try:
                all_years.add(event_instance.start_date.year)
            except Exception as err:
                print(err, event_instance)

    return HttpResponse(json.dumps(sorted(all_years)), content_type='application/json')


def groups(request, slug):
    try:
        metadata = Meta.objects.get(slug=slug)
    except models.Meta.DoesNotExist:
        raise Http404('Timeline not found')

    all_groups = Group.objects.values_list('slug', 'name').order_by('region__slug')
    return HttpResponse(json.dumps(list(all_groups)), content_type='application/json')


def groups_by_region(request, slug):
    try:
        metadata = Meta.objects.get(slug=slug)
    except models.Meta.DoesNotExist:
        raise Http404('Timeline not found')

    rgns = Region.objects.all().order_by('name')
    rg_list = []
    for rgn in rgns:
        grps = list(Group.objects.filter(region=rgn.id).order_by('region__slug').values('slug', 'name', 'region__name',
                                                                                        'region__slug'))
        rgn_obj = {
            'slug': rgn.slug,
            'name': rgn.name,
            'groups': grps
        }
        rg_list.append(rgn_obj)
    return HttpResponse(json.dumps(rg_list), content_type='application/json')


def year_settings(request, slug):
    try:
        metadata = Meta.objects.get(slug=slug)
    except models.Meta.DoesNotExist:
        raise Http404('Timeline not found')

    return HttpResponse(json.dumps(settings.TOGGLES['years']), content_type='application/json')


def themes(request, slug):
    try:
        metadata = Meta.objects.get(slug=slug)
    except models.Meta.DoesNotExist:
        raise Http404('Timeline not found')

    all_themes = {}
    for t in Theme.objects.all():
        all_themes[t.slug] = t.name
    return HttpResponse(json.dumps(all_themes), content_type='application/json')


def meta(request, slug):
    try:
        metadata = Meta.objects.get(slug=slug)
    except models.Meta.DoesNotExist:
        raise Http404('Timeline not found')

    return HttpResponse(json.dumps(metadata.as_json()), content_type='application/json')
