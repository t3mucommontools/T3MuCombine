m3m[1.65,1.9];
sig_m0[1.777, 1.65, 2.0];
sig_sigma[0.02, 0.0, 0.05];
sig_alpha[ 1, -20., 20.]; 
sig_n[2, 0.0, 5.0]; 


t3m_sig_shape  = CBShape(m3m, sig_m0, sig_sigma, sig_alpha, sig_n);

bkg_exp_slope[-5.0,-10.0,0.0];



sqrtS[13000., 13000., 13000.]