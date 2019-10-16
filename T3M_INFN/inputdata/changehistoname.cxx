
void changehistoname(){

  TFile *_file0 = TFile::Open("LOCAL_COMBINED_threemu_default.root");

  TH1F *hdata = (TH1F *)_file0->Get("threemu_default_Cut_9_Nminus0_ThreeMuMass_Data");
  TH1F *hbkg = (TH1F *)_file0->Get("threemu_default_Cut_9_Nminus0_ThreeMuMass_Data");
  TH1F *hsig = (TH1F *)_file0->Get("threemu_default_Cut_9_Nminus0_ThreeMuMass_MC2");
  
  TFile *out = new TFile("input_histograms.root","RECREATE");


  hdata->Write("data_obs",TObject::kWriteDelete);
  hsig->Write("signal",TObject::kWriteDelete);
  hsig->Write("signal_up",TObject::kWriteDelete);
  hbkg->Write("background",TObject::kWriteDelete);
  hbkg->Write("background_up",TObject::kWriteDelete);
}
