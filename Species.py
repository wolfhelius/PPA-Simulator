# -*- coding: utf-8 -*-
"""
Created on May 14, 2014

@author: adamwolf
"""

"""
"Species": [
    {
    "id" = 1
    "species" = 3
    "startyear" = 1950 # make this into a datetime
    "age" : []
    "bl" : []
    "bw" : []    
    }
    ]

"""
    
class Species:
    def __init__(self, id):
    	self.id = 1
        self.Gc = 0
        self.Gu = 0
        self.MUc = 0
        self.MUu = 0
        self.F = 0
