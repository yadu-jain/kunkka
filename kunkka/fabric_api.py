import fabric
from fabric.api import *
import os
env.hosts=["216.185.100.203"]
env.user="root"
#env.password="m@l@vtez@l6804"
env.password="5UGjGAU77iaCKGIE"

temp_path="/home/heera/data_platform/env/kunkka/temp/"
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