from pathlib import Path
import backend.config as cfg

import markdown

def parse_md(fname):
    f = open(fname)
    text = f.read()
    html = markdown.markdown(text, extensions = ['fenced_code', 'codehilite'])
    return html

class FileLink:
    def __init__(self, path):
        if isinstance(path, Path):
            path = path.as_posix()
        path = path.replace(cfg.path.git.as_posix(), '/gitrepo')
        self.path = Path(path)

    def __repr__(self):
        return self.path.as_posix()

    def __str__(self):
        return self.path.as_posix()

    @property
    def name(self):
        return self.path.name

def is_path(var):
    return isinstance(var, Path)

def is_file_link(var):
    return isinstance(var, FileLink)

def is_list(var):
    return isinstance(var, list)

