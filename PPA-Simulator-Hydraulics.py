# Initial Development of PPA Forest Dynamics Simulator

from random import random, randint

from PPA import *

from MakeSpecies import MakeSpecies

SpeciesList, nSpp = MakeSpecies()

# run parameters
year = 0
dt = 0.2 # years
nYear = 100
global nextPID, nextCID
nextPID = 0
nextCID = 0

nP = 1
nC = 10

# Initialize cohorts
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
        C.species = SpeciesList[randint(0,nSpp-1)]
        C.startyear = year
        D = 5*random()
        C.dbh.append(D)
        C.UpdateH()
        C.nindivs.append(0.05)
        C.UpdateB()
        tile.patch[iP].cohort[iC] = C

    tile.patch[iP].Relayer()
    tile.patch[iP].MergeCohorts()

# run the simulation
for iT in range(nYear*dt):
    for iP in tile:
        P = tile.patch[iP]
        for iC in patch:
            C = P.cohort[iC]
            S = C.species

            # fast timestep
            # photosynthesis
            # water demand / hydraulics
            # soil leaching, evap, rain

            # allocation

            C.dbh.append(C.dbh[iT] + G*dt)

            C.UpdateH()
            C.UpdateB()

            # slow timestep (annual)
            if ((iT % 1/dt) == 0):
    	        tile.patch[iP].Relayer()
    	        tile.patch[iP].MergeCohorts()

                # make sure dT is dt_slow
                C.nindivs.append(C.indivs[iT]*(1-MU*dt))

                # new cohorts
                if (C.layer[iT] == 0): # add other constraints as need be, ie minimum age
                    Cnew = Cohort(nextCID)
                    nextCID += 1
                    Cnew.species = S # if we wanted evolution it would happen here
                    Cnew.dbh.append(1)
                    Cnew.UpdateH()
                    Cnew.nindivs.append(F * C.crownarea[-1]*C.nindivs[-1])
                    Cnew.startyear = iT+1
                    Cnew.UpdateB()
                    P.cohorts.push(Cnew)

            # end of timestep
            P.cohort[iC] = C
        tile.patch[iP] = P






