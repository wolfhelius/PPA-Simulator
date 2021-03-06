# Initial Development of PPA Forest Dynamics Simulator

from random import random, randint

from PPA import *

from MakeSpecies import MakeSpecies

SpeciesList, nSpp = MakeSpecies()

global nextPID, nextCID
nextPID = 0
nextCID = 0

nP = 1
nC = 10

# make a tile with one patch one cohort
tile = Tile(0)
for iP in range(nP):
    tile.patch.append(Patch(nextPID))
    nextPID += 1
    for iC in range(nC):
    	test = log10(pi)
        tile.patch[iP].cohort.append(Cohort(nextCID))
        nextCID += 1

        # initialize cohorts
        C = tile.patch[iP].cohort[iC]
        #C.species = SpeciesList[randint(0,2-1)]
        C.species = SpeciesList[randint(0,1)]
        D = 10*random()
        C.dbh.append(D)
        C.UpdateH()
        C.nindivs.append(0.05)
        tile.patch[iP].cohort[iC] = C

    tile.patch[iP].Relayer()






