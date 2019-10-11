m3m[1.64,2.0];
sig_m0_A1[1.777, 1.64, 2.0];
sig_sigma_A1[0.02, 0.0, 0.05];
sig_alpha_A1[ 1, -20., 20.]; 
sig_n_A1[2, 0.0, 5.0]; 
t3m_sig_shape_A1  = CBShape(m3m, sig_m0_A1, sig_sigma_A1, sig_alpha_A1, sig_n_A1);


m3m[1.64,2.0];
sig_m0_A2[1.777, 1.64, 2.0];
sig_sigma_A2[0.02, 0.0, 0.05];
sig_alpha_A2[ 1, -20., 20.];
sig_n_A2[2, 0.0, 5.0];
t3m_sig_shape_A2  = CBShape(m3m, sig_m0_A2, sig_sigma_A2, sig_alpha_A2, sig_n_A2);

m3m[1.64,2.0];
sig_m0_B1[1.777, 1.64, 2.0];
sig_sigma_B1[0.02, 0.0, 0.05];
sig_alpha_B1[ 1, -20., 20.]; 
sig_n_B1[2, 0.0, 5.0]; 
t3m_sig_shape_B1  = CBShape(m3m, sig_m0_B1, sig_sigma_B1, sig_alpha_B1, sig_n_B1);

m3m[1.64,2.0];
sig_m0_B2[1.777, 1.64, 2.0];
sig_sigma_B2[0.02, 0.0, 0.05];
sig_alpha_B2[ 1, -20., 20.];
sig_n_B2[2, 0.0, 5.0];
t3m_sig_shape_B2  = CBShape(m3m, sig_m0_B2, sig_sigma_B2, sig_alpha_B2, sig_n_B2);

m3m[1.64,2.0];
sig_m0_C1[1.777, 1.64, 2.0];
sig_sigma_C1[0.02, 0.0, 0.05];
sig_alpha_C1[ 1, -20., 20.]; 
sig_n_C1[2, 0.0, 5.0]; 
t3m_sig_shape_C1  = CBShape(m3m, sig_m0_C1, sig_sigma_C1, sig_alpha_C1, sig_n_C1);

m3m[1.64,2.0];
sig_m0_C2[1.777, 1.64, 2.0];
sig_sigma_C2[0.02, 0.0, 0.05];
sig_alpha_C2[ 1, -20., 20.];
sig_n_C2[2, 0.0, 5.0];
t3m_sig_shape_C2  = CBShape(m3m, sig_m0_C2, sig_sigma_C2, sig_alpha_C2, sig_n_C2);

m3m[1.64,2.0];
bkg_m0_A1[1.777, 1.64, 2.0];
bkg_sigma_A1[0.02, 0.0, 0.05];
bkg_alpha_A1[ 1, -20., 20.];
bkg_n_A1[2, 0.0, 5.0];
t3m_bkg_shape_A1= CBShape(m3m, bkg_m0_A1, bkg_sigma_A1, bkg_alpha_A1, bkg_n_A1);



bkg_exp_slope_A1[0.5,-2.,5.0];
bkg_exp_slope_A2[0.0,-1.,1.0];
bkg_exp_slope_B1[0.5,-2.,5.0];
bkg_exp_slope_B2[0.0,-1.,1.0];
bkg_exp_slope_C1[0.5,-2.,5.0];
bkg_exp_slope_C2[0.0,-1,1.0];

bkg_exp_offset_A1[0.0,-10.0,10.0];
bkg_exp_offset_A2[0.0,-10.0,10.0];
bkg_exp_offset_B1[0.0,-10.0,10.0];
bkg_exp_offset_B2[0.0,-10.0,10.0];
bkg_exp_offset_C1[0.0,-10.0,10.0];
bkg_exp_offset_C2[0.0,-10.0,10.0];

bkg_exp_shape_A1 = RooExponential(m3m,bkg_exp_slope_A1, bkg_exp_offset_A1);
bkg_exp_shape_A2 = RooExponential(m3m,bkg_exp_slope_A2, bkg_exp_offset_A2);
bkg_exp_shape_B1 = RooExponential(m3m,bkg_exp_slope_B1, bkg_exp_offset_B1);
bkg_exp_shape_B2 = RooExponential(m3m,bkg_exp_slope_B2, bkg_exp_offset_B2);
bkg_exp_shape_C1 = RooExponential(m3m,bkg_exp_slope_C1, bkg_exp_offset_C1);
bkg_exp_shape_C2 = RooExponential(m3m,bkg_exp_slope_C2, bkg_exp_offset_C2);


sqrtS[13000., 13000., 13000.]
