# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class AutomailConf(models.Model):
    login = models.CharField(max_length=192, primary_key=True)
    etat = models.IntegerField(null=True, blank=True)
    prive = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=384, blank=True)
    class Meta:
        db_table = u'euroxers_automail_conf'

class Blacklist(models.Model):
    login = models.CharField(max_length=192, primary_key=True)
    chasse = models.IntegerField(null=True, blank=True)
    preums = models.IntegerField(null=True, blank=True)
    fortunes = models.IntegerField(null=True, blank=True)
    repondeur = models.IntegerField(null=True, blank=True)
    uptime = models.IntegerField(null=True, blank=True)
    cps = models.IntegerField(null=True, blank=True)
    blacklist = models.IntegerField(null=True, blank=True)
    preums_equipe = models.IntegerField(null=True, blank=True)
    historique = models.IntegerField(null=True, blank=True)
    passwd = models.IntegerField(null=True, blank=True)
    mpc = models.IntegerField(null=True, blank=True)
    convert2 = models.IntegerField(null=True, blank=True)
    repondeur_conf = models.IntegerField(null=True, blank=True)
    bookmark = models.IntegerField(null=True, blank=True)
    preums_minuit = models.IntegerField(null=True, blank=True, db_column="preums$minuit")
    preums_midi = models.IntegerField(null=True, blank=True, db_column="preums$midi")
    preums_18h = models.IntegerField(null=True, blank=True, db_column="preums$18h")
    preums_test = models.IntegerField(null=True, blank=True, db_column="preums$test")
    coin = models.IntegerField(null=True, blank=True)
    preums_geo = models.IntegerField(null=True, blank=True, db_column="preums$geo")
    chasse_all = models.IntegerField(null=True, blank=True)
    ntp = models.IntegerField(null=True, blank=True)
    preums_taiste = models.IntegerField(null=True, blank=True, db_column="preums$taiste")
    automail = models.IntegerField(null=True, blank=True)
    automail_conf = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'euroxers_blacklist'

class Bookmark(models.Model):
    id = models.BigIntegerField(unique=True,primary_key=True)
    book_time = models.DateTimeField()
    book_login = models.CharField(max_length=192, blank=True)
    post_time = models.DateTimeField()
    login = models.CharField(max_length=192, blank=True)
    info = models.CharField(max_length=192, blank=True)
    message = models.TextField(blank=True)
    class Meta:
        db_table = u'euroxers_bookmark'

class ChasseLog(models.Model):
    id = models.BigIntegerField(unique=True,primary_key=True)
    post_time = models.DateTimeField()
    quoi = models.CharField(max_length=21)
    login = models.CharField(max_length=192, blank=True)
    cible = models.DateTimeField()
    message = models.TextField(blank=True)
    patience = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'euroxers_chasse_log'

class Chasseurs(models.Model):
    login = models.CharField(max_length=192, primary_key=True)
    score = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    patience = models.IntegerField(null=True, blank=True)
    ratai = models.IntegerField(null=True, blank=True)
    survie = models.IntegerField(null=True, blank=True)
    lance = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'euroxers_chasseurs'
        
    def __unicode__(self):
        return "%s: %s" % (self.login, self.score)
    
    def mean_patience(self):
        if self.score != 0:
            mpat = self.patience / self.score
        else:
            mpat = 0
        return mpat 

class Coincoins(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    post_id = models.IntegerField(null=True, blank=True)
    login = models.CharField(max_length=192, blank=True)
    post_time = models.CharField(max_length=42, blank=True)
    doublon = models.IntegerField(null=True, blank=True)
    seul = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'euroxers_coincoins'

class Cps(models.Model):
    login = models.CharField(max_length=192, primary_key=True)
    latitude = models.CharField(max_length=72, blank=True)
    longitude = models.CharField(max_length=72, blank=True)
    class Meta:
        db_table = u'euroxers_cps'

class Fortunes(models.Model):
    fortune_id = models.BigIntegerField(unique=True, primary_key=True)
    fortune_no = models.IntegerField()
    note_modo = models.IntegerField(null=True, blank=True)
    votes_modo = models.IntegerField(null=True, blank=True)
    fortune_login = models.CharField(max_length=192, blank=True)
    fortune_time = models.DateTimeField()
    id = models.BigIntegerField()
    post_id = models.IntegerField(null=True, blank=True)
    post_time = models.DateTimeField()
    doublon = models.IntegerField(null=True, blank=True)
    seul = models.IntegerField(null=True, blank=True)
    login = models.CharField(max_length=192, blank=True)
    info = models.CharField(max_length=192, blank=True)
    message = models.TextField(blank=True)
    class Meta:
        db_table = u'euroxers_fortunes'

class FortunesComments(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    login = models.CharField(max_length=192, blank=True)
    fortune_no = models.IntegerField()
    date = models.DateTimeField()
    message = models.TextField(blank=True)
    is_titre = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'euroxers_fortunes_comments'

class LastCoin(models.Model):
    post_time = models.DateTimeField()
    coin_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'euroxers_last_coin'

class Modo(models.Model):
    login = models.CharField(max_length=192, primary_key=True)
    fortunes = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'euroxers_modo'

class ModoVotes(models.Model):
    id = models.BigIntegerField(unique=True,primary_key=True)
    login = models.CharField(max_length=192, blank=True)
    fortune_no = models.IntegerField()
    note = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'euroxers_modo_votes'

class Mpc(models.Model):
    login = models.CharField(max_length=192, primary_key=True)
    economic = models.FloatField(null=True, blank=True)
    social = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'euroxers_mpc'

class Posts(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    post_id = models.IntegerField(null=True, blank=True)
    post_time = models.DateTimeField()
    doublon = models.IntegerField(null=True, blank=True)
    seul = models.IntegerField(null=True, blank=True)
    login = models.CharField(max_length=192, blank=True)
    info = models.CharField(max_length=192, blank=True)
    message = models.TextField(blank=True)
    class Meta:
        db_table = u'euroxers_posts'

class Preums(models.Model):
    login = models.CharField(max_length=192, db_index=True)
    score = models.IntegerField(null=True, blank=True)
    equipe = models.BigIntegerField(null=True, blank=True) #models.ForeignKey('PreumsEquipes',db_column="equipe", null=False, blank=True)
    preums_name = models.CharField(max_length=192, primary_key=True)
    class Meta:
        db_table = u'euroxers_preums'
        
    def get_equipe(self):
        """This method only existe because the current data in the db don't
           work with the Django configuration for null values.
           It returns the team for the preums' moule or None if the moule
           doesn't belong to a team"""
        if self.equipe == 0:
            return
        cachekey = "_get_equipe_cache"
        if not hasattr(self, cachekey):
            setattr(self, cachekey, PreumsEquipes.objects.get(equipe_id=self.equipe))
        return getattr(self, cachekey)
        
    def __unicode__(self):
        return "%s (%s): %d" % (self.login, self.get_equipe(), self.score)
        #return "%s: %d" % (self.login, self.score)
        
    

class PreumsEquipes(models.Model):
    equipe_id = models.BigIntegerField(unique=True, primary_key=True, db_column="id")
    nom = models.CharField(unique=True, max_length=255, blank=True)
    class Meta:
        db_table = u'euroxers_preums_equipes'
        
    def __unicode__(self):
        return "%s" % (self.nom)

class PreumsMsg(models.Model):
    post_id = models.IntegerField(null=True, blank=True)
    post_time = models.DateTimeField()
    login = models.CharField(max_length=192, blank=True)
    info = models.CharField(max_length=192, blank=True)
    message = models.TextField(blank=True)
    preums_name = models.CharField(max_length=192, primary_key=True)
    is_strict = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'euroxers_preums_msg'

class Repondeur(models.Model):
    id = models.BigIntegerField(unique=True, primary_key=True)
    dest = models.CharField(max_length=192, blank=True)
    post_time = models.DateTimeField()
    login = models.CharField(max_length=192, blank=True)
    info = models.CharField(max_length=192, blank=True)
    message = models.TextField(blank=True)
    class Meta:
        db_table = u'euroxers_repondeur'

class RepondeurConf(models.Model):
    login = models.CharField(max_length=192, primary_key=True)
    etat = models.IntegerField(null=True, blank=True)
    prive = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'euroxers_repondeur_conf'

