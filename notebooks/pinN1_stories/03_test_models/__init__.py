# as paths are stored in yaml file and we also want to access other directories
# two packages are great
from functools import reduce
import json
import os
import sys
import yaml

# we import the catalog of paths
PATHS_FILE = os.path.abspath("../../../PATHS.yml")
PCAT = yaml.load(open(PATHS_FILE, "r"), Loader=yaml.FullLoader)

# to transform the path
def get_path(*key_args):
    path = reduce(lambda x, y: x.get(y), key_args, PCAT)
    return os.path.abspath(os.path.join(os.path.dirname(PATHS_FILE), path))
    

# we load the scripts from the corresponding src directory
src_dir = get_path("CODE", "MODELS", "ROOT")
sys.path.insert(1, src_dir)