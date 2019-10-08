#include <string>
#include <map>

using namespace RooFit;
using namespace RooStats ;


static const Int_t NCAT = 6;
Double_t MMIN = 1.65;
Double_t MMAX = 2.0;
double signalScaler=1;///10.;
double analysisLumi = 1.;   // 1/fb

void AddSigData(TString, RooWorkspace*,  std::vector<string>);
void AddBkgData(TString, RooWorkspace*,  std::vector<string>);
void SigModelFit(RooWorkspace*, std::vector<string>);
void BkgModelFit(RooWorkspace*, std::vector<string>, RooFitResult** fitresults, bool sidebands, std::vector<string> cat_names);
void MakeSigWS(RooWorkspace* w, const char* filename,  std::vector<string>);
void MakeBkgWS(RooWorkspace* w, const char* filename,  std::vector<string>);
void MakeDataCard(RooWorkspace* w, const char* fileBaseName, const char* fileBkgName,  std::vector<string> cat_names);
void MakeCombinedDataCard(RooWorkspace* w, const char* fileBaseName, const char* fileBkgName,  std::vector<string> cat_names);
void MakePlots(RooWorkspace* w,   std::vector<string> cat_names);


// void MakePlots(RooWorkspace*, );


void SetConstantParams(const RooArgSet* params);





void 
createDataCards(TString inputfile, int signalsample = 0, Bool_t dobands = false)
{
  vector<string> cat_names; // reserved to handle categories
  cat_names.push_back("A1");
  cat_names.push_back("B1");
  cat_names.push_back("C1");

  cat_names.push_back("A2");
  cat_names.push_back("B2");
  cat_names.push_back("C2");


  TString signalname("T3MSignal");
  TString bkgname("T3MBkg");


  TString fileBaseName("CMS_"+signalname+"_13TeV");
  TString fileBkgName("CMS_"+bkgname+"_13TeV");


  TString card_name("model_card.rs");
  HLFactory hlf("HLFactory", card_name, false);
  RooWorkspace* w = hlf.GetWs();
  RooFitResult* fitresults[NCAT];
  w->var("m3m")->setMin(MMIN);
  w->var("m3m")->setMax(MMAX);

  w->Print();
  bool doSideBands = true;
  AddSigData(inputfile,w,cat_names);
  AddBkgData(inputfile,w,cat_names);
  SigModelFit(w,cat_names);

  MakeSigWS(w, fileBaseName, cat_names);
  BkgModelFit(w, cat_names, fitresults, doSideBands,cat_names);
  MakeBkgWS(w, fileBkgName,cat_names);
  MakeDataCard(w, fileBaseName, fileBkgName,   cat_names);

  TString filename("temp_workspace.root");
  w->writeToFile(filename);
  MakePlots(w,cat_names);




  return;

}

void 
SigModelFit(RooWorkspace* w, std::vector<string> cat_names) {

  Int_t ncat = NCAT;
  RooDataHist* sigToFit[NCAT];  
  RooAbsPdf* pdfSigCB[NCAT];
  RooAbsPdf* pdfSigGS[NCAT];
  RooAddPdf* SignalModel[NCAT];

  Float_t minMassFit(MMIN),maxMassFit(MMAX); 


  for(unsigned int category=0; category< NCAT; category++)
    {

      std::cout<<"category  "<< cat_names.at(category).c_str() << std::endl;
      sigToFit[category]     =  (RooDataHist*) w->data(TString::Format("Sig_%s",cat_names.at(category).c_str()));
      pdfSigCB[category]     =  (RooAbsPdf*)   w->pdf("t3m_sig_CBshape"+TString::Format("_%s",cat_names.at(category).c_str()));
      pdfSigGS[category]     =  (RooAbsPdf*)   w->pdf("t3m_sig_GSshape"+TString::Format("_%s",cat_names.at(category).c_str()));


      RooAbsReal* CBFraction = new RooRealVar(TString::Format("cb_fraction_%s",cat_names.at(category).c_str()),"",1,0,100);    
      RooAbsReal* GSFraction = new RooRealVar(TString::Format("gs_fraction_%s",cat_names.at(category).c_str()),"",1,0,100);

      SignalModel[category] = new RooAddPdf(TString::Format("SignalModel_%s",cat_names.at(category).c_str()),"g+a",RooArgList(*pdfSigCB[category],*pdfSigGS[category]),*CBFraction);
      SignalModel[category]->fitTo(*sigToFit[category],Range(minMassFit,maxMassFit));
      

      w->defineSet(TString::Format("SigPdfParam_%s",cat_names.at(category).c_str()), RooArgSet(
      											       *w->var("sig_m0"+TString::Format("_%s",cat_names.at(category).c_str())),
											       *w->var("sig_sigma"+TString::Format("_%s",cat_names.at(category).c_str())),
											       *w->var("sig_gaus_sigma"+TString::Format("%s",cat_names.at(category).c_str())),
      											       *w->var("sig_alpha"+TString::Format("_%s",cat_names.at(category).c_str())),
      											       *w->var("sig_n"+TString::Format("_%s",cat_names.at(category).c_str()))));
     
      SetConstantParams(w->set(TString::Format("SigPdfParam_%s",cat_names.at(category).c_str())));
      w->import(*SignalModel[category]);
    }
}

void 
MakePlots(RooWorkspace* w,   std::vector<string> cat_names){

  Int_t ncat = NCAT;
  RooDataHist* signalAll[NCAT]; 
  RooDataSet* dataAll[NCAT];
  RooAbsPdf* sigpdf[NCAT]; 
  RooAbsPdf* bkgpdf[NCAT]; 

  for(unsigned int category=0; category< NCAT; category++){
    signalAll[category]=  (RooDataHist*) w->data(TString::Format("Sig_%s",cat_names.at(category).c_str()));
    dataAll[category]=  (RooDataSet*) w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str()));
    sigpdf[category] =(RooAbsPdf*)w->pdf("SignalModel"+TString::Format("_%s",cat_names.at(category).c_str()));
    bkgpdf[category] =(RooAbsPdf*)w->pdf(TString::Format("bkg_fit_1par_%s",cat_names.at(category).c_str()));
  }

  RooRealVar* m3m     = w->var("m3m");  

  m3m->setUnit("GeV");
  m3m->setRange("SB1",1.65,1.73);
  m3m->setRange("SB2",1.81,2.0);
  m3m->setRange("fullRange",1.65,2.0);


  TLatex *text = new TLatex();
  text->SetNDC();
  text->SetTextSize(0.04);


  RooPlot* plot[NCAT];
  for(unsigned int category=0; category< NCAT; category++){
    plot[category] = m3m->frame();
    signalAll[category]->plotOn( plot[category],RooFit::MarkerColor(kCyan+2),RooFit::MarkerStyle(6),RooFit::MarkerSize(0.75));
    sigpdf[category]->plotOn(plot[category], RooFit::LineColor(kCyan+2),RooFit::LineWidth(2.1));
    dataAll[category]->plotOn(plot[category],RooFit::MarkerColor(kGray+3),RooFit::MarkerStyle(21),RooFit::MarkerSize(0.75));
    bkgpdf[category]->plotOn(plot[category],Range("fullRange"),RooFit::LineColor(kGray+3),RooFit::LineWidth(2.1));
    plot[category]->SetTitle(TString::Format("Category %s",cat_names.at(category).c_str()));     
    plot[category]->SetMinimum(0.01);
    plot[category]->SetMaximum(1.40*plot[category]->GetMaximum());
    plot[category]->GetXaxis()->SetTitle("m_{3mu} [GeV]");
    
    TCanvas* ctmp_sig = new TCanvas(TString::Format("Category %s",cat_names.at(category).c_str()),"Categories",0,0,700,500);
    ctmp_sig->SetFrameLineWidth(3);
    ctmp_sig->SetTickx();
    ctmp_sig->SetTicky();
    plot[category]->Draw();
    plot[category]->Print();
    plot[category]->Draw("SAME");
    TLegend *legmc = new TLegend(0.12,0.70,0.43,0.86);
    
    legmc->AddEntry(plot[category]->getObject(0),"MC Signal (B=10-e8)","LPE");
    legmc->AddEntry(plot[category]->getObject(1),"Signal Model","L");
    legmc->AddEntry(plot[category]->getObject(2),"Data","LPE");
    legmc->AddEntry(plot[category]->getObject(3),"Data Model","L");
    
    legmc->SetBorderSize(0);
    legmc->SetFillStyle(0);
    legmc->SetTextSize(0.029);
    
    legmc->Draw();  
    ctmp_sig->SaveAs("plots/"+TString::Format("Category_%s",cat_names.at(category).c_str())+".png");
  }
}



void 
AddSigData(TString file, RooWorkspace* w, std::vector<string> cat_names) {

  TFile *f = new TFile(file,"READ");
  TH1F *taumass[NCAT];

  for(unsigned int category=0; category< NCAT; category++){
    TString name = TString::Format("Sig_%s",cat_names.at(category).c_str());
    taumass[category] = (TH1F*)f->Get(TString::Format("signal%s",cat_names.at(category).c_str()));
    RooDataHist sighist("sighist","sighist",*w->var("m3m"),Import(*taumass[category]));
    w->import(sighist,Rename(name));
  }
  f->Close();
}


void 
AddBkgData(TString file,RooWorkspace* w, std::vector<string> cat_names) {

  Int_t ncat = NCAT;

  TFile *f = new TFile(file,"READ");
  TH1F *taumass[NCAT];
  for(unsigned int category=0; category< NCAT; category++)
    {
      TString name = TString::Format("Bkg_%s",cat_names.at(category).c_str());
      taumass[category] = (TH1F*)f->Get(TString::Format("background%s",cat_names.at(category).c_str())); 
      RooDataHist bkghist("bkghist","bkghist",*w->var("m3m"),Import(*taumass[category]));
      w->import(bkghist,Rename(name));
    }
  f->Close();
}



void 
BkgModelFit(RooWorkspace* w,  std::vector<string>, RooFitResult** fitresults, bool SideBands, std::vector<string> cat_names){


  Int_t ncat = NCAT; // reserved for categories
  RooDataSet* data[NCAT];
  RooPlot* plotbkg_fit[NCAT];
  RooAbsPdf* bkg_fitTmp_1par[NCAT];
 
  RooRealVar* m3m     = w->var("m3m");  


  m3m->setUnit("GeV");
  m3m->setRange("SB1",1.65,1.73);
  m3m->setRange("SB2",1.81,2.0);
  m3m->setRange("fullRange",1.65,2.0);
  
  for(unsigned int category=0; category< NCAT; category++)
    {
      data[category]   = (RooDataSet*) w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str()));
      bkg_fitTmp_1par[category] = new RooGenericPdf(TString::Format("bkg_fit_1par_%s",cat_names.at(category).c_str()), "exp(@1*@0)", RooArgList(*w->var("m3m"), *w->var(TString::Format("bkg_exp_slope_%s",cat_names.at(category).c_str()))));   // Generig BKG pdf for more careful description
      fitresults[category]=bkg_fitTmp_1par[category]->fitTo(*data[category], Strategy(1), Minos(kFALSE), Range("SB1,SB2"),SumW2Error(kTRUE), Save(kTRUE),RooFit::PrintEvalErrors(-1));
      
      w->import(*bkg_fitTmp_1par[category]);
    }
}


void 
MakeSigWS(RooWorkspace* w, const char* fileBaseName,  std::vector<string> cat_names) {

  TString wsDir   = "workspaces/";
  RooWorkspace *wAll = new RooWorkspace("w_all","w_all");
  RooAbsPdf* SigPdf[NCAT];
  cout << "-----------------------------------Write signal workspace in: " <<std::endl;

  for(unsigned int category; category < NCAT; category++){

  //(1) Retrieve p.d.f.s

    //  SigPdf[category] = (RooAbsPdf*)  w->pdf("t3m_sig_shape"+TString::Format("_%s",cat_names.at(category).c_str()));
    //  wAll->import(*w->pdf("t3m_sig_CBshape"+TString::Format("_%s",cat_names.at(category).c_str())));
    //  wAll->import(*w->pdf("t3m_sig_GSshape"+TString::Format("_%s",cat_names.at(category).c_str())));
  wAll->import(*w->pdf("SignalModel"+TString::Format("_%s",cat_names.at(category).c_str())));
  wAll->import(*w->data(TString::Format("Sig_%s",cat_names.at(category).c_str())));

  //(2) factory of systematics
  //....



  }
  TString filename(wsDir+TString(fileBaseName)+".root");
  wAll->writeToFile(filename);
  cout << "-----------------------------------Write signal workspace in: " << filename << " file" << endl;
  
  return;

}


void 
MakeBkgWS(RooWorkspace* w, const char* fileBaseName, std::vector<string> cat_names) {
  TString wsDir   = "workspaces/";

  RooWorkspace *wAll = new RooWorkspace("w_all","w_all");
  RooDataSet* data[NCAT];
  RooExtendPdf* bkg_fitPdf[NCAT];
 
  for(unsigned int category=0; category < NCAT; category++){
    data[category] = (RooDataSet*) w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str()));
    wAll->import(*data[category],Rename(TString::Format("data_obs_%s",cat_names.at(category).c_str())));
    wAll->import(*w->pdf(TString::Format("bkg_fit_1par_%s",cat_names.at(category).c_str())));
    wAll->import(*w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str())));
  }
  TString filename(wsDir+TString(fileBaseName)+".root");
  wAll->writeToFile(filename);

  return;
}





void MakeDataCard(RooWorkspace* w, const char* fileBaseName, const char* fileBkgName,  std::vector<string> cat_names) {

  TString cardDir = "datacards/";
  Int_t ncat = NCAT;
  TString wsDir   = "../workspaces/";

  RooDataSet* data[NCAT];
  RooDataSet* signal[NCAT];

  for (int c = 0; c < ncat; ++c) {
    data[c]  = (RooDataSet *) w->data(Form("Bkg_%s",cat_names.at(c).c_str()));  //  meaningless for now
    signal[c] = (RooDataSet*) w->data(Form("Sig_%s",cat_names.at(c).c_str()));
    TString filename(cardDir+TString(fileBaseName)+Form("_%s",cat_names.at(c).c_str() ) +".txt");
    ofstream outFile(filename);
  
  
    outFile << "# HF Tau to three mu" << endl;
    outFile << "imax 1" << endl;
    outFile << "jmax 1" << endl;
    outFile << "kmax *" << endl;
    outFile << "---------------" << endl;


    // outFile << Form("shapes data_obs  %s ",cat_names.at(c).c_str())<< wsDir+TString(fileBkgName)+".root " << Form("w_all:bkg_fit_1par_%s",cat_names.at(c).c_str()) << endl;
    // outFile << Form("shapes bkg %s ", cat_names.at(c).c_str())  << wsDir+TString(fileBkgName)+".root " << Form("w_all:data_obs_%s",cat_names.at(c).c_str()) << endl;


    outFile << Form("shapes data_obs  %s ",cat_names.at(c).c_str())  << wsDir+TString(fileBkgName)+".root " << Form("w_all:data_obs_%s",cat_names.at(c).c_str()) << endl;
    outFile << Form("shapes bkg %s ", cat_names.at(c).c_str())   << wsDir+TString(fileBkgName)+".root " << Form("w_all:bkg_fit_1par_%s",cat_names.at(c).c_str()) << endl;

    outFile << Form("shapes signal %s ", cat_names.at(c).c_str()) << wsDir+TString(fileBaseName)+".root " << Form("w_all:SignalModel_%s",cat_names.at(c).c_str()) << endl;

    outFile << "---------------" << endl;
    outFile << Form("bin            %s  ", cat_names.at(c).c_str()) << endl;
    outFile << "observation   "  <<  data[c]->sumEntries() << endl;
    outFile << "------------------------------" << endl;

    outFile << Form("bin               %s        %s     ",cat_names.at(c).c_str(),cat_names.at(c).c_str())<<  endl;
    outFile << "process              signal     bkg     " << endl;
    outFile << "process                0          1      " << endl;
    outFile << "rate                "  << " " << signal[c]->sumEntries()*signalScaler << "    " << 1 << endl;
    outFile << "--------------------------------" << endl;

   
    outFile << "lumi_13TeV       lnN  1.027      - " << endl;

    outFile.close();
  
    cout << "Write data card in: " << filename << " file" << endl;
  }
  return;
}





void 
SetConstantParams(const RooArgSet* params) {

  TIterator* iter(params->createIterator());
  for (TObject *a = iter->Next(); a != 0; a = iter->Next()) {
    RooRealVar *rrv = dynamic_cast<RooRealVar *>(a);
    if (rrv) { rrv->setConstant(true); std::cout << " " << rrv->GetName(); }
  }  

}


