from db import get_perms_links

def getAuthorizedLinks(request):    
    perms=request.user.perms
    if perms and len(perms) >0:        
        try:
            request.allowed_links=get_perms_links(perms)#[obj for obj in get_perms_links(perms)]
        except Exception as e:
            print e
            request.allowed_links=[]
    else:
        print "No perms"
        request.allowed_links=[]
def authorizeResource(request):    
    for link in request.allowed_links:
        if request.path ==link.path:
            request.link=link
            return True
    return False
