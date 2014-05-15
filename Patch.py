
class Patch:
    def __init__(self, id):
    	self.pid = id
        self.cohorts = []

	def PPA_Relayer(self):
		# PPA the cohorts
		# sort the cohorts by height
		# from tallest to shortest count the ground area
		# split cohorts at the boundaries
		# start new layer, continue until all cohorts have been layered