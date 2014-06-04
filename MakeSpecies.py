from PPA import Species
import numpy as np
import json

def MakeSpecies():
	# Purves et al crown envelope allometry
	f = './dat/CrownParms.dat'


	C0_Ro = 0.503
	C1_Ro = 3.126
	C0_R40 = 0.5
	C1_R40 = 10.0
	C0_B = 1.196
	C1_B = 0.511
	m2_per_ha = 10000

	cols = ['spcd','aa','bb','T','V']
	data = np.genfromtxt(f, dtype=None, names=cols, delimiter="\t", skip_header=2)

	nSpp = 260

	SpeciesList = []

	for iSpp in range(nSpp):
		S = Species(data['spcd'][iSpp])
		S.aH = data['aa'][iSpp]
		S.bH = data['bb'][iSpp]
		S.T = data['T'][iSpp]
		S.V = data['V'][iSpp]

		Ti = S.T
		S.B = (1-Ti)*C0_B + Ti*C1_B;
		S.Ro = (1-Ti)*C0_Ro + Ti*C1_Ro; 
		S.R40 = (1-Ti)*C0_R40 + Ti*C1_R40;

	   	SpeciesList.append(S)


	# # convert Species List into JSON
	# SpeciesJSON = {}
	# for key in SpeciesList:
	# 	SpeciesJSON[key] = SpeciesList[key].__dict__   	

	# with open('SpeciesList.json', 'w') as outfile:
	# 	json.dump(SpeciesJSON, outfile)

	return SpeciesList, nSpp