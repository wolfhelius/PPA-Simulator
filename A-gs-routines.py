# Photosynthesis and stomatal conductance routines

# Constants (Farrior et al 2013): averages of sun and shade leaves from deciduous trees
Lnot = 1200		# Light at top of crown
Vmax = 0.6 		# Vcmax
k = 0.33		# Light extinction coefficient for Beer's law
l.tilda = 2 	# Number of leaf layers that operate at light-satureated photosynthetic rate
alpha_f = Vmax/Lnot*exp(l.tilda*k)
	
# Calculate water-saturated canopy photosynthetic rate (AL); from Farrior et al. 2013 Appendix A
def Acan(l,L):
	ltilda = 1/k*log(alpha_f*L/Vmax)
	if  (l<=ltilda):
		AL = Vmax*l 
	if	(ltilda<l):
		if	(ltilda > 0):
			AL = Vmax/k*(1+log(alpha_f*L/Vmax) - alpha_f*L/Vmax*exp(-k*l))
	if(ltilda<0):
		AL = alpha_f * L /k *(1-exp(-k*l))
	print(AL)

# Calculate water-saturated canopy-level stomatal conductance using Ball-Berry
m = 10 		# Slope of BB
Cs = 300	# CO2 concentration at leaf surface
gs=m*Cs*A 	# Uses canopy integrated A
