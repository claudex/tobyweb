# -*- encoding: utf-8 -*-

from django.db import models
import helpers
from polymorphic import PolymorphicModel

import re

class Tribune(models.Model):
    name = models.CharField(max_length=42, unique=True)
    
    def __unicode__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=42,unique=True)
    
    def __unicode__(self):
        return self.name
    
class Mussel(models.Model):
    username = models.CharField(max_length=256)
    tribune = models.ForeignKey(Tribune)
    team = models.ForeignKey(Team)
    
    class Meta:
        unique_together = ("username","tribune")
        
    def __unicode__(self):
        return self.username
        
class Cps(models.Model):
    latitude = models.DecimalField(max_digits=15,decimal_places=12)
    longitude = models.DecimalField(max_digits=15,decimal_places=12)
    mussel = models.ForeignKey(Mussel)
    
    def __unicode__(self):
        return "%s (%d,%d)"%(mussel.username,latitude,longitude)

class Post(models.Model):
    tribune = models.ForeignKey(Tribune)
    post_id = models.IntegerField()
    time = models.DateTimeField()
    ua = models.CharField(max_length=256)
    mussel = models.ForeignKey(Mussel,blank=True,null=True)
    msg = models.TextField()
    
    class Meta:
        unique_together = ("tribune","post_id","time")
        
    #@classmethod
    #def create(cls,tribune,post_id,time,ua,mussel,msg):
        #post = Post()
        #post.tribune=tribune
        #post.post_id=post_id
        #post.ua=ua
        #post.mussel=mussel
        #post.msg=msg
        #return post
    
class Filter(PolymorphicModel):
    tribune = models.ForeignKey(Tribune)
        
class PreumsFilter(Filter):
    name = models.CharField(max_length=42)
    hour = models.TimeField()
    last = models.ForeignKey(Post, blank=True, null=True)
    blacklist = models.ManyToManyField(Mussel)
    
    def process(self,post_list):
        ret = None
        candidate = None
        for post in post_list:
            if post.mussel and not blacklist.contains(post.mussel):
                if self.last == None or (self.last.time.date() < post.time.date() 
                and post.time.time() >= self.hour):
                    if candidate == None or post.time < candidate.time or (post.time == candidate.time and post.post_id < candidate.post_id):
                        candidate = post
        if candidate <> None:
            self.last = candidate
            self.save()
            if candidate.mussel == None:
                ret = {'msg': u"Bonjour %s, dommage que tu ne sois pas identifié [:kiki]"%(candidate.ua)}
            else:
                score, create = PreumsScore.objects.get_or_create(mussel=candidate.mussel, preums=self, defaults={'score':1})
                score.inc_score
                score.save()
                i = 1
                for s in PreumsScore.objects.order_by("-score"):
                    if s == score:
                        ret = {'msg': "Bonjour %s, tu es %de"%(candidate.mussel.username,i)}
                        break
                    else:
                        i+=1
        return ret
            
class PreumsScore(models.Model):
    mussel = models.ForeignKey(Mussel)
    preums = models.ForeignKey(PreumsFilter)
    score = models.IntegerField()
    
    def inc_score(self):
        self.score = self.score + 1
        
class FortuneFilter(Filter):
    cmd = "#fortune "
    
    norloge_regex = r"(\d{2}/\d{2}#)?\d{1,2}:\d{2}(:\d{2})?(¹|²|³|^[1-9]|:[1-9])?"
    
    bloc_regex = norloge_regex + "-" + norloge_regex
    
    fortune_id = models.IntegerField()
    posts = models.ManyToManyField(Post)
    msg = models.TextField()
    
    def process(self, post_list):
        #syntaxe: #fortune norloge1 norloge2 norloge2 // commentaire
        #ou nhorloge1-nhorloge2 pour un bloc
        
        for post in post_list:
            if post.msg.startswith(self.cmd):
                if post.mussel <> None:
                    norloges, sep, comment = post.msg[len(cmd):].split("//")
                    cont = True
                    posts = []
                    while cont:
                        cur_hor, sep, norloges = norloges.split(" ")
                        if sep:
                            cur_hor = cur_hor.strip()
                            if helpers.is_norloge(cur_hor):
                                p_time = helpers.norloge_to_time(cur_hor)
                                posts.append(helpers.norloge_to_post(p_time))
                            elif helpers.is_norloge_block(cur_hor):
                                start_nor,sep,end_nor = cur_hor.split("-")
                                p_from = helpers.norloge_to_time(start_nor)
                                p_to = helpers.norloge_to_time(end_nor)
                                posts.extend(helpers.interval_to_posts(p_from,p_to))
                        else:
                            if helpers.is_norloge(norloges):
                                p_time = helpers.norloge_to_time(norloges)
                                posts.append(helpers.norloge_to_post(p_time))
                            cont=False
                    if posts:
                        fortune = Fortune(tribune=post.tribune, owner=post.mussel)
                        fortune.save()
                        if comment:
                            fortune.comment = comment
                        fortune.posts.extend(posts)
                        fortune.save()
                            

                    
class Fortune(models.Model):
    tribune = models.ForeignKey(Tribune)
    owner = models.ForeignKey(Mussel)
    posts = models.ManyToManyField(Post)
    comment = models.TextField(blank=True)
    
class CpsFilter(Filter):
    regex = r"cps(:\d{1,3}(\.\d+)?){2}"
    
    def process(self, post_list):
        #TODO use only the last post
        pattern = re.compile(self.regex)
        for post in post_list:
            res = pattern.search(post.ua)
            if res:
                del_pos = res.string.find(":",4)
                lat = float(res.string[4:del_pos])
                lon = float(res.string[del_pos+1:])
                try:
                    cps = Cps.objects.get(mussel=post.mussel)
                except Cps.DoesNotExist:
                    cps = Cps(mussel=post.mussel)
                if cps.latitude <> lat or cps.longitude <> lon:
                    cps.latitude = lat
                    cps.longitude = lon
                    cps.save()