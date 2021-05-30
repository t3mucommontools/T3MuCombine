
void prepare_hsit(){

  TFile *_file0 = TFile::Open("LOCAL_COMBINED_signalselector_default_LumiScaled.root");

  TH1F *hdataA1 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitA1Data");
  TH1F *hbkgA1 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitA1Data");
  TH1F *hsigA1 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitA1MC2");
  TH1F *hsigA1_3 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitA1MC3");
  TH1F *hsigA1_4 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitA1MC4");

  TH1F *hdataB1 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitB1Data");
  TH1F *hbkgB1 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitB1Data");
  TH1F *hsigB1 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitB1MC2");
  TH1F *hsigB1_3 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitB1MC3");
  TH1F *hsigB1_4 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitB1MC4");

  TH1F *hdataC1 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitC1Data");
  TH1F *hbkgC1 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitC1Data");
  TH1F *hsigC1 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitC1MC2");
  TH1F *hsigC1_3 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitC1MC3");
  TH1F *hsigC1_4 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitC1MC4");



  TH1F *hdataA2 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitA2Data");
  TH1F *hbkgA2 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitA2Data");
  TH1F *hsigA2 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitA2MC2");
  TH1F *hsigA2_3 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitA2MC3");
  TH1F *hsigA2_4 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitA2MC4");

  TH1F *hdataB2 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitB2Data");
  TH1F *hbkgB2 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitB2Data");
  TH1F *hsigB2 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitB2MC2");
  TH1F *hsigB2_3 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitB2MC3");
  TH1F *hsigB2_4 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitB2MC4");

  TH1F *hdataC2 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitC2Data");
  TH1F *hbkgC2 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitC2Data");
  TH1F *hsigC2 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitC2MC2");
  TH1F *hsigC2_3 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitC2MC3");
  TH1F *hsigC2_4 = (TH1F *)_file0->Get("signalselector_default_TauMassRefitC2MC4");
  
  TFile *out = new TFile("input_histograms.root","RECREATE");
  
  hsigA1->Add(hsigA1_3);
  hsigA1->Add(hsigA1_4);

  hsigB1->Add(hsigB1_3);
  hsigB1->Add(hsigB1_4);

  hsigC1->Add(hsigC1_3);
  hsigC1->Add(hsigC1_4);

  hsigA2->Add(hsigA2_3);
  hsigA2->Add(hsigA2_4);

  hsigB2->Add(hsigB2_3);
  hsigB2->Add(hsigB2_4);

  hsigC2->Add(hsigC2_3);
  hsigC2->Add(hsigC2_4);

  hdataA1->Write("data_obsA1",TObject::kWriteDelete);
  hsigA1->Write("signalA1",TObject::kWriteDelete);
  hbkgA1->Write("backgroundA1",TObject::kWriteDelete);
  

  hdataB1->Write("data_obsB1",TObject::kWriteDelete);
  hsigB1->Write("signalB1",TObject::kWriteDelete);
  hbkgB1->Write("backgroundB1",TObject::kWriteDelete);
  

  hdataC1->Write("data_obsB1",TObject::kWriteDelete);
  hsigC1->Write("signalC1",TObject::kWriteDelete);
  hbkgC1->Write("backgroundC1",TObject::kWriteDelete);



  hdataA2->Write("data_obsA2",TObject::kWriteDelete);
  hsigA2->Write("signalA2",TObject::kWriteDelete);
  hbkgA2->Write("backgroundA2",TObject::kWriteDelete);
  

  hdataB2->Write("data_obsB2",TObject::kWriteDelete);
  hsigB2->Write("signalB2",TObject::kWriteDelete);
  hbkgB2->Write("backgroundB2",TObject::kWriteDelete);
  

  hdataC2->Write("data_obsC2",TObject::kWriteDelete);
  hsigC2->Write("signalC2",TObject::kWriteDelete);
  hbkgC2->Write("backgroundC2",TObject::kWriteDelete);


}
