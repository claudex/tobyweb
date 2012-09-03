from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from models import Preums,PreumsMsg, Blacklist


def index(request):
    return HttpResponse("Hello world")
    
def preums(request,tribune,*args, **kwargs):
    if 'hour' in kwargs:
        hour = kwargs['hour']
    else:
        hour = 'minuit'
        
    preums_available = [msg.preums_name for msg in PreumsMsg.objects.all().distinct()]
    print preums_available
    if hour not in preums_available:
        raise Http404
        
    #Retrieve the blacklist login
    preums_col_name = "preums_%s" % (hour)
    if preums_col_name not in dir(Blacklist):
        preums_col_name = 'preums'    
    filter_args = { preums_col_name: 1}
    blacklist_login = [bl.login for bl in Blacklist.objects.filter(**filter_args)]
 

    #print blacklist_login
        
    preums_list = Preums.objects.filter(preums_name=hour).order_by('score').reverse()

    #preums_table_data=''.join(['<td>%d</td><td>%s;
    table_data = '';
    i = 1
    #TODO  /!\ Warning big XSS fault (verify that there is no <script> or <img>...)
    for preums in preums_list:
        if preums.get_equipe():
            name= "%s (%s)" % (preums.login,preums.get_equipe())
        else:
            name= preums.login
        table_data += "<tr><td>%d</td><td>%s</td><td>%d</td></tr>\n" % (i,name,preums.score)
        i+=1
    
    return render_to_response('tribune/preums.djhtml',
                              {'table_data': table_data,
                               'preums_available': preums_available,
                               'blacklist': blacklist_login,
                               'tribune': tribune,
                               'hour': hour})