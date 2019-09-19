#include <string>
#include <map>

using namespace RooFit;
using namespace RooStats ;


static const Int_t NCAT = 6;
Double_t MMIN = 1.65;
Double_t MMAX = 1.9;
double signalScaler=1;      // meaningless scale so far
double analysisLumi = 1.;   // 1/fb  

void AddSigData(RooWorkspace*,  std::vector<string>);
void AddBkgData(RooWorkspace*,  std::vector<string>);
void SigModelFit(RooWorkspace*, std::vector<string>);
void BkgModelFit(RooWorkspace*, std::vector<string>, RooFitResult* fitresults);
void MakeSigWS(RooWorkspace* w, const char* filename,  std::vector<string>);
void MakeBkgWS(RooWorkspace* w, const char* filename,  std::vector<string>);
void MakeDataCard(RooWorkspace* w, const char* fileBaseName, const char* fileBkgName,  std::vector<string> cat_names);


// void MakePlots(RooWorkspace*, );  // to be done later


void SetConstantParams(const RooArgSet* params);





void 
createDataCards(int signalsample = 0, Bool_t dobands = false)
{
  vector<string> cat_names; // reserved to handle categories

  TString signalname("T3MSignal");
  TString bkgname("T3MBkg");


  TString fileBaseName("CMS_"+signalname+"_13TeV");
  TString fileBkgName("CMS_"+bkgname+"_13TeV");


  TString card_name("model_card.rs");
  HLFactory hlf("HLFactory", card_name, false);
  RooWorkspace* w = hlf.GetWs();
  RooFitResult* fitresults;
  w->var("m3m")->setMin(MMIN);
  w->var("m3m")->setMax(MMAX);

  w->Print();

  AddSigData(w,cat_names);
  AddBkgData(w,cat_names);
  SigModelFit(w,cat_names);
  MakeSigWS(w, fileBaseName, cat_names);
  BkgModelFit(w, cat_names, fitresults);
  MakeBkgWS(w, fileBkgName,cat_names);


  MakeDataCard(w, fileBaseName, fileBkgName,   cat_names);

  TString filename("testworkspace.root");
  w->writeToFile(filename);

  return;

}

void 
SigModelFit(RooWorkspace* w, std::vector<string> cat_names) {

  Int_t ncat = NCAT;
  RooDataHist* sigToFit;  // create for one category so far
  RooAbsPdf* pdfSig;

  Float_t minMassFit(MMIN),maxMassFit(MMAX); 

  sigToFit   = (RooDataHist*) w->data("Sig_");
  pdfSig     = (RooAbsPdf*)  w->pdf("t3m_sig_shape");

  pdfSig->fitTo(*sigToFit,Range(minMassFit,maxMassFit));

  w->defineSet("SigPdfParam_", RooArgSet(*w->var("sig_m0"),*w->var("sig_sigma"),*w->var("sig_alpha"),*w->var("sig_n")));
  SetConstantParams(w->set("SigPdfParam_"));


}



void 
AddSigData(RooWorkspace* w, std::vector<string> cat_names) {

  Int_t ncat = NCAT;

  TFile *f = new TFile("input_histograms.root","READ");
  TH1F *taumass;
  taumass = (TH1F*)f->Get("signal"); // debugging
  RooDataHist sighist("sighist","sighist",*w->var("m3m"),Import(*taumass));


  w->import(sighist,Rename("Sig_"));
}


void 
AddBkgData(RooWorkspace* w, std::vector<string> cat_names) {

  Int_t ncat = NCAT;

  TFile *f = new TFile("input_histograms.root","READ");
  TH1F *taumass;
  taumass = (TH1F*)f->Get("background"); // debugging
  RooDataHist bkghist("bkghist","bkghist",*w->var("m3m"),Import(*taumass));

  w->import(bkghist,Rename("Bkg_"));
}



void 
BkgModelFit(RooWorkspace* w,  std::vector<string>, RooFitResult* fitresults){


  Int_t ncat = NCAT; // reserved for categories
  RooDataSet* data;
  RooPlot* plotbkg_fit;

 
  RooRealVar* m3m     = w->var("m3m");  
  m3m->setUnit("GeV");
  data   = (RooDataSet*) w->data("Bkg_");
  m3m->setMin(MMIN);
  m3m->setMax(MMAX);


  RooAbsPdf* bkg_fitTmp_1par = new RooGenericPdf("bkg_fit_1par_", "exp(@1*@0)", RooArgList(*w->var("m3m"), *w->var("bkg_exp_slope")));
  fitresults=bkg_fitTmp_1par->fitTo(*data, Strategy(1),Minos(kFALSE), Range(1.65,1.9),SumW2Error(kTRUE), Save(kTRUE),RooFit::PrintEvalErrors(-1));

  RooPlot *frame =((RooRealVar*) w->var("m3m"))->frame();
  
  w->import(*bkg_fitTmp_1par);

}


void 
MakeSigWS(RooWorkspace* w, const char* fileBaseName,  std::vector<string> cat_names) {

  TString wsDir   = "workspaces/";
  Int_t ncat = NCAT; // reserved for categories

  RooWorkspace *wAll = new RooWorkspace("w_all","w_all");
  RooAbsPdf* SigPdf;


  //(1) Retrieve p.d.f.s
  SigPdf = (RooAbsPdf*)  w->pdf("t3m_sig_shape");
  wAll->import(*w->pdf("t3m_sig_shape"));
  wAll->import(*w->data("Sig_"));

  //(2) factory of systematics


  TString filename(wsDir+TString(fileBaseName)+".root");
  wAll->writeToFile(filename);
  cout << "Write signal workspace in: " << filename << " file" << endl;
  
  return;

}


void 
MakeBkgWS(RooWorkspace* w, const char* fileBaseName, std::vector<string> cat_names) {

  TString wsDir   = "workspaces/";
  Int_t ncat = NCAT;   // reserve for categories

  RooDataSet* data;
  RooExtendPdf* bkg_fitPdf;

  RooWorkspace *wAll = new RooWorkspace("w_all","w_all");
  data = (RooDataSet*) w->data("Bkg_");

  wAll->import(*data,Rename("data_obs"));
  wAll->import(*w->pdf("bkg_fit_1par_"));
  wAll->import(*w->data("Bkg_"));

  TString filename(wsDir+TString(fileBaseName)+".root");
  wAll->writeToFile(filename);

  return;
}



void MakeDataCard(RooWorkspace* w, const char* fileBaseName, const char* fileBkgName,  std::vector<string> cat_names) {

  TString cardDir = "datacards/";
  Int_t ncat = NCAT;
  TString wsDir   = "workspaces/";

  RooDataSet* data;
  RooDataSet* signal;

  data  = (RooDataSet*) w->data("Bkg_");  //  meaningless for now
  signal = (RooDataSet*) w->data("Sig_");
  TString filename(cardDir+TString(fileBaseName)+".txt");
  ofstream outFile(filename);

  
  outFile << "# Fully Hadronic HH analysis" << endl;
  outFile << "imax 1" << endl;
  outFile << "kmax *" << endl;
  outFile << "---------------" << endl;
  outFile << "shapes data_obs  T3M"  << wsDir+TString(fileBkgName)+".root" << " w_all:data_obs" << endl;
  outFile << "shapes bkg T3M"    << wsDir+TString(fileBkgName)+".root" << " w_all:bkg_fit_1par_" << endl;
  outFile << "shapes signal T3M" << wsDir+TString(fileBaseName)+".root" << " w_all:t3m_sig_shape" << endl;
  outFile << "---------------" << endl;
  outFile << "bin          1  "  << endl;
  outFile <<  "observation   "  <<  data->sumEntries() << endl;
  outFile << "------------------------------" << endl;
  outFile << "bin                  T3M  T3M           "<< endl;
  outFile << "process              signal     bkg     " << endl;
  outFile << "process                 0        1      " << endl;
  outFile <<  "rate                      "  << " " << signal->sumEntries()*signalScaler << " " << 1 << endl;
  outFile << "--------------------------------" << endl;
  outFile << "lumi_13TeV       lnN  1.027      - " << endl;
  outFile.close();
  
  cout << "Write data card in: " << filename << " file" << endl;
  
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


