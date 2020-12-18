
import os
import time
import backend.config as cfg
import subprocess
from pathlib import Path
def get_febs():
    febs = [f for f in os.listdir(cfg.path.feb) if not f.endswith('cgi')]
    failed_parse = []
    febdict = {}
    failed_index = 900
    for f in febs:
        try: 
            index = int(f.split('_')[-1])
            # febdict[index] = {'id':f}
            febdict[index] = get_feb_info(f)
        except:
            febdict[failed_index] = {'id':f}
            failed_index += 1
    return febdict

def get_feb_info(full_id):
    #do some checks maybe
    p = cfg.path.feb/full_id

    fields = ['fpgatype', 'rev', 'errorcode', 'comments']
    res = {}
    res['id'] = full_id
    for field in fields:
        with open(p/field, 'r') as f:
            res[field] = f.read()

    #Get the updated time from git
    t = subprocess.run(['git', 'log', '-1', '--pretty="%ci"', '.'], 
    stdout=subprocess.PIPE, encoding="UTF-8",
    cwd=p.as_posix()).stdout

    t = time.strptime(t.strip('"\n'), '%Y-%m-%d %H:%M:%S %z')
    res['time'] = time.strftime("%Y-%m-%d %H:%M:%S", t)

    return res

    