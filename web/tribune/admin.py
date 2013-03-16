# -*- coding: utf-8 -*-
"""
Model admin
"""
from django.contrib import admin
from models import *

# Simple automatic registering
admin.site.register(AutomailConf)
admin.site.register(Blacklist)
admin.site.register(Bookmark)
admin.site.register(ChasseLog)
admin.site.register(Chasseurs)
admin.site.register(Coincoins)
admin.site.register(Cps)
admin.site.register(Fortunes)
admin.site.register(FortunesComments)
admin.site.register(LastCoin)
admin.site.register(Modo)
admin.site.register(ModoVotes)
admin.site.register(Mpc)
admin.site.register(Posts)
admin.site.register(Preums)
admin.site.register(PreumsEquipes)
admin.site.register(PreumsMsg)
admin.site.register(Repondeur)
admin.site.register(RepondeurConf)
