Overview

PPA-testSort.py is test code. It generates nC cohorts of random diameter (0-10cm), calcs Zstar and relayers the cohorts, creating any necessary splits.

PPA-Simulator.py is prototype dynamics code.

5/21:
TODO: 
-) merge cohorts based on a max number of cohorts (per species?)
-) get G, MU, F into MakeSpecies
	?from FIA? See Purves, Appendix 1 & 2 for parameter estimation

-) Zstar and Relayer using flattop model where CR = phi*D^2, and phi = R40/40 (ie R = phi*D)
-) call FindZstar in Relayer