from decimal import Decimal
import json

from django.core import serializers
from django.http import HttpResponse, Http404
from django.db.models import Count, F, Sum
from django.shortcuts import render_to_response
from django.template import loader, RequestContext

from models import Blacklist, ChasseLog, Chasseurs, Cps, Preums, PreumsEquipes, PreumsMsg 

def preums(request, tribune, *args, **kwargs):
    """
    Preum's list (??)
    """
    if 'hour' in kwargs:
        hour = kwargs['hour']
    else:
        hour = 'minuit'
    preums_available = [msg.preums_name for msg in PreumsMsg.objects.all().distinct()]
    
    if hour not in preums_available:
        raise Http404
        
    #Retrieve the blacklist login
    preums_col_name = "preums_%s" % (hour)
    if preums_col_name not in dir(Blacklist):
        preums_col_name = 'preums'    
    filter_args = { preums_col_name: 1}
    blacklist_login = [bl.login for bl in Blacklist.objects.filter(**filter_args)]
    
    #Last preums
    last_preums = PreumsMsg.objects.get(preums_name=hour)
   
    #Individual highscore list
    preums_list = Preums.objects.filter(preums_name=hour).exclude(score = 0).exclude(login__in = blacklist_login).order_by('score').reverse()
    
    #Team highscore list
    team_preums = Preums.objects.filter(preums_name=hour).exclude(equipe = 0).values('equipe').annotate(Sum('score')).order_by('score__sum').reverse()
    
    for team in team_preums:
        team['name'] = PreumsEquipes.objects.get(equipe_id = team['equipe']).nom
    
    #Stats
    nb_moules = len(preums_list)
    nb_team = len(team_preums)
    nb_preums = preums_list.aggregate(Sum('score'))['score__sum']
    
    return render_to_response('tribune/preums.html',
                              {'preums_list': preums_list,
                               'team_preums': team_preums,
                               'preums_available': preums_available,
                               'last_preums': last_preums,
                               'blacklist': blacklist_login,
                               'nb_moules': nb_moules,
                               'nb_team': nb_team,
                               'nb_preums': nb_preums,
                               'tribune': tribune,
                               'hour': hour},
                              context_instance=RequestContext(request))
    
    
def chasse(request, tribune):
    #Blacklist
    blacklist = [bl.login for bl in Blacklist.objects.filter(chasse = 1)]
    
    #Score
    score_list = Chasseurs.objects.exclude(login = blacklist).order_by('-points')
    all_toupils = ChasseLog.objects.filter(patience = 300).filter(quoi = 'tue') #TODO: maybe too much data in memory
    
#    i = 1
    for score in score_list:
#        score.rank = i
#        score.mean_patience =  (score.patience / score.score) if score.score != 0 else 0 
        score.toupil = all_toupils.filter(login = score.login).count()
#        i += 1
    
    #TODO: One Query to rule them all, One Query to find them, One Query to bring them all and in the darkness bind them
    intelligent = score_list.order_by('-points')[0]
    efficace = Chasseurs.objects.extra(select = { 'efficace': 'CAST((points - 10*CAST(survie AS SIGNED))/score AS SIGNED)'}).order_by('-efficace')[0]
    zen = Chasseurs.objects.extra(select = {'pmoyenne': 'CAST(patience/score AS UNSIGNED)'}).order_by('-pmoyenne')[0]
    canardeur = score_list.order_by('-score')[0]
    gentil = score_list.order_by('-survie')[0]
    genereux = score_list.order_by('-lance')[0]
    toupileur = all_toupils.values('login').annotate(Count('id')).order_by('-id__count')[0]
    con = score_list.order_by('points')[0]
    lourd = Chasseurs.objects.exclude(score = 0).extra(select = { 'efficace': 'CAST((points - 10*CAST(survie AS SIGNED))/score AS SIGNED)'}).order_by('efficace')[0]
    precoce = Chasseurs.objects.exclude(score = 0).extra(select = {'pmoyenne': 'CAST(patience/score AS UNSIGNED)'}).order_by('pmoyenne')[0]
    maladroit = Chasseurs.objects.exclude(login = blacklist).order_by('-ratai')[0]
    chauvounet = {'login': 'domi', 'score': 0}
    radin = score_list.order_by('lance','-score')[0]
    
    #stats
    nb_chasseurs = Chasseurs.objects.exclude(login = blacklist).count()
    
    #TODO add the team highscore
    
    return render_to_response('tribune/chasse.html',
                              {'scorelist': score_list,
                               'blacklist': blacklist,
                               'intelligent': intelligent,
                               'efficace': efficace,
                               'zen': zen,
                               'canardeur': canardeur,
                               'gentil': gentil,
                               'genereux': genereux,
                               'toupileur': toupileur,
                               'con': con,
                               'lourd': lourd,
                               'precoce': precoce,
                               'maladroit': maladroit,
                               'chauvounet': chauvounet,
                               'radin': radin},
                              context_instance=RequestContext(request))
    
def cps(request, tribune):
    moules = Cps.objects.all()
    return render_to_response('tribune/cps.html',
                              {'tribune': tribune,
                               'moules': moules},
                              context_instance=RequestContext(request))
    
def cps_json(request, tribune):
    #TODO: remove this view, the result could be directly written in the template
    data = []
    for moule in Cps.objects.all():
        data.append({'login': moule.login,
                     'latitude': float(moule.latitude), #JSON serializer doesn't accept Decimal objects
                     'longitude': float(moule.longitude)})
    return HttpResponse(json.dumps(data), mimetype="application/json")
