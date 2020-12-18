
import os
import time
import backend.config as cfg
from backend import git
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

def get_bebs():
    bebs = [f for f in os.listdir(cfg.path.beb) if not f.endswith('cgi')]
    failed_parse = []
    bebdict = {}
    failed_index = 900
    for b in bebs:
        try: 
            index = int(b.split('_')[-1])
            # bebdict[index] = {'id':b}
            bebdict[index] = get_beb_info(b)
        except:
            bebdict[failed_index] = {'id':b}
            failed_index += 1
    return bebdict



def get_feb_info(full_id):
    if full_id is None:
        return None
    #do some checks maybe
    p = cfg.path.feb/full_id
    fields = ['fpgatype', 'rev', 'errorcode', 'comments']
    additional_fields = [f for f in os.listdir(p) if f not in fields and '.' not in f]
    fields += additional_fields

    res = {}
    res['id'] = full_id
    for field in fields:
        with open(p/field, 'r') as f:
            res[field] = f.read()

    res['time'] = git.get_modified_time(p)
    return res

def get_beb_info(full_id):
    if full_id is None:
        return None
    #do some checks maybe
    p = cfg.path.beb/full_id

    fields = ['hostname', 'inuse', 'rev', 'errorcode', 'comments']
    additional_fields = [f for f in os.listdir(p) if f not in fields and '.' not in f]
    fields += additional_fields

    res = {}
    res['id'] = full_id
    for field in fields:
        with open(p/field, 'r') as f:
            res[field] = f.read()

    res['time'] = git.get_modified_time(p)
    return res

def get_modules():
    modules = [f for f in os.listdir(cfg.path.module) if not f.endswith('cgi')]
    failed_parse = []
    moddict = {}
    failed_index = 900
    for m in modules:
        try: 
            index = int(m.strip('T'))
            moddict[index] = {'id':m}
            # bebdict[index] = get_beb_info(b)
        except:
            moddict[failed_index] = {'id':m}
            failed_index += 1
    return moddict

def resolve_name(p):
    try:
        rpath = Path(p).resolve().name
        if rpath.name == p.name:
            rpath = None
    except:
        rpath = None
    return rpath

def get_module_info(full_id):
    p = cfg.path.module/full_id

    res = {}
    res['id'] = full_id

    for name in ['feb_top', 'feb_bot']:
        res[name] = get_feb_info(resolve_name(p/name))
    for name in ['beb_top', 'beb_bot']:
        res[name] = get_beb_info(resolve_name(p/name))

    res['extra'] = {}
    res['extra']['time'] = git.get_modified_time(p)
    files = [f for f in p.iterdir() if not f.is_symlink()]
    for f in files:
        if f.suffix == '':
            with open(f, 'r') as infile:
                res['extra'][f.name] = infile.read()
        else:
            res['extra'][f.stem] = Path(f'/gitrepo/Eiger/modules/{res["id"]}/{f.name}')
        
    return res

def get_systems():
    systems = [f for f in os.listdir(cfg.path.systems) if not f.endswith('cgi')]
    failed_parse = []
    systemdict = {}
    failed_index = 900
    for s in systems:
        try: 
            systemdict[s] = get_system_info(s)
            # bebdict[index] = get_beb_info(b)
        except:
            systemdict[s] = {'id':s}
    return systemdict

def get_system_info(full_id):
    if full_id is None:
        return None
    p = cfg.path.systems/full_id
    res = {}
    res['id'] = full_id
    res['type'] = full_id.split('_')[1]
    res['time'] = git.get_modified_time(p)
    return res