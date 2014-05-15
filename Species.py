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
    	self.sid = 1
        self.G = 0
        self.Gu = 0
        self.MUc = 0
        self.MUu = 0
        self.Fc = 0
        self.Fu = 0
        self.alpha_H_D = 0
        self.beta_H_D = 0
        self.alpha_CR_D = 0
        self.beta_CR_D = 0
        self.Vmax = 0
        self.k = 0.5
        self.LUE = 0
