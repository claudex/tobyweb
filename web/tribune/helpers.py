from datetime import datetime
from models import Post

#norloge format : MM/DD#hh:mm:ss
norloge_regex=r"((0[1-9]|1[0-2])#)?([0-1]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?(¹|²|³|^[1-9]|:[1-9])?"
norloge_patern = re.compile(norloge_regex)
norloge_ex_patern = re.compile(r"^"+norloge_regex+r"$")

bloc_pattern = re.compile(r"^"+norloge_regex + r"-" + norloge_regex+r"$")

class NorlogeFormatError:
    def __init__(self, reason):
        self.reason = reason;
    
    def __str__(self):
        return self.reason;
    
class PostNorloge:
    def __init__(self,hour, minute, idx=0, **kwargs) month=None, day=None, second=None, idx=0):
        self.hour=hour
        self.minute=minute
        if ("month" in kwargs and "day" not in kwargs) or ("day" in kwargs and "month" not in kwargs):
            raise NorlogeFormatError("You cannot specify a day without a month or a month without a day")
        if (month in kwargs and day in kwargs):
            self.month=kwargs["month"]
            self.day=kwargs["day"]
        else:
            self.month=None
            self.day=None
        if (idx > 0 and "second" not in kwargs):
            raise NorlogeFormatError("You cannot specify an index without a second")
        if "second" in kwargs:
            self.second=kwargs["second"]
        self.idx=idx
        
    
def norloge_to_time(norloge):
    """Return a PostNorloge corresponding to the norloge
    
    Parameters
    ----------
    norloge : string
        A norloge matching the following regex : (\d{2}/\d{2}#)?\d{1,2}:\d{2}(:\d{2})?(¹|²|³|^[1-9]|:[1-9])?
        
    Exceptions
    ----------
    NorlogeFormatError
        When the given norloge doesn't match the regex
        
    """

    if is_norloge(norloge):
        date, sep, time = norloge.split("#")
        if sep:
            month, sep, day = date.split("/")
        else:
            time=date
        post_time = _time_from_norloge(time)
        if sep:
            post_time.month=int(month)
            post_time.day=int(day)
        return post_time
    else:
        raise NorlogeFormatError("The norloge is not formated correctly")
            
def _time_from_norloge(time):
    hour,sep,mmss = time.split(":")
    minutes,sep,ssid = time.split(":")
    idx = 0
    if len(ssid) >= 2:
        secondes = ssid[0:2]
        if len(ssid) == 3:
            if ssid[2] == "²":
                idx=1
            elif ssid[2] == "³":
                idx=2
        elif len(ssid) == 4:
            sec, sep, id = ssid.split(":")
            if not sep:
                sec, sep, id = ssid.split("^")
            if sep:
                idx = int(id)-1
        
        complete=True
    else:
        complete=False
    
    if secondes:
        norloge=PostNorloge(int(hour),int(minutes),idx,second=secondes)
    else:
        norloge=PostNorloge(int(hour),int(minutes))
    return norloge
            
            
        
def norloge_to_post(norloge):
    """Return the post corresponding to the norloge
    If there is multiple post at the time and no more precise qualifier, the first of the most recent date is chosen.
    
    Parameters
    ----------
    norloge : PostNorloge
    
    """
    if norloge.month and norloge.second:
        post = Post.objects.filter(time__month = norloge.month, time__day = norloge.day, time__hour = norloge.hour, time__minute = norloge.minute, time__second = norloge.second).order_by("-time")[idx]
    elif norloge.month:
        post = Post.objects.filter(ime__month = norloge.month, time__day = norloge.day, time__hour = norloge.hour, time__minute = norloge.minute).order_by("-time")[idx]
    elif norloge.second:
        post = Post.objects.filter(time__hour = norloge.hour, time__minute = norloge.minute, time__second = norloge.second).order_by("-time")[idx]
    else:
        post = Post.objects.filter(time__hour = norloge.hour, time__minute = norloge.minute).order_by("-time")[idx]
    return post

def interval_to_posts(fromNorloge, toNorloge):
    """Return a QuerySet of the Post between fromNorloge and toNorloge
    If the fromNorloge or toNorloge in ambiguous, the most recent post is chosen
    
    Parameters
    ----------
    fromNorloge : PostNorloge
        The norloge from with the QuerySet starts
    toNorloge : PostNorloge
        The norloge where the QuerySet ends
        
    """
    fromPost = norloge_to_post(fromNorloge)
    toPost = norloge_to_post(toNorloge)
    
    #TODO improve these queries
    nbToPosts = Post.objects.filter(time = toPost.time).count()
    totalPosts = Post.objects.filter(time__range=(fromPost.time, toPost.time)).count()
    postList = Post.objects.filter(time__range=(fromPost.time, toPost.time)).order_by("-time")[fromNorloge.idx:totalPosts-fromNorloge-(nbToPosts-1-toPost.idx)]
    
    return postList;
        
def is_norloge(norloge):
    if re.match(norloge_ex_patern,norloge):
        return True
    else:
        return False
        
def contains_norloge(norloge):
    if re.search(norloge_patern,norloge):
        return True
    else:
        return False
        
def is_norloge_block(block):
    if re.match(bloc_pattern,block):
        return True
    else:
        return False