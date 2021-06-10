m3m[1.62,2.0];
sig_m0_A1[1.776, 1.775, 1.778];
sig_sigma_A1[0.010, 0.00, 0.05];
sig_alpha_A1[ 1, -5., 5.];
sig_n_A1[1, 0.0, 5.0];
sig_gaus_sigma_A1[0.021,0.01,0.05];
cb_fraction_A1[0.5,0,1];

t3m_sig_CBshape_A1_threeGlobal  = CBShape(m3m, sig_m0_A1, sig_sigma_A1, sig_alpha_A1, sig_n_A1);
t3m_sig_GSshape_A1_threeGlobal  = Gaussian(m3m,sig_m0_A1,sig_gaus_sigma_A1);


sig_m0_B1[1.776, 1.775, 1.778];
sig_sigma_B1[0.02, 0.00, 0.5];
sig_alpha_B1[ 1, -20., 20.];
sig_n_B1[2, 0.0, 5.0];
sig_gaus_sigma_B1[0.02,0.00,0.5];
cb_fraction_B1[0.5,0,1];

t3m_sig_CBshape_B1_threeGlobal  = CBShape(m3m, sig_m0_B1, sig_sigma_B1, sig_alpha_B1, sig_n_B1);
t3m_sig_GSshape_B1_threeGlobal  = Gaussian(m3m,sig_m0_B1,sig_gaus_sigma_B1);


sig_m0_C1[1.776, 1.775, 1.778];
sig_sigma_C1[0.042, 0.01, 0.05];
sig_alpha_C1[ 1, -20., 20.];
sig_n_C1[2, 0.0, 5.0];
sig_gaus_sigma_C1[0.01,0.0,0.05];
cb_fraction_C1[0.2,0,1];

t3m_sig_CBshape_C1_threeGlobal  = CBShape(m3m, sig_m0_C1, sig_sigma_C1, sig_alpha_C1, sig_n_C1);
t3m_sig_GSshape_C1_threeGlobal  = Gaussian(m3m,sig_m0_C1,sig_gaus_sigma_C1);


sig_m0_A2[1.776, 1.775, 1.778];
sig_sigma_A2[0.01, 0.0, 0.05];
sig_alpha_A2[ 1, -20., 20.];
sig_n_A2[2, 0.0, 5.0];
sig_gaus_sigma_A2[0.01,0.0,0.05];
cb_fraction_A2[0.5,0,1];

t3m_sig_CBshape_A2_threeGlobal  = CBShape(m3m, sig_m0_A2, sig_sigma_A2, sig_alpha_A2, sig_n_A2);
t3m_sig_GSshape_A2_threeGlobal  = Gaussian(m3m,sig_m0_A2,sig_gaus_sigma_A2);


sig_m0_B2[1.776, 1.775, 1.778];
sig_sigma_B2[0.02, 0.0, 0.05];
sig_alpha_B2[ 1, -20., 20.];
sig_n_B2[2, 0.0, 5.0];
sig_gaus_sigma_B2[0.02,0.0,0.05];
cb_fraction_B2[0.5,0,1];

t3m_sig_CBshape_B2_threeGlobal  = CBShape(m3m, sig_m0_B2, sig_sigma_B2, sig_alpha_B2, sig_n_B2);
t3m_sig_GSshape_B2_threeGlobal  = Gaussian(m3m,sig_m0_B2,sig_gaus_sigma_B2);


sig_m0_C2[1.776, 1.775, 1.778];
sig_sigma_C2[0.02, 0.0, 0.05];
sig_alpha_C2[ 1, -20., 20.];
sig_n_C2[2, 0.0, 5.0];
sig_gaus_sigma_C2[0.02,0.0,0.05];
cb_fraction_C2[0.5,0,1];

t3m_sig_CBshape_C2_threeGlobal  = CBShape(m3m, sig_m0_C2, sig_sigma_C2, sig_alpha_C2, sig_n_C2);
t3m_sig_GSshape_C2_threeGlobal  = Gaussian(m3m,sig_m0_C2,sig_gaus_sigma_C2);

sig_m0_A3[1.776, 1.775, 1.778];
sig_sigma_A3[0.01, 0.0, 0.05];
sig_alpha_A3[ 1, -20., 20.];
sig_n_A3[2, 0.0, 5.0];
sig_gaus_sigma_A3[0.01,0.0,0.05];
cb_fraction_A3[0.5,0,1];

t3m_sig_CBshape_A3_threeGlobal  = CBShape(m3m, sig_m0_A3, sig_sigma_A3, sig_alpha_A3, sig_n_A3);
t3m_sig_GSshape_A3_threeGlobal  = Gaussian(m3m,sig_m0_A3,sig_gaus_sigma_A3);


sig_m0_B3[1.776, 1.775, 1.778];
sig_sigma_B3[0.02, 0.0, 0.05];
sig_alpha_B3[ 1, -20., 20.];
sig_n_B3[2, 0.0, 5.0];
sig_gaus_sigma_B3[0.02,0.0,0.05];
cb_fraction_B3[0.5,0,1];

t3m_sig_CBshape_B3_threeGlobal  = CBShape(m3m, sig_m0_B3, sig_sigma_B3, sig_alpha_B3, sig_n_B3);
t3m_sig_GSshape_B3_threeGlobal  = Gaussian(m3m,sig_m0_B3,sig_gaus_sigma_B3);


sig_m0_C3[1.776, 1.775, 1.778];
sig_sigma_C3[0.02, 0.0, 0.05];
sig_alpha_C3[ 1, -20., 20.];
sig_n_C3[2, 0.0, 5.0];
sig_gaus_sigma_C3[0.02,0.0,0.05];
cb_fraction_C3[0.5,0,1];

t3m_sig_CBshape_C3_threeGlobal  = CBShape(m3m, sig_m0_C3, sig_sigma_C3, sig_alpha_C3, sig_n_C3);
t3m_sig_GSshape_C3_threeGlobal  = Gaussian(m3m,sig_m0_C3,sig_gaus_sigma_C3);

bkg_exp_slope_A1[-1.0,-6.0, 1.0];
bkg_exp_slope_A2[-1.0,-6.0, 1.0];
bkg_exp_slope_A3[-1.0,-6.0, 1.0];
bkg_exp_slope_B1[-1.0,-10.0,-0.0];
bkg_exp_slope_B2[-1.0,-6.0,-0.0];
bkg_exp_slope_B3[-1.0,-6.0,-0.0];
bkg_exp_slope_C1[-1.0,-6.0,-0.0];
bkg_exp_slope_C2[-1.0,-6.0,-0.0];
bkg_exp_slope_C3[-1.0,-6.0,-0.0];


bkg_exp_offset_A1[0.0,-20.0,20.0];
bkg_exp_offset_A2[0.0,-20.0,20.0];
bkg_exp_offset_A3[0.0,-20.0,20.0];
bkg_exp_offset_B1[0.0,-20.0,20.0];
bkg_exp_offset_B2[0.0,-20.0,20.0];
bkg_exp_offset_B3[0.0,-20.0,20.0];
bkg_exp_offset_C1[0.0,-20.0,20.0];
bkg_exp_offset_C2[0.0,-20.0,20.0];
bkg_exp_offset_C3[0.0,-20.0,20.0];


bkg_powerlaw_slope_A1[-1.0,-5.0,1.0];
bkg_powerlaw_slope_A2[-1.0,-5.0,1.0];
bkg_powerlaw_slope_A3[-1.0,-5.0,1.0];

bkg_powerlaw_slope_B1[-1.0,-5.0,1.0];
bkg_powerlaw_slope_B2[-1.0,-5.0,1.0];
bkg_powerlaw_slope_B3[-1.0,-5.0,1.0];

bkg_powerlaw_slope_C1[-1.0,-5.0,1.0];
bkg_powerlaw_slope_C2[-1.0,-5.0,1.0];
bkg_powerlaw_slope_C3[-1.0,-5.0,1.0];


bkg_exp_shape_A1 = RooExponential(m3m,bkg_exp_slope_A1, bkg_exp_offset_A1);
bkg_exp_shape_A2 = RooExponential(m3m,bkg_exp_slope_A2, bkg_exp_offset_A2);
bkg_exp_shape_A3 = RooExponential(m3m,bkg_exp_slope_A3, bkg_exp_offset_A3);
bkg_exp_shape_B1 = RooExponential(m3m,bkg_exp_slope_B1, bkg_exp_offset_B1);
bkg_exp_shape_B2 = RooExponential(m3m,bkg_exp_slope_B2, bkg_exp_offset_B2);
bkg_exp_shape_B3 = RooExponential(m3m,bkg_exp_slope_B3, bkg_exp_offset_B3);
bkg_exp_shape_C1 = RooExponential(m3m,bkg_exp_slope_C1, bkg_exp_offset_C1);
bkg_exp_shape_C2 = RooExponential(m3m,bkg_exp_slope_C2, bkg_exp_offset_C2);
bkg_exp_shape_C3 = RooExponential(m3m,bkg_exp_slope_C3, bkg_exp_offset_C3);


//bkg_exp_slope_A1[-2.0,-6.0,-0.001];
//bkg_exp_slope_A2[-2.0,-6.0,-0.001];
//bkg_exp_slope_B1[-3.0,-6.0,-0.001];
//bkg_exp_slope_B2[-2.0,-6.0,-0.001];
//bkg_exp_slope_C1[-2.0,-6.0,-0.001];
//bkg_exp_slope_C2[-2.0,-6.0,-0.001];
//
//bkg_exp_offset_A1[0.0,0.0,5.0];
//bkg_exp_offset_A2[0.0,0.0,5.0];
//bkg_exp_offset_B1[0.0,0.0,5.0];
//bkg_exp_offset_B2[0.0,0.0,5.0];
//bkg_exp_offset_C1[0.0,0.0,5.0];
//bkg_exp_offset_C2[0.0,0.0,5.0];

sqrtS[13000., 13000., 13000.]

//bkg_exp_offset[0.0,-10.0,10.0];
//bkg_exp_shape  = RooExponential(m3m,bkg_exp_slope);
