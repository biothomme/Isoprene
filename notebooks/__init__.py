# as paths are stored in yaml file and we also want to access other directories
# two packages are great
import yaml
import sys

# we import the catalog of paths
PCAT = yaml.load(open("../PATHS.yml", "r"), Loader=yaml.FullLoader)

# then we add scripts directory to path variable
sys.path.insert(0, "../src")

