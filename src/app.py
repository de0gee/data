import os
import sys
sys.path.insert(0, os.getcwd())
import logging

# Setup logging
try:
    os.remove('datastore.log')
except:
    pass
logger = logging.getLogger('datastore')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('datastore.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
bigformatter = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(module)s:%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S')
formatter = logging.Formatter('%(asctime)s %(levelname)-7s %(module)-11s %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S')
fh.setFormatter(bigformatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

from jsonencoder import jsonencoder

if __name__ == '__main__':
    logger.info('creating an instance of auxiliary_module.Auxiliary')
    a = {
        "time": 12398123,
        "ab:cd:ef": -12,
        "cd:df": -20,
        "user": "zack"
    }
    c = jsonencoder.JSONEncoder()
    print(c.encode(a))
    logger.info('done with auxiliary_module.some_function()')
