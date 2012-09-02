from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from models import Preums,PreumsMsg


def index(request):
    return HttpResponse("Hello world")
    
def preums(request,tribune,*args, **kwargs):
#    print dir()
#    print hour
#    if not 'hour' in dir():
#        hour='minuit'
    if 'hour' in kwargs:
        hour = kwargs['hour']
        print "plop"
    else:
        hour = 'minuit'
    preums_available = PreumsMsg.objects.all().distinct()
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
    
    return render_to_response('tribune/preums.html',
                              {'table_data': table_data,
                               'preums_available': preums_available,
                               'tribune': tribune,
                               'hour': hour})