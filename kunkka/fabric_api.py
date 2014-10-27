import fabric
from fabric.api import *
import os
env.hosts=["216.185.100.203"]
env.user="root"
#env.password="m@l@vtez@l6804"
env.password="5UGjGAU77iaCKGIE"

# temp_path="/home/heera/data_platform/env/kunkka/temp/"
temp_path="/home/swarthi/projects/env/kunkka/temp/"
##################### Fab function ##########################
def __delete_from_cache__():
    global temp_path
    temp_file=os.path.join(temp_path,"keys.txt")
    with hide('output','running','warnings'):
        put(temp_file,"/root/scripts/")    
        run("python /root/scripts/delete_keys_in_file.py "+"/root/scripts/keys.txt >> /root/scripts/log.txt",pty=False,combine_stderr=False)

def delete_allowed_compaies(userids):
    global temp_path
    temp_file=os.path.join(temp_path,"keys.txt")
    str_userids="\n".join(["user_cmp_"+ userid for userid in userids])
    with open(temp_file,"wb") as f:
        f.write(str_userids)
        f.flush()
        f.close()
    execute(__delete_from_cache__)
    return True


def delete_search_routes(table):
    global temp_path
    temp_file=os.path.join(temp_path,"keys.txt")
    key_list="\n".join([ "_".join(["sr_new",str(row["FROM_CITY_ID"]),str(row["TO_CITY_ID"]),row["JOURNEY_DATE"].replace("-","_") ]) for row in table])
    print key_list
    with open(temp_file,"wb") as f:
        f.write(key_list)
        f.flush()
        f.close()
    execute(__delete_from_cache__)
    return True

def delete_route_pickups(table):
    global temp_path
    temp_file=os.path.join(temp_path,"keys.txt")
    key_list="\n".join(["pkps_new_"+str(row["ROUTE_SCHEDULE_ID"]) for row in table])
    key_list+="\n".join(["delete pkpdtl_"+str()])
    print "clear pickups caching..."
    with open(temp_file,"wb") as f:
        f.write(key_list)
        f.flush()
        f.close()
    execute(__delete_from_cache__)
    return True    

def delete_route_pickup_details(table):
    global temp_path
    temp_file=os.path.join(temp_path,"keys.txt")
    key_list="\n".join(["pkpdtl_"+str(row["PICKUP_ID"]) for row in table])
    print "clear pickups details caching..."
    with open(temp_file,"wb") as f:
        f.write(key_list)
        f.flush()
        f.close()
    execute(__delete_from_cache__)
    return True

def delete_origin_cities():
    global temp_path
    temp_file=os.path.join(temp_path,"keys.txt")
    key_list="\n".join(["origin_cities"])
    print key_list
    with open(temp_file,"wb") as f:
        f.write(key_list)
        f.flush()
        f.close()
    execute(__delete_from_cache__)
    return True    
