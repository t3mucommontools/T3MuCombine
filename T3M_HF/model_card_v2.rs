m3m[1.62,2.0];

sig_m0_A1[1.776, 1.775, 1.778];
sig_sigma_A1[0.010739, 0.00, 0.03];
sig_alpha_A1[1.88, 1.01, 6.];
sig_n_A1[2.48, 2.0, 4.0];
sig_gaus_sigma_A1[0.002, 0.00, 0.03];
cb_fraction_A1[0.5,0,1];

sig_m0_A[1.776, 1.775, 1.778];
sig_sigma_A[0.010, 0.00, 0.03];
sig_alpha_A[1.88, 1.01, 6.0];
sig_n_A[2.48, 2.0, 4.0];
sig_gaus_sigma_A[0.002, 0.00, 0.03];
cb_fraction_A[0.5,0,1];

t3m_sig_CBshape_A1_twoGlobalTracker  = CBShape(m3m, sig_m0_A, sig_sigma_A1, sig_alpha_A1, sig_n_A1);
t3m_sig_GSshape_A1_twoGlobalTracker  = Gaussian(m3m,sig_m0_A, sig_gaus_sigma_A1);

sig_m0_B1[1.776, 1.775, 1.778];
sig_sigma_B1[0.0172, 0.00, 0.3];
sig_alpha_B1[1.74, 1., 6];
sig_n_B1[3.57, 1.01, 4.];
sig_gaus_sigma_B1[0.006,0.00,0.03];
cb_fraction_B1[0.5,0,1];

sig_m0_B[1.776, 1.775, 1.778];
sig_sigma_B[0.0172, 0.00, 0.03];
sig_alpha_B[1.74, 1., 6.0];
sig_n_B[3.57, 1.01, 4.0];
sig_gaus_sigma_B[0.006,0.00,0.03];
cb_fraction_B[0.5,0,1];

t3m_sig_CBshape_B1_twoGlobalTracker  = CBShape(m3m, sig_m0_B, sig_sigma_B1, sig_alpha_B, sig_n_B);
t3m_sig_GSshape_B1_twoGlobalTracker  = Gaussian(m3m,sig_m0_B, sig_gaus_sigma_B1);

sig_m0_C1[1.776, 1.775, 1.778];
sig_sigma_C1[0.02308, 0.01, 0.03];
sig_alpha_C1[1.9734, 1.87, 2.];
sig_n_C1[4.01, 4.00, 4.2];
sig_gaus_sigma_C1[0.006, 0.01, 0.03];
cb_fraction_C1[0.875,0,1];

sig_m0_C[1.776, 1.775, 1.778];
sig_sigma_C[0.0223, 0.01, 0.03];
sig_alpha_C[1.9734, 1.87, 6.];
sig_n_C[4.01, 1.01, 6.0];
sig_gaus_sigma_C[0.0223, 0.01, 0.03];
cb_fraction_C[0.875,0,1];

t3m_sig_CBshape_C1_twoGlobalTracker  = CBShape(m3m, sig_m0_C, sig_sigma_C1, sig_alpha_C, sig_n_C);
t3m_sig_GSshape_C1_twoGlobalTracker  = Gaussian(m3m,sig_m0_C, sig_gaus_sigma_C1);

sig_m0_A2[1.776, 1.775, 1.778];
sig_sigma_A2[0.0104, 0.00, 0.03];
sig_alpha_A2[1.7425, 1.01, 6.];
sig_n_A2[2.52, 1.01, 4.0];
sig_gaus_sigma_A2[0.006, 0.00, 0.03];
cb_fraction_A2[0.5,0,1];

t3m_sig_CBshape_A2_twoGlobalTracker  = CBShape(m3m, sig_m0_A, sig_sigma_A2, sig_alpha_A, sig_n_A);
t3m_sig_GSshape_A2_twoGlobalTracker  = Gaussian(m3m,sig_m0_A, sig_gaus_sigma_A2);

sig_m0_B2[1.776, 1.775, 1.778];
sig_sigma_B2[0.0175, 0.00, 0.03];
sig_alpha_B2[1.777, -1., 20.];
sig_n_B2[3.2769, 3.1, 100.];
sig_gaus_sigma_B2[0.006,0.00,0.03];
cb_fraction_B2[0.5,0,1];

t3m_sig_CBshape_B2_twoGlobalTracker  = CBShape(m3m, sig_m0_B, sig_sigma_B2, sig_alpha_B, sig_n_B);
t3m_sig_GSshape_B2_twoGlobalTracker  = Gaussian(m3m,sig_m0_B, sig_gaus_sigma_B2);

sig_m0_C2[1.776, 1.775, 1.778];
sig_sigma_C2[0.02366, 0.01, 0.03];
sig_alpha_C2[1.778, 1., 6.];
sig_n_C2[5.52, 1.01, 6.0];
sig_gaus_sigma_C2[0.006, 0.01, 0.03];
cb_fraction_C2[0.867,0,1];

t3m_sig_CBshape_C2_twoGlobalTracker  = CBShape(m3m, sig_m0_C, sig_sigma_C2, sig_alpha_C, sig_n_C);
t3m_sig_GSshape_C2_twoGlobalTracker  = Gaussian(m3m,sig_m0_C, sig_gaus_sigma_C2);

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

bkg_norm_A1[0.0,0.0,100000.0];
bkg_norm_A2[0.0,0.0,100000.0];
bkg_norm_A3[0.0,0.0,100000.0];
bkg_norm_B1[0.0,0.0,100000.0];
bkg_norm_B2[0.0,0.0,100000.0];
bkg_norm_B3[0.0,0.0,100000.0];
bkg_norm_C1[0.0,0.0,100000.0];
bkg_norm_C2[0.0,0.0,100000.0];
bkg_norm_C3[0.0,0.0,100000.0];

bkg_powerlaw_slope_A1[-1.0,-10.0,1.0];
bkg_powerlaw_slope_A2[-1.0,-10.0,1.0];

bkg_powerlaw_slope_B1[-1.0,-10.0,1.0];
bkg_powerlaw_slope_B2[-1.0,-10.0,1.0];

bkg_powerlaw_slope_C1[-1.0,-10.0,1.0];
bkg_powerlaw_slope_C2[-1.0,-10.0,1.0];
