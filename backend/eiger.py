
import os
import time
import backend.config as cfg
from backend import git
from backend.utils import FileLink
import subprocess
from pathlib import Path
import json




class EigerModule:
    def __init__(self):
        self.data = {}
        self['id'] = None
        self['beb_top'] = None
        self['beb_bot'] = None
        self['feb_top'] = None
        self['feb_bot'] = None
        self['extra'] = {}

    def __str__(self):
        return f'EigerModule({self["id"]})'

    def __repr__(self):
        return self.__str__()

    def items(self):
        return self.data.items()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def load(self, full_id):
        if full_id is None:
            return self
        p = cfg.path.module/full_id
        if not p.is_dir():
            return

        self['id'] = full_id
        for name in ['feb_top', 'feb_bot']:
            self[name] = get_feb_info(resolve_name(p/name))
        for name in ['beb_top', 'beb_bot']:
            self[name] = get_beb_info(resolve_name(p/name))

        self['extra']['time'] = git.get_modified_time(p)
        files = [f for f in p.iterdir() if not f.is_symlink()]
        for f in files:
            if f.suffix == '':
                with open(f, 'r') as infile:
                    self['extra'][f.name] = infile.readlines()
            else:
                self['extra'][f.stem] = FileLink(f)

        return self

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
    res['url'] = f'/eiger/feb/{full_id}'
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
    res['url'] = f'/eiger/beb/{full_id}'
    return res

def get_mounted_modules():
    modules = {}
    path = cfg.path.systems
    
    for fname in path.iterdir():
        if fname.is_dir():
            for mod in fname.iterdir():
                if mod.is_symlink():
                    modules[resolve_name(mod)] = fname.name
    return modules
    

def get_modules():
    modules = [f for f in os.listdir(cfg.path.module) if not f.endswith('cgi')]
    failed_parse = []
    moddict = {}
    failed_index = 900
    for m in modules:
        try: 
            index = int(m.strip('T'))
            # moddict[index] = {'id':m}
            moddict[index] = EigerModule().load(m)
            # bebdict[index] = get_beb_info(b)
        except:
            moddict[failed_index] = {'id':m}
            failed_index += 1
    return moddict

def resolve_name(p):
    try:
        name = Path(p).resolve().name
        print(f'{name=}, {p=}, p.name: {p.name}')
        if name == p.name:
            name = None
    except:
        name = None
    return name


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



def list_modules_in_system(full_id, orientation = 'horizontal'):
    """
    Return a nested list of modules in a system, adding id: to hostname to 
    indicate how you can access the bebs from command line
    """
    if full_id is None:
        return None
    p = cfg.path.systems/full_id
    files = [f for f in p.iterdir() if 'module_' in f.name]
    files.sort(key = lambda x : tuple(int(i) for i in x.name.split('_')[1].split('.')))
    cols = max(int(f.name.split('.')[-1]) for f in files)+1
    modules = [EigerModule().load(resolve_name(f)) for f in files]
    for f,m in zip(files, modules):
        m['pos'] = f.name.split('_')[-1]
    

    if orientation == 'horizontal':
        modules = modules[::-1]
    i=0
    for mod in modules:
        if mod['beb_top'] is not None:
            mod['beb_top']['hostname'] = f'{i*2}:{mod["beb_top"]["hostname"]}'
            mod['beb_bot']['hostname'] = f'{i*2+1}:{mod["beb_bot"]["hostname"]}'
            i+=1
    if orientation == 'horizontal':
        modules = modules[::-1]
    modules = [modules[i:i+cols] for i in range(0, len(modules), cols)]
    modules = modules[::-1]
    return modules

def get_system_info(full_id):
    if full_id is None:
        return None
    p = cfg.path.systems/full_id
    res = {}
    res['id'] = full_id
    res['type'] = full_id.split('_')[1]
    res['time'] = git.get_modified_time(p)
    excluded = ['module', '.cgi']
    files = [f for f in p.iterdir() if not any(n in f.name for n in excluded)]
    for fname in files:
        if fname.is_dir():
            fpaths = [FileLink(f) for f in fname.iterdir()]
            res[fname.stem] = fpaths

        elif fname.suffix == '':
            with open(fname, 'r') as f:
                res[fname.name] = f.read().strip('\n ')
        else:
            res[fname.name] = fname.name
    
    res['modules'] = list_modules_in_system(full_id, res['orientation'])

    #pass column width to display
    res['column-width'] = 4
    if len(res['modules'][0]) == 6:
        res['column-width'] = 2
     
    


    return res