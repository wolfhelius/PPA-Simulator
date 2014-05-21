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
        
    def Update(self):
        D = self.dbh[-1]
        S = self.species
        logH = S.aH + S.bH*log10(C.dbh[-1])
        C.height.append(10**logH)
        tile.patch[0].cohort[0] = C

        logH = S.
        self.height[len-1] = S.alpha_H_D*D^S.beta_H_D
        self.crownarea[len-1] = S.alpha_CA_D*D^S.beta_CA_D
        self.bsw[len-1] = 0
        # etc

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