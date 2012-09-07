from django.http import HttpResponse, Http404
from django.db.models import Sum
from django.shortcuts import render_to_response
from django.template import loader, RequestContext

from models import Blacklist, Preums, PreumsEquipes, PreumsMsg 

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
    table_data = '';
    i = 1
    # TODO  /!\ Warning big XSS fault (verify that there is no <script> or <img>...)
    for preums in preums_list:
        if preums.get_equipe():
            name= "%s (%s)" % (preums.login,preums.get_equipe())
        else:
            name= preums.login
        table_data += "<tr><td>%d</td><td>%s</td><td>%d</td></tr>\n" % (i,name,preums.score)
        i+=1
    
    #Team highscore list
    team_preums = Preums.objects.filter(preums_name=hour).exclude(equipe = 0).values('equipe').annotate(Sum('score')).order_by('score__sum').reverse()
    team_table = ''
    i = 1
    # TODO  /!\ Warning big XSS fault (verify that there is no <script> or <img>...)
    for preums in team_preums:
        team = PreumsEquipes.objects.get(equipe_id=preums['equipe'])
        team_table += "<tr><td>%d</td><td>%s</td><td>%d</td></tr>\n" % (i,team.nom, preums['score__sum'])
        i+=1
    
    #Stats
    nb_moules = len(preums_list)
    nb_team = len(team_preums)
    nb_preums = preums_list.aggregate(Sum('score'))['score__sum']
    
    return render_to_response('tribune/preums.html',
                              {'table_data': table_data,
                              'preums_list': preums_list,
                               'team_table': team_table,
                               'preums_available': preums_available,
                               'last_preums': last_preums,
                               'blacklist': blacklist_login,
                               'nb_moules': nb_moules,
                               'nb_team': nb_team,
                               'nb_preums': nb_preums,
                               'tribune': tribune,
                               'hour': hour}, context_instance=RequestContext(request))