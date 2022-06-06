m3m[1.62,2.0];
sig_m0_A[1.776, 1.775, 1.778];
sig_sigma_A[0.010, 0.00, 0.05];
sig_alpha_A[ 1, -5., 5.];
sig_n_A[1, 0.0, 5.0];
sig_gaus_sigma_A[0.021,0.01,0.05];
cb_fraction_A[0.5,0,1];

t3m_sig_CBshape_A_twoGlobalTracker  = CBShape(m3m, sig_m0_A, sig_sigma_A, sig_alpha_A, sig_n_A);
t3m_sig_GSshape_A_twoGlobalTracker  = Gaussian(m3m,sig_m0_A,sig_gaus_sigma_A);


sig_m0_B[1.776, 1.775, 1.778];
sig_sigma_B[0.02, 0.00, 0.5];
sig_alpha_B[ 1, -20., 20.];
sig_n_B[2, 0.0, 5.0];
sig_gaus_sigma_B[0.02,0.00,0.5];
cb_fraction_B[0.5,0,1];

t3m_sig_CBshape_B_twoGlobalTracker  = CBShape(m3m, sig_m0_B, sig_sigma_B, sig_alpha_B, sig_n_B);
t3m_sig_GSshape_B_twoGlobalTracker  = Gaussian(m3m,sig_m0_B,sig_gaus_sigma_B);


sig_m0_C[1.776, 1.775, 1.778];
sig_sigma_C[0.02, 0.00, 0.5];
sig_alpha_C[ 1, -20., 20.];
sig_n_C[2, 0.0, 5.0];
sig_gaus_sigma_C[0.02,0.00,0.5];
cb_fraction_C[0.5,0,1];

t3m_sig_CBshape_C_twoGlobalTracker  = CBShape(m3m, sig_m0_C, sig_sigma_C, sig_alpha_C, sig_n_C);
t3m_sig_GSshape_C_twoGlobalTracker  = Gaussian(m3m,sig_m0_C,sig_gaus_sigma_C);


bkg_exp_slope_A1[-1.0,-1000.0,100.0];
bkg_exp_slope_A2[-1.0,-1000.0,100.0];
bkg_exp_slope_B1[-1.0,-1000.0,100.0];
bkg_exp_slope_B2[-1.0,-1000.0,100.0];
bkg_exp_slope_C1[-1.0,-1000.0,100.0];
bkg_exp_slope_C2[-1.0,-1000.0,100.0];


bkg_exp_offset_A1[0.0,0.0,10000.0];
bkg_exp_offset_A2[0.0,0.0,10000.0];
bkg_exp_offset_B1[0.0,0.0,10000.0];
bkg_exp_offset_B2[0.0,0.0,10000.0];
bkg_exp_offset_C1[0.0,0.0,10000.0];
bkg_exp_offset_C2[0.0,0.0,10000.0];

t3m_bkg_expo_A1  = Exponential(m3m, bkg_exp_slope_A1);
t3m_bkg_expo_A2  = Exponential(m3m, bkg_exp_slope_A2);
t3m_bkg_expo_B1  = Exponential(m3m, bkg_exp_slope_B1);
t3m_bkg_expo_B2  = Exponential(m3m, bkg_exp_slope_B2);
t3m_bkg_expo_C1  = Exponential(m3m, bkg_exp_slope_C1);
t3m_bkg_expo_C2  = Exponential(m3m, bkg_exp_slope_C2);

bkg_powerlaw_slope_A1[-1.0,-10.0,1.0];
bkg_powerlaw_slope_A2[-1.0,-10.0,1.0];

bkg_powerlaw_slope_B1[-1.0,-10.0,1.0];
bkg_powerlaw_slope_B2[-1.0,-10.0,1.0];

bkg_powerlaw_slope_C1[-1.0,-10.0,1.0];
bkg_powerlaw_slope_C2[-1.0,-10.0,1.0];

sqrtS[13000., 13000., 13000.]
