
import subprocess
import time
import backend.config as cfg

def get_modified_time(path, format = "%Y-%m-%d %H:%M:%S"):
    t = subprocess.run(['git', 'log', '-1', '--pretty="%ci"', '.'], 
    stdout=subprocess.PIPE, encoding="UTF-8",
    cwd=path.as_posix()).stdout
    t = time.strptime(t.strip('"\n'), '%Y-%m-%d %H:%M:%S %z')
    return time.strftime("%Y-%m-%d %H:%M:%S", t)

def last_commit():
    return get_modified_time(cfg.path.git)

def branch():
    return subprocess.run(['git', 'branch','--show-current',], 
    stdout=subprocess.PIPE, encoding="UTF-8",
    cwd=cfg.path.git.as_posix()).stdout
