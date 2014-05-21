#include "math.h"
#include <string.h>
#include <fstream>
#include <iostream>
#include <algorithm>

#include "PPA.h"

using namespace std;

Stand::Stand(float k_in, float lambda_in, int N_tot_in, float dx_in, int spID_in) :
	k(k_in), lambda(lambda_in), spID(spID_in), dx(dx_in)
{

	m_ground_area = dx_in*dx_in;
	N_tot = (int) N_tot_in*m_ground_area/m2_per_ha;

	D = new float[N_tot];
	H = new float[N_tot];
	R = new float[N_tot];
	A = new float[N_tot];
		
	calculate_SizeDist();
	read_CrownParms();
	ispp = getIsp(spID);
	calculate_Zstar();
	CopyToTreeStruct();
	
}

Stand::~Stand(){

	delete [] trees;
	
	delete [] spID_vec;
	delete [] T;
	delete [] V;
	delete [] aa;
	delete [] bb;

}

int fascend (const void * a, const void * b)
{
	return ( *(float*)a - *(float*)b );
}

int fdescend (const void * a, const void * b)
{
	if (*(float*)b-*(float*)a < 0) return -1;
	if (*(float*)b-*(float*)a > 0) return  1;
	return 0;
}

//		struct st_ex { 
//			char product[16];
//			float price;
//		};
//
//		/* qsort struct comparision function (price float field) */
//		int struct_cmp_by_price(const void *a, const void *b)
//		{
//			struct st_ex *ia = (struct st_ex *)a;
//			struct st_ex *ib = (struct st_ex *)b;
//			return (int)(100.f*ia->price - 100.f*ib->price);
//			/* float comparison: returns negative if b > a 
//			 and positive if a > b. We multiplied result by 100.0
//			 to preserve decimal fraction */
//			
//		} 

int fdescend_treestruct (const void *a, const void *b)
{
    struct tree_struct *tree_a = (struct tree_struct *)a;
    struct tree_struct *tree_b = (struct tree_struct *)b;
	
	if (tree_b->D - tree_a->D < 0) return -1;
	if (tree_b->D - tree_a->D > 0) return  1;
	return 0;
}

int Stand::getIsp(int spID){
	for(int i=0; i<Nspp; i++){
		if (spID_vec[i] == spID) return i;
	}
}


void Stand::calculate_SizeDist(){
	
	// simulate D for N points 
	float inv_k = 1./k;
	float U;
	float rm = (float) RAND_MAX + 1.f;
	for (int iN=0; iN<N_tot; iN++){
		float testD = 0.f;
		while ((testD > 100.) || (testD < 1.f)){
			U = -log(rand()/rm);
			testD = lambda*(pow(U,inv_k)) * 100.;
		}		
		D[iN] = testD;
	}
	// qsort D
	qsort(D, N_tot, sizeof(float), fdescend);

}

void Stand::read_CrownParms(){

	ifstream cp_file("CrownParms.dat");
		
	string line;
	char * cline;
	getline(cp_file, line); // read header
	getline(cp_file, line);
	Nspp = atoi(line.c_str());
	
	spID_vec = new int[Nspp];
	T = new float[Nspp];
	V = new float[Nspp];
	aa = new float[Nspp];
	bb = new float[Nspp];

	for(int ispp = 0; ispp<Nspp; ispp++){
		cp_file >> spID_vec[ispp] >> aa[ispp] >> bb[ispp] >> T[ispp] >> V[ispp];
		//cout << spID_vec[ispp] << "\t" << aa[ispp] << "\t" << bb[ispp] << "\t" << T[ispp] << "\t" << V[ispp] << endl;
	}
					
}

void Stand::calculate_Zstar(){
	float Ti = T[ispp];
	float a = aa[ispp];
	float b = bb[ispp];
	
	float B = (1-Ti)*C0_B + Ti*C1_B;
	float Ro = (1-Ti)*C0_Ro + Ti*C1_Ro; 
	float R40 = (1-Ti)*C0_R40 + Ti*C1_R40;
	float M = 0.95;
	B = 1; // this sets the crown shape to a cone to be fair to pbrt
	
	float *logH, *Rmax, *HM;
	logH = new float[N_tot];
	HM = new float[N_tot];
	Rmax = new float[N_tot];
	
	for(int i = 0; i<N_tot; i++){
		logH[i] = a + b*log10(D[i]);
		H[i] = pow(10.f, logH[i]);
		Rmax[i] = Ro + (R40-Ro)*(D[i]/40);
		HM[i] = H[i]*M;
		//printf("D = %f\tlogH = %f\tH = %f\n", D[i], logH[i], H[i]);
	}

	// This is an O(logn) algorithm for fast execution
	int iZ_lower = 0;
	int iZ_upper = N_tot;
	int iZ;
	int count = 0;
	float A_cum_upper = 0;
	while(true){
		count++;
		iZ = (iZ_upper + iZ_lower) / 2;
		float Z = H[iZ];
		float A_cum = 0;
		for(int iN = 0; iN<N_tot; iN++){
			R[iN] = (H[iN] >= Z) ? Rmax[iN]*pow(min(H[iN]-Z, HM[iN])/HM[iN], B) : 0.f;
			A[iN] = M_PI*R[iN]*R[iN];
			A_cum = A_cum + A[iN];
		}
		//printf("iZ_lower: %u\tiZ_upper: %u\tiZ: %u\tA_cum: %f\n", iZ_lower, iZ_upper, iZ, A_cum);
		
		if (A_cum > m_ground_area){
			// iZ is too large
			A_cum_upper = A_cum;
			iZ_upper = iZ;
		} else {
			// iZ is too small
			iZ_lower = iZ;
		}
		
		if (iZ_upper - iZ_lower == 1){
			if (A_cum_upper > m_ground_area){
				Zstar = Z;
			} else {
				Zstar = 0.f;
			}
			N_can = iZ;
			N_und = N_tot - N_can;
			Zdiff = H[0] - Z;
			break;
		}
	}
	
	
	canopy_fraction = (float) N_can / (float) N_tot;
	printf("Canopy Trees: \t%u\tZstar\t%6.2f\tcanopy fraction: %6.2f\n", N_can, Zstar, canopy_fraction);

	delete [] logH; 
	delete [] Rmax;
	delete [] HM;
}

void Stand::CopyToTreeStruct(){
	
	trees = new tree_struct[N_can];
	for(int i=0; i<N_can; i++){
		trees[i].D = D[i];
		trees[i].H = H[i];
		trees[i].R = R[i];
		trees[i].A = A[i];
		//at this point coordinates haven't been assigned
		//trees[i].X = X[i];
		//trees[i].Y = Y[i];
		
	}
	
	delete [] D;
	delete [] H;
	delete [] R;
	delete [] A;
	
}

void Stand::Sort(){
	
	// qsort tree_struct array trees
	qsort(trees, N_can, sizeof(tree_struct), fdescend_treestruct);
	return;

}

void Stand::Shuffle(){
	int N = N_can;
	while (N>1){
		int k;
		
		k = rand() % N;
		N--;
		tree_struct temp = trees[N];
		trees[N] = trees[k];
		trees[k] = temp;
		
	}
	return;
	
}

