m3m[1.65,2.0];
sig_m0_A1[1.777, 1.60, 2.0];
sig_sigma_A1[0.02, 0.0, 0.05];
sig_alpha_A1[ 1, -20., 20.]; 
sig_n_A1[2, 0.0, 5.0]; 
sig_gaus_sigmaA1[0.02,0.0,0.1];

t3m_sig_CBshape_A1  = CBShape(m3m, sig_m0_A1, sig_sigma_A1, sig_alpha_A1, sig_n_A1);
t3m_sig_GSshape_A1  = Gaussian(m3m,sig_m0_A1,sig_gaus_sigmaA1);


sig_m0_B1[1.777, 1.60, 2.0];
sig_sigma_B1[0.02, 0.0, 0.05];
sig_alpha_B1[ 1, -20., 20.]; 
sig_n_B1[2, 0.0, 5.0]; 
sig_gaus_sigmaB1[0.02,0.0,0.1];
t3m_sig_CBshape_B1  = CBShape(m3m, sig_m0_B1, sig_sigma_B1, sig_alpha_B1, sig_n_B1);
t3m_sig_GSshape_B1  = Gaussian(m3m,sig_m0_B1,sig_gaus_sigmaB1);


sig_m0_C1[1.777, 1.60, 2.0];
sig_sigma_C1[0.02, 0.0, 0.05];
sig_alpha_C1[ 1, -20., 20.]; 
sig_n_C1[2, 0.0, 5.0]; 
sig_gaus_sigmaC1[0.02,0.0,0.1];
t3m_sig_CBshape_C1  = CBShape(m3m, sig_m0_C1, sig_sigma_C1, sig_alpha_C1, sig_n_C1);
t3m_sig_GSshape_C1  = Gaussian(m3m,sig_m0_C1,sig_gaus_sigmaC1);

bkg_exp_slope_A1[-5.0,-6.0,-0.0];
bkg_exp_slope_B1[-5.0,-6.0,-0.0];
bkg_exp_slope_C1[-5.0,-6.0,-0.0];




sig_m0_A2[1.777, 1.60, 2.0];
sig_sigma_A2[0.02, 0.0, 0.05];
sig_alpha_A2[ 1, -20., 20.]; 
sig_n_A2[2, 0.0, 5.0]; 
sig_gaus_sigmaA2[0.02,0.0,0.1];

t3m_sig_CBshape_A2  = CBShape(m3m, sig_m0_A2, sig_sigma_A2, sig_alpha_A2, sig_n_A2);
t3m_sig_GSshape_A2  = Gaussian(m3m,sig_m0_A2,sig_gaus_sigmaA2);


sig_m0_B2[1.777, 1.60, 2.0];
sig_sigma_B2[0.02, 0.0, 0.05];
sig_alpha_B2[ 1, -20., 20.]; 
sig_n_B2[2, 0.0, 5.0]; 
sig_gaus_sigmaB2[0.02,0.0,0.1];
t3m_sig_CBshape_B2  = CBShape(m3m, sig_m0_B2, sig_sigma_B2, sig_alpha_B2, sig_n_B2);
t3m_sig_GSshape_B2  = Gaussian(m3m,sig_m0_B2,sig_gaus_sigmaB2);


sig_m0_C2[1.777, 1.60, 2.0];
sig_sigma_C2[0.02, 0.0, 0.05];
sig_alpha_C2[ 1, -20., 20.]; 
sig_n_C2[2, 0.0, 5.0]; 
sig_gaus_sigmaC2[0.02,0.0,0.1];
t3m_sig_CBshape_C2  = CBShape(m3m, sig_m0_C2, sig_sigma_C2, sig_alpha_C2, sig_n_C2);
t3m_sig_GSshape_C2  = Gaussian(m3m,sig_m0_C2,sig_gaus_sigmaC2);

bkg_exp_slope_A2[-5.0,-6.0,-0.0];
bkg_exp_slope_B2[-5.0,-6.0,-0.0];
bkg_exp_slope_C2[-5.0,-6.0,-0.0];





bkg_exp_offset[0.0,-10.0,10.0];
bkg_exp_shape  = RooExponential(m3m,bkg_exp_slope);



sqrtS[13000., 13000., 13000.];