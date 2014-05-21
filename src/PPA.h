
#ifndef PPA_H
#define PPA_H

#define C0_Ro 0.503
#define C1_Ro 3.126
#define C0_R40 0.5
#define C1_R40 10.0
#define C0_B 1.196
#define C1_B 0.511
#define m2_per_ha 10000

int fascend (const void * a, const void * b);
int fdescend (const void * a, const void * b);

struct tree_struct {
	float D, H, R, A, X, Y;
};

class Stand {
private:

	int Nspp;
	int *spID_vec;
	float *T;
	float *V;
	float *aa, *bb;
	
	void calculate_SizeDist();
	void read_CrownParms();
	int getIsp(int spID);
	void calculate_Zstar();
	void CopyToTreeStruct();

	
public:
	float k, lambda, dx;
	float Zstar, Zdiff;
	float *D, *H, *R, *A;
	int N_tot, N_can, N_und;
	float canopy_fraction;
	tree_struct *trees; 
	
	float m_ground_area;
	
	int spID, ispp;
	
	Stand(float k = 0.2, float lambda = 1.1, int N_tot = 1000, float dx = 100., int spID = 91);
	~Stand();
	
	void Sort();
	void Shuffle();
	
};

#endif