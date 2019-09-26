m3m[1.60,2.0];
sig_m0_A[1.777, 1.60, 2.0];
sig_sigma_A[0.02, 0.0, 0.05];
sig_alpha_A[ 1, -20., 20.]; 
sig_n_A[2, 0.0, 5.0]; 
t3m_sig_shape_A  = CBShape(m3m, sig_m0_A, sig_sigma_A, sig_alpha_A, sig_n_A);

sig_m0_B[1.777, 1.60, 2.0];
sig_sigma_B[0.02, 0.0, 0.05];
sig_alpha_B[ 1, -20., 20.]; 
sig_n_B[2, 0.0, 5.0]; 
t3m_sig_shape_B  = CBShape(m3m, sig_m0_B, sig_sigma_B, sig_alpha_B, sig_n_B);

sig_m0_C[1.777, 1.60, 2.0];
sig_sigma_C[0.02, 0.0, 0.05];
sig_alpha_C[ 1, -20., 20.]; 
sig_n_C[2, 0.0, 5.0]; 
t3m_sig_shape_C  = CBShape(m3m, sig_m0_C, sig_sigma_C, sig_alpha_C, sig_n_C);


bkg_exp_slope_A[-5.0,-6.0,-0.0];
bkg_exp_slope_B[-5.0,-6.0,-0.0];
bkg_exp_slope_C[-5.0,-6.0,-0.0];
bkg_exp_offset[0.0,-10.0,10.0];



bkg_exp_shape  = RooExponential(m3m,bkg_exp_slope);



sqrtS[13000., 13000., 13000.]