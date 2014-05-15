# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 22:41:22 2013

@author: adamwolf
"""

"""
"cohorts": [
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
    
from Species import Species

class Cohort:
    def __init__(self, id):
        self.cid = id
        self.startyear = 0
        self.species=Species(0)
        self.age=[]
        self.bliving=[]
        self.br=[]
        self.bseed=[]
        self.bsw=[]
        self.bwood=[]
        self.crownarea=[]
        self.dbh=[]
        self.height=[]
        self.layer=[]
        self.nindivs=[]
        self.nsc=[]
        self.bl=[]
        
    def UpdateBiomassAllometrically(self):
        i = self.dbh.len()-1
        D = self.dbh[len]
        S = self.species
        self.height[len-1] = S.alpha_H_D*D^S.beta_H_D
        self.crownarea[len-1] = S.alpha_CA_D*D^S.beta_CA_D
        self.bsw[len-1] = 0
        # etc