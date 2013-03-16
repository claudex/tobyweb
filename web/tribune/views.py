from decimal import Decimal
import json

from django.core import serializers
from django.http import HttpResponse, Http404
from django.db.models import Count, F, Sum
from django.shortcuts import render_to_response
from django.template import loader, RequestContext

from models import Blacklist, ChasseLog, Chasseurs, Cps, Preums, PreumsEquipes, PreumsMsg 

def preums(request, tribune_name, *args, **kwargs):
    """
    Preum's list (??)
    """
    try:
        tribune = Tribune.objects.get(name=tribune_name)
        if 'hour' in kwargs:
            hour = kwargs['hour']
        else:
            hour = 'minuit'
        preums_available = [preums.name for preums in PreumsFilter.objects.filter(tribune=tribune]
        
        cur_preums = Preums.objects.get(name=hour)
    
        #Individual highscore list
        preums_list = Preums.objects.filter(preums=cur_preums).order_by('-score')
        
        #Team highscore list
        team_preums = Preums.objects.filter(preums_name=hour).annotate(team="mussel.team").aggregate(Sum("score")).order_by("-score__sum")
        
        for team in team_preums:
            team['name'] = PreumsEquipes.objects.get(equipe_id = team['equipe']).nom
        
        #Stats
        nb_moules = len(preums_list)
        nb_team = len(team_preums)
        nb_preums = preums_list.aggregate(Sum('score'))['score__sum']
        
        return render_to_response('tribune/preums.html',
                                {'cur_preums': cur_preums,
                                'preums_list': preums_list,
                                'team_preums': team_preums,
                                'preums_available': preums_available,
                              #  'last_preums': last_preums,
                              #  'blacklist': blacklist_login,
                                'nb_moules': nb_moules,
                                'nb_team': nb_team,
                                'nb_preums': nb_preums,
                                'tribune': tribune},
                                #'hour': hour},
                                context_instance=RequestContext(request))
    except ObjectDoesNotExist:
        return HttpResponse("<h1>Tribune not found</h1>") #TODO change not found handler.
    
    
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

def post(request):
    if request.method == 'POST':
        json_dump = json.load(request)
        tribune_name = json_dump['tribune']
        try:
            tribune = Tribune.objects.get(name=tribune_name)
            post_list = []
            for post in json_dump['posts']:
                post_id=int(post['post_id'])
                ua = post['ua']
                login = post['user']
                time_text = post['time']
                msg = post['msg']
                time = timezone.make_aware(datetime.strptime(time_text,"%Y-%m-%dT%H:%M:%S"),
                    timezone.utc)
                if login:
                    mussel,m_c = Mussel.objects.get_or_create(username=login, tribune=tribune)
                else:
                    mussel = None
                p, created = Post.objects.get_or_create(tribune=tribune,post_id=post_id,
                    time=time, ua=ua, mussel=mussel, msg=msg)
                if created:
                    post_list.append(p)
            resp = []            
            #for fil in Filter.objects.filter(tribune = tribune):
                #resp.append(fil.process(post_list))
            [resp.append(fil.process(post_list)) for fil in Filter.objects.filter(tribune = tribune)]
            return HttpResponse(json.dumps(resp,cls=PostEncoder))
        except Tribune.DoesNotExist:
            resp = HttpResponse("The tribune does not exist")
            resp.status_code = 400
            return resp
    else:
        resp = HttpResponse("The method is not allowed. Method allowed: POST")
        resp.status_code = 400
        return resp
