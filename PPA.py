# PPA Class Defs
from math import pi, log10

import numpy as np

class Species:
    def __init__(self, id):
        self.sid = 1
        self.G = 0
        self.Gu = 0
        self.MUc = 0
        self.MUu = 0
        self.Fc = 0
        self.Fu = 0
        self.aH = 0
        self.bH = 0
        self.Vm = 0
        self.k = 0.5
        self.LUE = 0
        self.B = 0;
        self.Ro = 0
        self.R40 = 0
        self.V = 0

class Tile:
    def __init__(self, id):
        self.tid = id
        self.patch = []

class Patch:

    global flattop
    flattop = True

    def __init__(self, id):
        self.pid = id
        self.cohort = []
        self.Zstar = []

    def MergeCohorts(self):
        maxC = 20

        CC = self.cohort
        CC = sorted(CC, key=lambda cohort: cohort.dbh[-1], reverse=True)

        maxD = log(CC[0].dbh[-1])
        minD = log(CC[-1].dbh[-1])
        Dedges, dD = np.linspace(maxD, minD, num=maxC+1, retstep=True)

        nL = self.cohort[-1].layer[-1]

        SS = []
        for C in CC:
            SS.append(C.species)

        # SS = [SS.append(C.species) for C in CC]
        SS = set(SS)
        nS = len(SS)

        # the list where the merged cohorts will be pushed
        CM = []

        for iS in range(nS):
            for iL in range (nL):
                CSL = []
                for C in CC:
                    if (C.species == SS[iS]) & (C.layer[-1] = iL):
                        CSL.append(C)
                iD = 0
                iC = 0
                while (True):
                    # base case
                    if (iC == len(CSL)):
                        break

                    C = CSL[iC]

                    # make upper range boundary above or equal current cohort
                    # iD is upper range boundary
                    if (C.dbh[-1]>Dedges[iD]):
                        iD += 1
                    else:
                        break

                    while (True):   
                        # Gobble smaller cohorts in same size class
                        if (iC+1 < len(CSL)) & (CSL[iC+1].dbh[-1] >=Dedges[iD]):                            
                            C.Merge(CSL[iC+1])
                            iC += 1
                        else:
                            # Finish if no smaller cohorts, or no more cohorts at all
                            CM.append(C)
                            iC += 1
                            break
                for iC in range(len(CSL)):
                    CM.append(CSL[iC])

        self.cohort = CM

    def Relayer(self):
        # Allows for multiple layers, assumes Zstar and crown areas known a priori
        # Updates Patch.Zstar
        # Updates Patch.Cohort array with new array, including any splits
        # Updates Cohort.Layer

        self.cohort = sorted(self.cohort, key=lambda cohort: cohort.height[-1], reverse=True)
        nC = len(self.cohort)

        global flattop
        if (not(flattop)):
            self.FindZstar()
        else:
            for iC in range(nC):
                C = self.cohort[iC]
                D = C.dbh[-1]
                S = C.species
                phi = S.R40/40
                R = phi*D
                C.crownarea.append(pi*R**2) 
                self.cohort[iC] = C

        CC = [] # temporary structure to allow splitting
        GA = 0
        layer = 0
        Z = self.cohort[0].height[-1]
        for iC in range(nC):
            C = self.cohort[iC]
            S = C.species
            dCA = C.crownarea[-1]*C.nindivs[-1]
            if (GA + dCA < 1):
                C.layer.append(layer)
                CC.append(C)
            else:
                ratio =  (1 - GA)/(dCA)
                C2 = C.Split(ratio)
                C.layer.append(layer)
                if (layer == 0):
                    self.Zstar.append(C.height[-1])
                layer += 1
                C2.layer.append(layer)
                GA = dCA*(1-ratio)
                CC.append(C)
                CC.append(C2)
        self.cohort = CC

    def FindZstar(self):
        # Allows for only a single Zstar
        # Updates Patch.Cohort.Crownarea
        nC = len(self.cohort)
        iZ0 = 0
        iZ1 = nC-1
        count = 0
        # O(logN) operation to find Zstar
        while (True):
            count += 1
            iZ = int((iZ1 + iZ0)/2)
            Z = self.cohort[iZ].height[-1]
            GA = 0
            for iC in range(nC):
                C = self.cohort[iC]
                H = C.height[-1]
                if (H >= Z):
                    S = C.species
                    D = C.dbh[-1]
                    Rmax = S.Ro + (S.R40-S.Ro)*(D/40)
                    M = 0.95
                    R = Rmax*(min(H-Z, H*M)/H*M)**S.B
                    dCA = pi*R**2 * C.nindivs[-1] 
                    GA = GA + dCA
                else:
                    break
        
            # we have Zstar
            if (iZ == iZ0) | (count > nC/2):
                # Algorithm ends when iZ0 and iZ1 bound the solution
                if (iZ1 < nC-1):
                    # Zstar is the height of iZ0, even though this does not fill GA
                    Zstar = self.cohort[iZ0].height[-1]
                else:
                    # if iZ1 is the final cohort, then sum(CA)< GA
                    Zstar = 0

                # Zstar in hand, get crown areas
                # Sum(CA)<GA because "true" Zstar is between iZ0 and iZ1
                # CA of cohort iZ1 set to Rmax
                for iC in range(nC):
                    C = self.cohort[iC]
                    S = C.species
                    D = C.dbh[-1]
                    H = C.height[-1]
                    Rmax = S.Ro + (S.R40-S.Ro)*(D/40)
                    M = 0.95
                    if (H >= Zstar):
                        # Crown radius defined by diameter and height above Zstar
                        R = Rmax*(min(H-Z, H*M)/H*M)**S.B
                    else:
                        # Crown radius determined by diameter only
                        R = Rmax
                    C.crownarea.append(pi*R**2) 
                    self.cohort[iC] = C

                break

            if (GA > 1):
                # iZ is too large
                iZ1 = iZ
            else:
                # iZ is too small
                iZ0 = iZ;


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
        
    def UpdateH(self):
        D = self.dbh[-1]
        S = self.species
        logH = S.aH + S.bH*log10(D)
        H = 10**logH
        self.height.append(H)

    def UpdateB(self):
        # stub for update biomass
        D = self.dbh[-1]
        S = self.species
        

    def Split(self, ratio):
        global nextPID, nextCID

        C = self
        C.cid = nextCID
        nextCID += 1

        self.bliving=self.bliving*ratio
        self.br=self.br*ratio
        self.bseed=self.bseed*ratio
        self.bsw=self.bsw*ratio
        self.bwood=self.bwood*ratio
        self.crownarea=self.crownarea*ratio
        self.dbh=self.dbh*ratio
        self.height=self.height*ratio
        self.layer=self.layer*ratio
        self.nindivs=self.nindivs*ratio
        self.nsc=self.nsc*ratio
        self.bl=self.bl*ratio

        C.bliving=C.bliving*(1-ratio)
        C.br=C.br*(1-ratio)
        C.bseed=C.bseed*(1-ratio)
        C.bsw=C.bsw*(1-ratio)
        C.bwood=C.bwood*(1-ratio)
        C.crownarea=C.crownarea*(1-ratio)
        C.dbh=C.dbh*(1-ratio)
        C.height=C.height*(1-ratio)
        C.layer=C.layer*(1-ratio)
        C.nindivs=C.nindivs*(1-ratio)
        C.nsc=C.nsc*(1-ratio)
        C.bl=C.bl*(1-ratio)

        return C

    # https://docs.python.org/2/reference/datamodel.html
    def __cmp__(self, other):

        test = self.height[-1] - other.height[-1]
        if (test<0):
            return -1
        else:
            if (test>0):
                return 1
            else:
                return 0        

    # def __repr__(self):
    #     return repr((self.cid, self.dbh, self.height, self.crownarea, self.layer))

