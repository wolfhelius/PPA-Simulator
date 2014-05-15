# Initial Development of PPA Forest Dynamics Simulator

from Tile import Tile
from Patch import Patch, PPA_Relayer
from Cohort import Cohort, UpdateBiomassAllometrically
from Species import Species

from SpeciesDefs import *

# run parameters
year = 0
dt = 0.2 # years
nYear = 100
nextPID = 0
nextCID = 0

# make a tile with one patch one cohort
tile = Tile(0)
tile.patch[0] = Patch(nextPID)
nextPID += 1
tile.patch[0].cohort[0] = Cohort(nextCID)
nextCID += 1


# initialize cohorts
tile.patch[0].cohort[0].species = Species(0)
tile.patch[0].cohort[0].startyear = year
tile.patch[0].cohort[0].species=Species(0)
S = tile.patch[0].cohort[0].species
tile.patch[0].cohort[0].age[0]=0
tile.patch[0].cohort[0].dbh[0]=1
C = tile.patch[0].cohort[0]
C.dbh[0] = 1
C.nidivs[0] = 20 
C.UpdateBiomassAllometrically()

# start the simulation
for iT in range(nYear*dt):
	for iP in tile:
		P = tile.patch[iP]
		if ((iT % 1/dt) == 0):
			# PPA the cohorts
			# Merge cohorts of similar size 
		for iC in patch:
			C = P.cohort[iC]
			S = C.species

			# dynamics
			if (C.layer[iT] == 0):
				G = S.Gc
				MU = S.MUc
				F = S.Fc
			else:
				G = S.Gu
				MU = S.MUu
				F = S.Fu

			C.dbh[iT+1] = C.dbh[iT] + G*dt
			C.nindivs[iT+1] = C.indivs[iT]*(1-MU*dt)
			C.UpdateBiomassAllometrically()

			# new cohorts
			if (C.layer[iT] == 0): # add other constraints as need be, ie minimum age
				Cnew = Cohort(nextCID)
				Cnew.species = S # if we wanted evolution it would happen here
				Cnew.dbh[0] = 1
				Cnew.nindivs[0] = F * C.crownarea[iT+1]*C.nindivs[iT+1]
				Cnew.UpdateBiomassAllometrically()
				P.cohorts.push(Cnew)








