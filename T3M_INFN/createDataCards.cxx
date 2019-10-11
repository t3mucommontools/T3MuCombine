#include <string>
#include <map>

using namespace RooFit;
using namespace RooStats ;


static const Int_t NCAT = 6;
Double_t MMIN = 1.64;
Double_t MMAX = 2.0;
//double signalScaler=1/10.;
double signalScaler=1;
double analysisLumi = 1.;   // 1/fb

void AddSigData(RooWorkspace*,  std::vector<string>);
void AddBkgData(RooWorkspace*,  std::vector<string>);
void SigModelFit(RooWorkspace*, std::vector<string>, RooPlot*frame[NCAT]);
void BkgModelFit(RooWorkspace*, std::vector<string>, RooFitResult** fitresults, bool sidebands, std::vector<string> cat_names, RooPlot*frame[NCAT]);
void MakeSigWS(RooWorkspace* w, const char* filename,  std::vector<string>);
void MakeBkgWS(RooWorkspace* w, const char* filename,  std::vector<string>);
void MakeDataCard(RooWorkspace* w, const char* fileBaseName, const char* fileBkgName,  std::vector<string> cat_names);


// void MakePlots(RooWorkspace*, );


void SetConstantParams(const RooArgSet* params);





void 
createDataCards(int signalsample = 0, Bool_t dobands = false)
{
  vector<string> cat_names; // reserved to handle categories
  cat_names.push_back("A1");
  cat_names.push_back("A2");
  cat_names.push_back("B1");
  cat_names.push_back("B2");
  cat_names.push_back("C1");
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
  RooPlot *frame[NCAT];

  AddSigData(w,cat_names);
  AddBkgData(w,cat_names);
  SigModelFit(w,cat_names, frame);
  MakeSigWS(w, fileBaseName, cat_names);
  BkgModelFit(w, cat_names, fitresults, doSideBands, cat_names, frame);
  MakeBkgWS(w, fileBkgName,cat_names);

  MakeDataCard(w, fileBaseName, fileBkgName,   cat_names);
  for(unsigned int category=0; category< NCAT; category++)
      {
      TString NameForSave; NameForSave=TString::Format("FinalMass_%s",cat_names.at(category).c_str());

      TCanvas c;
      c.cd();
      frame[category]->SetTitle(NameForSave);
      frame[category]->Draw();
      c.SaveAs(NameForSave+".png");
      TString filename("temp_workspace.root");
      w->writeToFile(filename);
  }
  cout<<" create end "<<endl;



  return;

}

void 
SigModelFit(RooWorkspace* w, std::vector<string> cat_names, RooPlot *frame[NCAT] ) {

  Int_t ncat = NCAT;
  RooDataHist* sigToFit[NCAT];  // create for one category so far
  RooAbsPdf* pdfSig[NCAT];
  //RooAbsPdf* pdfBkg[NCAT];
  RooFitResult* fitresults[NCAT];
  //
  RooDataSet* data[NCAT];
  RooPlot* plotbkg_fit[NCAT];
  RooAbsPdf* bkg_fitTmp_1par[NCAT];
  RooRealVar* m3m     = w->var("m3m");
  m3m->setUnit("GeV");
  m3m->setRange("SB1",1.64,1.72);
  m3m->setRange("SB2",1.82,2.0);
  m3m->setRange("fullRange",1.64,2.0);
  //

  Float_t minMassFit(MMIN),maxMassFit(MMAX); 


  for(unsigned int category=0; category< NCAT; category++)
    {
      
      frame[category] = ((RooRealVar*) w->var("m3m"))->frame();
     
      sigToFit[category]   = (RooDataHist*) w->data(TString::Format("Sig_%s",cat_names.at(category).c_str()));
      pdfSig[category]     = (RooAbsPdf*)  w->pdf("t3m_sig_shape"+TString::Format("_%s",cat_names.at(category).c_str()));
    
      pdfSig[category]->fitTo(*sigToFit[category],Range(minMassFit,maxMassFit));
      
      w->defineSet(TString::Format("SigPdfParam_%s",cat_names.at(category).c_str()), RooArgSet(
											       *w->var("sig_m0"+TString::Format("_%s",cat_names.at(category).c_str())),
											       *w->var("sig_sigma"+TString::Format("_%s",cat_names.at(category).c_str())),
											       *w->var("sig_alpha"+TString::Format("_%s",cat_names.at(category).c_str())),
											       *w->var("sig_n"+TString::Format("_%s",cat_names.at(category).c_str()))));
      SetConstantParams(w->set(TString::Format("SigPdfParam_%s",cat_names.at(category).c_str())));

      data[category]   = (RooDataSet*) w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str()));

       sigToFit[category]->plotOn(frame[category]);// bkg_fitTmp_1par->plotOn(frame);
       pdfSig[category]->plotOn(frame[category],LineColor(kRed));// data->plotOn(frame);

    }
}



void 
AddSigData(RooWorkspace* w, std::vector<string> cat_names) {

  Int_t ncat = NCAT;

  TFile *f = new TFile("./Analysed_3global_03oct/datacardT3MuAllCat.root","READ");
  TH1F *taumass[NCAT];

  for(unsigned int category=0; category< NCAT; category++){
      
    TString name = TString::Format("Sig_%s",cat_names.at(category).c_str());
    taumass[category] = (TH1F*)f->Get(TString::Format("signal%s",cat_names.at(category).c_str())); // debugging
    RooDataHist sighist("sighist","sighist",*w->var("m3m"),Import(*taumass[category]));
    
    w->import(sighist,Rename(name));
    
  }
  cout<<" AddSigData end "<<endl;
}


void AddBkgData(RooWorkspace* w, std::vector<string> cat_names) {

  Int_t ncat = NCAT;

  TFile *f = new TFile("./Analysed_3global_03oct/datacardT3MuAllCat.root","READ");
  TH1F *taumass[NCAT];


  for(unsigned int category=0; category< NCAT; category++)
    {
      TString name = TString::Format("Bkg_%s",cat_names.at(category).c_str());
      taumass[category] = (TH1F*)f->Get(TString::Format("background%s",cat_names.at(category).c_str())); // debugging
      RooDataHist bkghist("bkghist","bkghist",*w->var("m3m"),Import(*taumass[category]));
      
      w->import(bkghist,Rename(name));

  }
  cout<<" AddBkgData end "<<endl;
}



void 
BkgModelFit(RooWorkspace* w,  std::vector<string>, RooFitResult** fitresults, bool SideBands, std::vector<string> cat_names, RooPlot *frame[NCAT]){


  Int_t ncat = NCAT; // reserved for categories
  RooDataSet* data[NCAT];
  RooPlot* plotbkg_fit[NCAT];
  RooAbsPdf* bkg_fitTmp_1par[NCAT];
  RooAbsPdf* pdfBkg[NCAT];
 
  RooRealVar* m3m     = w->var("m3m");  
  m3m->setUnit("GeV");
  m3m->setRange("SB1",1.64,1.72);
  m3m->setRange("SB2",1.82,2.0);
  m3m->setRange("fullRange",1.64,2.0);
  TCut sidebands = TCut("(m3m < 1.72 && m3m > 1.64) || (m3m < 2.0 && m3m > 1.82)");
  cout<<" bkg fit "<<endl;
  for(unsigned int category=0; category< NCAT; category++)
    {
      data[category]   = (RooDataSet*) w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str()));

      bkg_fitTmp_1par[category] = new RooGenericPdf(TString::Format("bkg_fit_1par_%s",cat_names.at(category).c_str()), "exp(@1*@0 + @2)", 
                                                    RooArgList( *w->var("m3m"),
                                                                *w->var(TString::Format("bkg_exp_slope_%s",cat_names.at(category).c_str())),
                                                                *w->var(TString::Format("bkg_exp_offset_%s",cat_names.at(category).c_str()))));   // Generig BKG pdf for more careful description

      fitresults[category]=bkg_fitTmp_1par[category]->fitTo(*data[category],Strategy(1), Minos(kFALSE), Range("SB1,SB2"),SumW2Error(kTRUE), Save(kTRUE),RooFit::PrintEvalErrors(-1));
      
      fitresults[category]->Print();
      w->import(*bkg_fitTmp_1par[category]);

      Double_t Nratio(0.);
      Double_t Nentries(static_cast<Double_t>(data[category]->sumEntries()));
      Nratio=(static_cast<Double_t>((data[category]->reduce(sidebands)->sumEntries())))/(static_cast<Double_t>(Nentries));

      data[category]->plotOn(frame[category], CutRange("SB1,SB2"));
      bkg_fitTmp_1par[category]->plotOn(frame[category],
                                        Normalization(Nratio, RooAbsReal::Relative), 
                                        LineColor(kBlue),
                                        LineStyle(kDashed), 
                                        Range("fullRange"));
      //By default the model is drawn in same range as used for the fitting
      bkg_fitTmp_1par[category]->plotOn(frame[category],
                                        Normalization(Nratio, RooAbsReal::Relative), 
                                        LineColor(kBlue));
    }
}


void 
MakeSigWS(RooWorkspace* w, const char* fileBaseName,  std::vector<string> cat_names) {

  TString wsDir   = "workspaces/";
  Int_t ncat = NCAT; // reserved for categories

  RooWorkspace *wAll = new RooWorkspace("w_all","w_all");
  RooAbsPdf* SigPdf[NCAT];


  for(unsigned int category; category < NCAT; category++){

  //(1) Retrieve p.d.f.s

  SigPdf[category] = (RooAbsPdf*)  w->pdf("t3m_sig_shape"+TString::Format("_%s",cat_names.at(category).c_str()));
  wAll->import(*w->pdf("t3m_sig_shape"+TString::Format("_%s",cat_names.at(category).c_str())));
  wAll->import(*w->data(TString::Format("Sig_%s",cat_names.at(category).c_str())));

  //(2) factory of systematics
  //....



  }
  TString filename(wsDir+TString(fileBaseName)+".root");
  wAll->writeToFile(filename);
  cout << "Write signal workspace in: " << filename << " file" << endl;
  
  return;

}


void 
MakeBkgWS(RooWorkspace* w, const char* fileBaseName, std::vector<string> cat_names) {
  TString wsDir   = "workspaces/";
  Int_t ncat = NCAT;   // reserve for categories

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
  //  TString wsDir   = "../workspaces/";
  TString wsDir   = "workspaces/";

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
    outFile << Form("shapes data_obs  %s ",cat_names.at(c).c_str())  << wsDir+TString(fileBkgName)+".root " << Form("w_all:data_obs_%s",cat_names.at(c).c_str()) << endl;
    outFile << Form("shapes bkg %s ", cat_names.at(c).c_str())   << wsDir+TString(fileBkgName)+".root " << Form("w_all:bkg_fit_1par_%s",cat_names.at(c).c_str()) << endl;

    outFile << Form("shapes signal %s ", cat_names.at(c).c_str()) << wsDir+TString(fileBaseName)+".root " << Form("w_all:t3m_sig_shape_%s",cat_names.at(c).c_str()) << endl;

    outFile << "---------------" << endl;
    outFile << Form("bin            %s  ", cat_names.at(c).c_str()) << endl;
    outFile << "observation   "  <<  data[c]->sumEntries() << endl;
    outFile << "------------------------------" << endl;

    outFile << Form("bin                  %s          %s     ",cat_names.at(c).c_str(),cat_names.at(c).c_str())<<  endl;
    outFile << "process              signal     bkg     " << endl;
    outFile << "process              0          1      " << endl;
    outFile << "rate                "  << " " << signal[c]->sumEntries()*signalScaler << "    " << data[c]->sumEntries() << endl;
    outFile << "--------------------------------" << endl;


   
    //outFile << "lumi_13TeV       lnN  1.027      - " << endl;
    outFile << "lumi_13TeV        lnN  1.027     - " << endl;
    //outFile << "DsNorm_13TeV      lnN  1.033     - " << endl;
    outFile << "BRDToTau_13TeV    lnN  1.03      - " << endl;
    outFile << "BRDsPhiPi_13TeV   lnN  1.08      - " << endl;
    outFile << "BRBtoTau_13TeV    lnN  1.11      - " << endl;    
    outFile << "BRBtoD_13TeV      lnN  1.16      - " << endl;
    outFile << "fUnc_13TeV        lnN  1.11      - " << endl;
    outFile << "DpmScaling_13TeV  lnN  1.03      - " << endl;
    outFile << "BsScaling_13TeV   lnN  1.12      - " << endl;
    outFile << "DsNorm_13TeV      lnN  1.05      - " << endl;
    outFile << "UncTrigger_13TeV  lnN  1.12      - " << endl;
    outFile << "UncRatioAcc_13TeV lnN  1.01      - " << endl;
    outFile << "UncMuonEff_13TeV  lnN  1.015     - " << endl;
    outFile << "MuES_13TeV        lnN  1.007     - " << endl;
    outFile << "MuRes_13TeV       lnN  1.025     - " << endl;


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


