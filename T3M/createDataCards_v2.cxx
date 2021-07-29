#include <string>
#include <map>

using namespace RooFit;
using namespace RooStats ;


static const Int_t NCAT = 6;
Double_t MMIN = 1.62;
Double_t MMAX = 2.0;
double signalScaler=1;///10.;
double analysisLumi = 1.;   // 1/fb

void AddSigData(TString, RooWorkspace*,  std::vector<string>);
void AddBkgData(TString, RooWorkspace*,  std::vector<string>);
void SigModelFit(RooWorkspace*, std::vector<string>, TString type, TString Run);
void BkgModelFit(RooWorkspace*, std::vector<string>, RooFitResult** fitresults, bool sidebands, std::vector<string> cat_names);
void MakeSigWS(RooWorkspace* w, const char* filename,  std::vector<string>);
void MakeBkgWS(RooWorkspace* w, const char* filename,  std::vector<string>);
void MakeDataCard(RooWorkspace* w, const char* fileBaseName, const char* fileBkgName,  std::vector<string> cat_names, TString Run);
void MakeCombinedDataCard(RooWorkspace* w, const char* fileBaseName, const char* fileBkgName,  std::vector<string> cat_names);
void MakePlots(RooWorkspace* w,   std::vector<string> cat_names);
void MakePlotsSgn(RooWorkspace* w,   std::vector<string> cat_names);


// void MakePlots(RooWorkspace*, );


void SetConstantParams(const RooArgSet* params);


void 
createDataCards_v2(TString inputfile, int signalsample = 0, Bool_t dobands = false, string modelCard="model_card.rs", TString type="threeGlobal", TString Run="2017")
{
   ROOT::Minuit2::Minuit2Minimizer min (ROOT::Minuit2::kCombined);
   min.SetPrintLevel(0);
   gErrorIgnoreLevel = 1001;

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


   TString card_name(modelCard);
   HLFactory hlf("HLFactory", card_name, false);
   RooWorkspace* w = hlf.GetWs();
   RooFitResult* fitresults[NCAT];
   w->var("m3m")->setMin(MMIN);
   w->var("m3m")->setMax(MMAX);

   w->Print();
   bool doSideBands = true;
   AddSigData(inputfile,w,cat_names);
   AddBkgData(inputfile,w,cat_names);
   SigModelFit(w,cat_names,type,Run);

   MakeSigWS(w, fileBaseName, cat_names);
   BkgModelFit(w, cat_names, fitresults, doSideBands,cat_names);
   MakeBkgWS(w, fileBkgName,cat_names);
   MakeDataCard(w, fileBaseName, fileBkgName, cat_names, Run);

   TString filename("temp_workspace.root");
   w->writeToFile(filename);
   MakePlots(w,cat_names);
   MakePlotsSgn(w,cat_names);




   return;

}

void 
SigModelFit(RooWorkspace* w, std::vector<string> cat_names, TString type, TString Run) {

   Int_t ncat = NCAT;
   RooDataHist* sigToFit[NCAT];  
   RooAbsPdf* pdfSigCB[NCAT];
   RooAbsPdf* pdfSigGS[NCAT];
   RooAddPdf* SignalModel[NCAT];

   Float_t minMassFit(MMIN),maxMassFit(MMAX); 

   RooRealVar* m3m     = w->var("m3m");  

   m3m->setUnit("GeV");
   m3m->setRange("SB1",1.62,1.75);
   m3m->setRange("SB2",1.80,2.0);
   m3m->setRange("signal",1.70,1.85);
   m3m->setRange("fullRange",1.62,2.0);

   for (unsigned int category=0; category < NCAT; category++){
      sigToFit[category]     =  (RooDataHist*) w->data(TString::Format("Sig_%s",cat_names.at(category).c_str()));
      pdfSigCB[category]     =  (RooAbsPdf*)   w->pdf("t3m_sig_CBshape"+TString::Format("_%s",cat_names.at(category).c_str())+"_"+type);
      pdfSigGS[category]     =  (RooAbsPdf*)   w->pdf("t3m_sig_GSshape"+TString::Format("_%s",cat_names.at(category).c_str())+"_"+type);
   }

   for(unsigned int category=0; category< NCAT; category++)
   {

      std::cout<<"category  "<< cat_names.at(category).c_str() << std::endl;


      //parameters before fitting
      RooRealVar* sig_m0         = w->var(TString::Format("sig_m0_%s",cat_names.at(category).c_str())) ;
      RooRealVar* sig_sigma      = w->var(TString::Format("sig_sigma_%s",cat_names.at(category).c_str())) ;
      RooRealVar* sig_alpha      = w->var(TString::Format("sig_alpha_%s",cat_names.at(category).c_str())) ;
      RooRealVar* sig_n          = w->var(TString::Format("sig_n_%s",cat_names.at(category).c_str())) ;
      RooRealVar* sig_gaus_sigma = w->var(TString::Format("sig_gaus_sigma_%s",cat_names.at(category).c_str())) ;
      RooRealVar* CBFraction     = w->var(TString::Format("cb_fraction_%s",cat_names.at(category).c_str())) ; 

      SignalModel[category] = new RooAddPdf(TString::Format("SignalModel_fit_%s",cat_names.at(category).c_str()),"g+c",RooArgList(*pdfSigCB[category], *pdfSigGS[category]), *CBFraction);
      //SignalModel[category] is fitted to data for each category separately
      SignalModel[category]->fitTo(*sigToFit[category],Range("signal"), SumW2Error(kTRUE));

      //retrieving parameters from fitted shape
      
      // fix all the parameters expect for the nomralisation of signal
      TString name_mean = TString::Format("m0_fixed_%s",cat_names.at(category).c_str());
      TString name_sigma_cb = TString::Format("sigma_cb_fixed_%s",cat_names.at(category).c_str());
      TString name_sigma_gaus = TString::Format("sigma_gaus_fixed_%s",cat_names.at(category).c_str());
      TString name_alpha_cb = TString::Format("alpha_cb_fixed_%s",cat_names.at(category).c_str());
      TString name_n_cb = TString::Format("n_cb_fixed_%s",cat_names.at(category).c_str());
      TString name_f_cb = TString::Format("f_cb_%s",cat_names.at(category).c_str());

      RooRealVar mean    (name_mean,"mean", sig_m0->getVal(), sig_m0->getVal(), sig_m0->getVal() );
      RooRealVar sigma_cb (name_sigma_cb,"sigma_cb", sig_sigma->getVal(), sig_sigma->getVal(), sig_sigma->getVal() );
      RooRealVar sigma_gaus (name_sigma_gaus,"sigma_gaus",sig_gaus_sigma->getVal(), sig_gaus_sigma->getVal(), sig_gaus_sigma->getVal());
      RooRealVar alpha_cb (name_alpha_cb,"alpha_cb",sig_alpha->getVal(), sig_alpha->getVal(), sig_alpha->getVal());
      RooRealVar n_cb (name_n_cb,"n_cb",sig_n->getVal(), sig_n->getVal(), sig_n->getVal());
      RooRealVar f_cb (name_f_cb,"f_cb",CBFraction->getVal(), CBFraction->getVal(), CBFraction->getVal());

      mean.setError(sig_m0->getError());
      sigma.setError(sig_sigma->getError());
      sigma_gaus.setError(sig_gaus_sigma->getError());
      alpha_cb.setError(sig_alpha->getError());
      n_cb.setError(sig_n->getError());
      f_cb.setError(CBFraction->getError());

      //RooCBShape CB_final(TString::Format("CB_final_%s",cat_names.at(category).c_str())+"_"+type+"_"+Run,"CB PDF",*m3m,mean,sigma_cb,*sig_alpha,*sig_n) ;
      //RooGaussian GS_final(TString::Format("GS_final_%s",cat_names.at(category).c_str())+"_"+type+"_"+Run,"GS PDF",*m3m,mean,*sig_gaus_sigma) ;
      //RooAddPdf signal(TString::Format("SignalModel_%s",cat_names.at(category).c_str()),"",RooArgList(CB_final,GS_final), *CBFraction);
      
      RooCBShape CB_final(TString::Format("CB_final_%s",cat_names.at(category).c_str())+"_"+type+"_"+Run,"CB PDF",*m3m,mean,sigma_cb,alpha_cb,n_cb) ;
      RooGaussian GS_final(TString::Format("GS_final_%s",cat_names.at(category).c_str())+"_"+type+"_"+Run,"GS PDF",*m3m,mean,sigma_gaus) ;
      RooAddPdf signal(TString::Format("SignalModel_%s",cat_names.at(category).c_str()),"",RooArgList(CB_final,GS_final), f_cb);

      w->import(mean);
      w->import(sigma_cb);
      w->import(sigma_gaus);
      w->import(n_cb);
      w->import(alpha_cb);
      w->import(f_cb);
      w->defineSet(TString::Format("SigPdfParam_%s",cat_names.at(category).c_str()), RooArgSet(
               mean, //*w->var("sig_m0"+TString::Format("_%s",cat_names.at(category).c_str())),
               sigma_cb, //*w->var("sig_sigma"+TString::Format("_%s",cat_names.at(category).c_str())),
               sigma_gaus, //*w->var("sig_gaus_sigma"+TString::Format("_%s",cat_names.at(category).c_str())),
               alpha_cb, //*w->var("sig_alpha"+TString::Format("_%s",cat_names.at(category).c_str())),
               n_cb, //*w->var("sig_n"+TString::Format("_%s",cat_names.at(category).c_str()))));
               f_cb //*w->var("CBFraction"+TString::Format("_%s",cat_names.at(category).c_str()));
               )); 
      SetConstantParams(w->set(TString::Format("SigPdfParam_%s",cat_names.at(category).c_str())));

      //w->import(*SignalModel[category]);
      w->import(signal);
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

   m3m->setUnit("GeV");
   m3m->setRange("SB1",1.62,1.73);
   m3m->setRange("SB2",1.81,2.0);
   m3m->setRange("SB1_A",1.62,1.753);
   m3m->setRange("SB2_A",1.801,2.0);
   m3m->setRange("SB1_B",1.62,1.739);
   m3m->setRange("SB2_B",1.815,2.0);
   m3m->setRange("SB1_C",1.62,1.727);
   m3m->setRange("SB2_C",1.827,2.0);
   m3m->setRange("fullRange",1.62,2.0);

   TLatex *text = new TLatex();
   text->SetNDC();
   text->SetTextSize(0.04);
   TCut sidebands = TCut("(m3m < 1.75 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.80)");
   cout<<" bkg fit "<<endl;

   RooPlot* plot[NCAT];
   for(unsigned int category=0; category< NCAT; category++){
      plot[category] = m3m->frame();
      signalAll[category]->plotOn( plot[category],RooFit::MarkerColor(kCyan+2),RooFit::MarkerStyle(6),RooFit::MarkerSize(0.75));
      sigpdf[category]->plotOn(plot[category], RooFit::LineColor(kCyan+2),RooFit::LineWidth(2));

      Double_t Nratio(0.);
      Double_t Nentries(static_cast<Double_t>(dataAll[category]->sumEntries()));
      if ( category%3==0 ) Nratio=(static_cast<Double_t>((dataAll[category]->reduce("(m3m < 1.753 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.801)")->sumEntries())))/(static_cast<Double_t>(Nentries));
      if ( category%3==1 ) Nratio=(static_cast<Double_t>((dataAll[category]->reduce("(m3m < 1.739 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.815)")->sumEntries())))/(static_cast<Double_t>(Nentries));
      if ( category%3==2 ) Nratio=(static_cast<Double_t>((dataAll[category]->reduce("(m3m < 1.727 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.827)")->sumEntries())))/(static_cast<Double_t>(Nentries));

      //ataAll[category]->plotOn(plot[category],CutRange("SB1,SB2"),RooFit::MarkerColor(kGray+3),RooFit::MarkerStyle(21),RooFit::MarkerSize(0.75));
      if ( category==0 || category==3 ) dataAll[category]->plotOn(plot[category],CutRange("SB1_A,SB2_A"),RooFit::MarkerColor(kGray+3),RooFit::MarkerStyle(21),RooFit::MarkerSize(0.75));
      if ( category==1 || category==4 ) dataAll[category]->plotOn(plot[category],CutRange("SB1_B,SB2_B"),RooFit::MarkerColor(kGray+3),RooFit::MarkerStyle(21),RooFit::MarkerSize(0.75));
      if ( category==2 || category==5 ) dataAll[category]->plotOn(plot[category],CutRange("SB1_C,SB2_C"),RooFit::MarkerColor(kGray+3),RooFit::MarkerStyle(21),RooFit::MarkerSize(0.75));


      //dataAll[category]->plotOn(plot[category],RooFit::MarkerColor(kGray+3),RooFit::MarkerStyle(21),RooFit::MarkerSize(0.75));
      //bkgpdf[category]->plotOn(plot[category],Normalization(Nratio, RooAbsReal::Relative), Range("fullRange"),RooFit::LineColor(kGray+3),RooFit::LineWidth(2));
      if ( category==0 || category==3 ) bkgpdf[category]->plotOn(plot[category],Normalization(Nratio, RooAbsReal::Relative), Range("SB1_A,SB2_A"),RooFit::LineColor(kGray+3),RooFit::LineWidth(2));
      if ( category==1 || category==4 ) bkgpdf[category]->plotOn(plot[category],Normalization(Nratio, RooAbsReal::Relative), Range("SB1_B,SB2_B"),RooFit::LineColor(kGray+3),RooFit::LineWidth(2));
      if ( category==2 || category==5 ) bkgpdf[category]->plotOn(plot[category],Normalization(Nratio, RooAbsReal::Relative), Range("SB1_C,SB2_C"),RooFit::LineColor(kGray+3),RooFit::LineWidth(2));


      //bkgpdf[category]->paramOn( plot[category], Format("NELU", AutoPrecision(2)),ShowConstants(), Layout(0.4,0.99,0.9));
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
      TLegend *legmc = new TLegend(0.50,0.70,0.86,0.86);

      legmc->AddEntry(plot[category]->getObject(0),"MC Signal (B=10-e7)","LPE");
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
MakePlotsSgn(RooWorkspace* w,   std::vector<string> cat_names){

   Int_t ncat = NCAT;
   RooDataHist* signalAll[NCAT]; 
   RooAbsPdf* sigpdf[NCAT]; 

   for(unsigned int category=0; category< NCAT; category++){
      signalAll[category]=  (RooDataHist*) w->data(TString::Format("Sig_%s",cat_names.at(category).c_str()));
      sigpdf[category] =(RooAbsPdf*)w->pdf("SignalModel"+TString::Format("_%s",cat_names.at(category).c_str()));
   }

   RooRealVar* m3m     = w->var("m3m");  

   m3m->setUnit("GeV");
   m3m->setRange("SB1",1.62,1.75);
   m3m->setRange("SB2",1.80,2.0);
   m3m->setRange("fullRange",1.62,2.0);


   TLatex *text = new TLatex();
   text->SetNDC();
   text->SetTextSize(0.04);

   RooPlot* plot_sgn[NCAT];
   for(unsigned int category=0; category< NCAT; category++){
      plot_sgn[category] = m3m->frame();
      signalAll[category]->plotOn( plot_sgn[category],RooFit::MarkerColor(kCyan+2),RooFit::MarkerStyle(6),RooFit::MarkerSize(0.75));
      //signalAll[category]->statOn( plot_sgn[category],Layout(0.65,0.99,0.9)) ;
      sigpdf[category]->plotOn( plot_sgn[category], RooFit::LineColor(kCyan+2),RooFit::LineWidth(2));
      sigpdf[category]->paramOn( plot_sgn[category], Format("NELU", AutoPrecision(4)), ShowConstants(), Layout(0.55,0.99,0.9));


      plot_sgn[category]->SetTitle(TString::Format("Category %s",cat_names.at(category).c_str()));     
      plot_sgn[category]->SetMinimum(0.01);
      plot_sgn[category]->SetMaximum(1.40*plot_sgn[category]->GetMaximum());
      plot_sgn[category]->GetXaxis()->SetTitle("m_{3mu} [GeV]");

      TCanvas* ctmp_sig = new TCanvas(TString::Format("Category %s",cat_names.at(category).c_str()),"Categories",0,0,700,500);
      ctmp_sig->SetFrameLineWidth(3);
      ctmp_sig->SetTickx();
      ctmp_sig->SetTicky();
      plot_sgn[category]->Draw();
      plot_sgn[category]->Print();
      plot_sgn[category]->Draw("SAME");
      TLegend *legmc = new TLegend(0.12,0.70,0.43,0.86);

      legmc->AddEntry(plot_sgn[category]->getObject(0),"MC Signal (B=10-e7)","LPE");
      legmc->AddEntry(plot_sgn[category]->getObject(1),"Signal Model","L");

      legmc->SetBorderSize(0);
      legmc->SetFillStyle(0);
      legmc->SetTextSize(0.029);

      legmc->Draw();  
      ctmp_sig->SaveAs("plots/"+TString::Format("Signal_%s",cat_names.at(category).c_str())+".png");
   }
}

void 
AddSigData(TString file, RooWorkspace* w, std::vector<string> cat_names) {

   TFile *f = new TFile(file,"READ");
   TH1F *taumass[NCAT];
   TH1F *taumass_combined[3];

   for(unsigned int category=0; category< NCAT; category++){
      TString name = TString::Format("Sig_%s",cat_names.at(category).c_str());
      
      taumass[category] = (TH1F*)f->Get(TString::Format("signal%s",cat_names.at(category).c_str()));
      if (category<3) taumass_combined[category] = (TH1F*)f->Get(TString::Format("signal%s",cat_names.at(category).c_str()));
      else taumass_combined[category%3]->Add((TH1F*)f->Get(TString::Format("signal%s",cat_names.at(category).c_str())));

      RooDataHist sighist("sighist","sighist",*w->var("m3m"),Import(*taumass[category]));
      w->import(sighist,Rename(name));
   }

   for (int i=0; i<3; i++) {
      TString name = TString::Format("Sig_combined_%c",(char)(66+i));
      RooDataHist sighist_combined("sighist_combined","sighist_combined",*w->var("m3m"), Import(*taumass_combined[i]));
      w->import(sighist_combined,Rename(name));
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
   /*
      m3m->setRange("SB1",1.62,1.75);
      m3m->setRange("SB2",1.80,2.0);
      m3m->setRange("signal",1.70,1.85);
      m3m->setRange("fullRange",1.62,2.0);
      */
   m3m->setRange("SB1_A",1.62,1.753);
   m3m->setRange("SB2_A",1.801,2.0);
   m3m->setRange("SB1_B",1.62,1.739);
   m3m->setRange("SB2_B",1.815,2.0);
   m3m->setRange("SB1_C",1.62,1.727);
   m3m->setRange("SB2_C",1.827,2.0);
   m3m->setRange("fullRange",1.62,2.0);


   for(unsigned int category=0; category< NCAT; category++)
   {
      data[category]   = (RooDataSet*) w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str()));
      bkg_fitTmp_1par[category] = new RooGenericPdf(TString::Format("bkg_fit_1par_%s",cat_names.at(category).c_str()), "exp(@1*@0 + @2)", 
            RooArgList(*w->var("m3m"), 
               *w->var(TString::Format("bkg_exp_slope_%s",cat_names.at(category).c_str())),
               *w->var(TString::Format("bkg_exp_offset_%s",cat_names.at(category).c_str()))));   // Generig BKG pdf for more careful description
      //fitresults[category]=bkg_fitTmp_1par[category]->fitTo(*data[category], Strategy(1), Minos(kFALSE), Range("SB1,SB2"),SumW2Error(kTRUE), Save(kTRUE),RooFit::PrintEvalErrors(-1));
      if ( category==0 || category==3 ) fitresults[category]=bkg_fitTmp_1par[category]->fitTo(*data[category], Strategy(1), Minos(kFALSE), Range("SB1_A,SB2_A"), SumW2Error(kTRUE), Save(kTRUE),RooFit::PrintEvalErrors(-1));
      if ( category==1 || category==4 ) fitresults[category]=bkg_fitTmp_1par[category]->fitTo(*data[category], Strategy(1), Minos(kFALSE), Range("SB1_B,SB2_B"), SumW2Error(kTRUE), Save(kTRUE),RooFit::PrintEvalErrors(-1));
      if ( category==2 || category==5 ) fitresults[category]=bkg_fitTmp_1par[category]->fitTo(*data[category], Strategy(1), Minos(kFALSE), Range("SB1_C,SB2_C"), SumW2Error(kTRUE), Save(kTRUE),RooFit::PrintEvalErrors(-1));

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





void MakeDataCard(RooWorkspace* w, const char* fileBaseName, const char* fileBkgName,  std::vector<string> cat_names, TString Run){

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
      //std::cout<<"category  "<< cat_names.at(c).c_str()  << "  Observed:  "<<  data[c]->sumEntries() << endl;
      std::cout<<"category  "<< cat_names.at(c).c_str()  << "  Observed:  -1" << endl;
      outFile << "------------------------------" << endl;

      outFile << Form("bin               %s        %s     ",cat_names.at(c).c_str(),cat_names.at(c).c_str())<<  endl;
      outFile << "process              signal     bkg     " << endl;
      outFile << "process                0          1      " << endl;
      //outFile << "rate                "  << " " << signal[c]->sumEntries()*signalScaler << "    " <<  data[c]->sumEntries()  << endl;
      outFile << "rate                "  << " " << signal[c]->sumEntries()*signalScaler << "    " <<  data[c]->sumEntries()  << endl;
      outFile << "--------------------------------" << endl;


      //outFile << "lumi_13TeV       lnN  1.027      - " << endl;
      //outFile << "lumi_13TeV        lnN  1.027     - " << endl;
      //outFile << "DsNorm_13TeV      lnN  1.033     - " << endl;
      if (Run.Contains("2018")){ 
         outFile << "DsNorm_13TeV      lnN  1.03      - " << endl; // updated on 13 April
         outFile << "BRDToTau_13TeV    lnN  1.03      - " << endl;
         outFile << "BRDsPhiPi_13TeV   lnN  1.08      - " << endl;
         outFile << "BRBtoD_13TeV      lnN  1.05      - " << endl;
         outFile << "BRBtoTau_13TeV    lnN  1.03      - " << endl;    
         outFile << "fUnc_13TeV        lnN  1.07      - " << endl; // updated on 13 April
         outFile << "DpmScaling_13TeV  lnN  1.03      - " << endl;
         outFile << "BsScaling_13TeV   lnN  1.04      - " << endl;
         outFile << "UncTrigger_13TeV  lnN  1.03      - " << endl; 
         outFile << "UncBDTCut_13TeV   lnN  1.06      - " << endl;
         outFile << "UncRatioAcc_13TeV lnN  1.01      - " << endl;
         outFile << "UncMuonEff_13TeV  lnN  1.015     - " << endl;
      }

      if (Run.Contains("2017")){
         //    outFile << "MuES_13TeV        lnN  1.007     - " << endl;
         //    outFile << "MuRes_13TeV       lnN  1.025     - " << endl;
         outFile << "DsNorm_13TeV      lnN  1.034      - " <<endl;
         outFile << "BRDToTau_13TeV    lnN  1.03      - " <<endl;
         outFile << "BRDsPhiPi_13TeV   lnN  1.08      - " <<endl;
         outFile << "BRBtoD_13TeV      lnN  1.05      - " <<endl;
         outFile << "BRBtoTau_13TeV    lnN  1.03      - " <<endl;
         outFile << "fUnc_13TeV        lnN  1.07      - " <<endl; // updated on 13 April
         outFile << "DpmScaling_13TeV  lnN  1.03      - " <<endl;
         outFile << "BsScaling_13TeV   lnN  1.04      - " <<endl;
         outFile << "UncTrigger_13TeV  lnN  1.05      - " <<endl;
         outFile << "UncBDTCut_13TeV   lnN  1.06      - " <<endl;
         outFile << "UncRatioAcc_13TeV lnN  1.01      - " <<endl;
         outFile << "UncMuonEff_13TeV  lnN  1.015     - " <<endl;
      }

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
