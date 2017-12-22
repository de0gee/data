# directory management
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import math
import logging

try:
    import ujson as json
except: 
    import json 
    
# create logger
logger = logging.getLogger('datastore.'+__name__)

class JSONEncoder:
    """A class that can make JSON a little smaller"""
    base_chars = 'abcdefghjijklmnopqrstuvwxyzABCDEFGHJIJKLMNOPQRSTUVWXYZ'
    base = len(base_chars)


    def __init__(self, compressor={}):   
        if compressor == {}:
            compressor = {
                'num': 0,
                'fromKey':{},
                'key': {},
            }
        self.compressor = compressor
        logger.info("HI")

    def num2string(self, number):
        if number < 1:
            return 'a'
        nums = []
        while True:
            power = math.floor(math.log(number)/math.log(self.base))
            if self.base**(power+1) == number:
                power = power+1
            if len(nums) == 0:
                nums = [0]*(power+1)
            num_at_power = math.floor(number/math.pow(self.base, power))
            nums[power] = int(num_at_power)
            number = number - num_at_power * math.pow(self.base, power)
            if number < self.base:
                if number > 0:
                    nums[0] = number
                break
        # s = []
        # for power,num_at_power in enumerate(nums):
        # 	s.append('{} * 3^{}'.format(num_at_power,power))
        # print(' + '.join(s))

        sToReturn = ''
        for i in reversed(nums):
            sToReturn += self.base_chars[int(i)]
        return sToReturn

    def encode(self, d):
        new_d = {}
        for key in d.keys():
            compressedKey = self.num2string(self.compressor['num'])
            if key not in self.compressor['fromKey']:
                self.compressor['fromKey'][key] = compressedKey
                self.compressor['key'][compressedKey] = key
                self.compressor['num'] += 1
            else:
                compressedKey = self.compressor['fromKey'][key]
            new_d[compressedKey] = d[key]
        return json.dumps(new_d)[1:-1]

    def decode(self, d_string):
        d = json.loads('{'+d_string+'}')
        new_d = {}
        for key in d.keys():
            new_d[self.compressor['key'][key]] = d[key]
        return new_d

    def dumps(self):
        return json.dumps(self.compressor)

    def loads(self, compressor_string):
        self.compressor = json.loads(compressor_string)

