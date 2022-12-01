m3m[1.62,2.0];

sig_alpha_A[ 1, -10., 10.];
sig_n_A[0.2, 0.0, 200.0];
sig_m0_A[1.776, 1.775, 1.778];

sig_sigma_A1[0.010, 0.00, 0.8];
sig_gaus_sigma_A1[0.01,0.00001,0.8];

t3m_sig_CBshape_A1_twoGlobalTracker  = CBShape(m3m, sig_m0_A, sig_sigma_A1, sig_alpha_A, sig_n_A);
t3m_sig_GSshape_A1_twoGlobalTracker  = Gaussian(m3m,sig_m0_A, sig_gaus_sigma_A1);

sig_sigma_A2[0.010, 0.00, 0.8];
sig_gaus_sigma_A2[0.01,0.00001,0.8];

t3m_sig_CBshape_A2_twoGlobalTracker  = CBShape(m3m, sig_m0_A, sig_sigma_A2, sig_alpha_A, sig_n_A);
t3m_sig_GSshape_A2_twoGlobalTracker  = Gaussian(m3m,sig_m0_A, sig_gaus_sigma_A2);

cb_fraction_A1[0.5,0,1];
cb_fraction_A2[0.5,0,1];
////////////////

sig_alpha_B[ 1, -10., 10.];
sig_n_B[1.0, 0.0, 200.0];
sig_m0_B[1.776, 1.775, 1.778];

sig_sigma_B1[0.02, 0.00, 0.3];
sig_gaus_sigma_B1[0.01,0.0000,0.3];

t3m_sig_CBshape_B1_twoGlobalTracker  = CBShape(m3m, sig_m0_B, sig_sigma_B1, sig_alpha_B, sig_n_B);
t3m_sig_GSshape_B1_twoGlobalTracker  = Gaussian(m3m,sig_m0_B, sig_gaus_sigma_B1);

sig_sigma_B2[0.02, 0.00, 0.3];
sig_gaus_sigma_B2[0.01,0.0000,0.3];

t3m_sig_CBshape_B2_twoGlobalTracker  = CBShape(m3m, sig_m0_B, sig_sigma_B2, sig_alpha_B, sig_n_B);
t3m_sig_GSshape_B2_twoGlobalTracker  = Gaussian(m3m,sig_m0_B, sig_gaus_sigma_B2);

cb_fraction_B1[0.1,0.00,1];
cb_fraction_B2[0.1,0.00,1];
////////////////

sig_alpha_C[ 1, -10., 10.];
sig_n_C[0.2, 0.0, 200.0];
sig_m0_C[1.776, 1.775, 1.778];

sig_sigma_C1[0.03, 0.00, 0.8];
sig_gaus_sigma_C1[0.01,0.00001,0.8];

t3m_sig_CBshape_C1_twoGlobalTracker  = CBShape(m3m, sig_m0_C, sig_sigma_C1, sig_alpha_C, sig_n_C);
t3m_sig_GSshape_C1_twoGlobalTracker  = Gaussian(m3m,sig_m0_C, sig_gaus_sigma_C1);

sig_sigma_C2[0.03, 0.00, 0.8];
sig_gaus_sigma_C2[0.01,0.00001,0.8];

t3m_sig_CBshape_C2_twoGlobalTracker  = CBShape(m3m, sig_m0_C, sig_sigma_C2, sig_alpha_C, sig_n_C);
t3m_sig_GSshape_C2_twoGlobalTracker  = Gaussian(m3m,sig_m0_C, sig_gaus_sigma_C2);

cb_fraction_C1[0.5,0,1];
cb_fraction_C2[0.5,0,1];
////////////////

bkg_exp_slope_twoGlobalTracker_2017_A1[-1.0,-1000.0,100.0];
bkg_exp_slope_twoGlobalTracker_2017_A2[-1.0,-1000.0,100.0];
bkg_exp_slope_twoGlobalTracker_2017_B1[-1.0,-1000.0,100.0];
bkg_exp_slope_twoGlobalTracker_2017_B2[-1.0,-1000.0,100.0];
bkg_exp_slope_twoGlobalTracker_2017_C1[-1.0,-1000.0,100.0];
bkg_exp_slope_twoGlobalTracker_2017_C2[-1.0,-1000.0,100.0];

bkg_exp_slope_twoGlobalTracker_2018_A1[-1.0,-1000.0,100.0];
bkg_exp_slope_twoGlobalTracker_2018_A2[-1.0,-1000.0,100.0];
bkg_exp_slope_twoGlobalTracker_2018_B1[-1.0,-1000.0,100.0];
bkg_exp_slope_twoGlobalTracker_2018_B2[-1.0,-1000.0,100.0];
bkg_exp_slope_twoGlobalTracker_2018_C1[-1.0,-1000.0,100.0];
bkg_exp_slope_twoGlobalTracker_2018_C2[-1.0,-1000.0,100.0];

t3m_bkg_expo_twoGlobalTracker_2017_A1_norm[0.0,0.0,100000.0];
t3m_bkg_expo_twoGlobalTracker_2017_A2_norm[0.0,0.0,100000.0];
t3m_bkg_expo_twoGlobalTracker_2017_B1_norm[0.0,0.0,100000.0];
t3m_bkg_expo_twoGlobalTracker_2017_B2_norm[0.0,0.0,100000.0];
t3m_bkg_expo_twoGlobalTracker_2017_C1_norm[0.0,0.0,100000.0];
t3m_bkg_expo_twoGlobalTracker_2017_C2_norm[0.0,0.0,100000.0];

t3m_bkg_expo_twoGlobalTracker_2018_A1_norm[0.0,0.0,100000.0];
t3m_bkg_expo_twoGlobalTracker_2018_A2_norm[0.0,0.0,100000.0];
t3m_bkg_expo_twoGlobalTracker_2018_B1_norm[0.0,0.0,100000.0];
t3m_bkg_expo_twoGlobalTracker_2018_B2_norm[0.0,0.0,100000.0];
t3m_bkg_expo_twoGlobalTracker_2018_C1_norm[0.0,0.0,100000.0];
t3m_bkg_expo_twoGlobalTracker_2018_C2_norm[0.0,0.0,100000.0];

t3m_bkg_expo_twoGlobalTracker_2017_A1  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2017_A1);
t3m_bkg_expo_twoGlobalTracker_2017_A2  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2017_A2);
t3m_bkg_expo_twoGlobalTracker_2017_B1  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2017_B1);
t3m_bkg_expo_twoGlobalTracker_2017_B2  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2017_B2);
t3m_bkg_expo_twoGlobalTracker_2017_C1  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2017_C1);
t3m_bkg_expo_twoGlobalTracker_2017_C2  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2017_C2);


t3m_bkg_expo_twoGlobalTracker_2018_A1  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2018_A1);
t3m_bkg_expo_twoGlobalTracker_2018_A2  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2018_A2);
t3m_bkg_expo_twoGlobalTracker_2018_B1  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2018_B1);
t3m_bkg_expo_twoGlobalTracker_2018_B2  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2018_B2);
t3m_bkg_expo_twoGlobalTracker_2018_C1  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2018_C1);
t3m_bkg_expo_twoGlobalTracker_2018_C2  = Exponential(m3m, bkg_exp_slope_twoGlobalTracker_2018_C2);

sqrtS[13000., 13000., 13000.]
