#include <string>
#include <sstream>
#include <fstream>
#include <map>

using namespace RooFit;
using namespace RooStats ;

Double_t MMIN = 1.62;
Double_t MMAX = 2.0;
double signalScaler=1;///10.;
double analysisLumi = 1.;   // 1/fb

void AddData(TString, RooWorkspace*, const Int_t NCAT, std::vector<string> branch_names, std::vector<string> cat_names, std::vector<string> bdt_val);
void SigModelFit(RooWorkspace*, const Int_t NCAT, std::vector<string>, RooFitResult** signal_fitresults, TString type, TString Run);
void BkgModelFit(RooWorkspace*, const Int_t NCAT, std::vector<string>, RooFitResult** bkg_fitresults, bool blind, std::vector<string> cat_names);
void MakeSigWS(RooWorkspace* w, const Int_t NCAT, const char* filename,  std::vector<string>);
void MakeBkgWS(RooWorkspace* w, const Int_t NCAT, const char* filename,  std::vector<string>);
void MakeDataCard(RooWorkspace* w, const Int_t NCAT, const char* fileBaseName, const char* fileBkgName, string configFile,  std::vector<string> cat_names, TString type, TString Run, bool blind);
void MakePlots(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, bool MultiPdf, bool blind, string configs);
void MakePlotsSplusB(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, bool MultiPdf, bool blind, string configs);
void MakePlotsSgn(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, string configs);

void SetConstantParams(const RooArgSet* params);
void tokenize(std::string const &str, const char delim, std::vector<std::string> &out);

void
createDataCards(TString inputfile, int signalsample = 0, bool blind = true, string modelCard="model_card.rs", string configFile="config.txt", TString type="threeGlobal", TString Run="2017", bool MultiPdf = false)
{
   //Set verbosity
   ROOT::Minuit2::Minuit2Minimizer min (ROOT::Minuit2::kCombined);
   min.SetPrintLevel(0);
   gErrorIgnoreLevel = 1001;

   cout<< "Blind option "<<blind<<endl;
   vector<string> branch_names; // reserved to handle names for relevant branches
   vector<string> cat_names; // reserved to handle categories
   vector<string> bdt_val; // reserved to handle bdt cuts
   string lines[3]; //

   //read config file
   std::ifstream file(configFile);
   if (file.is_open()) {
       std::string line; int i=0;
       while (std::getline(file, line) && i<3) {
           lines[i]=line; i++;
       }
       file.close();
   }
   tokenize(lines[0], ',', branch_names);
   tokenize(lines[1], ',', cat_names);
   tokenize(lines[2], ',', bdt_val);

   if(cat_names.size()!=bdt_val.size() && cat_names.size()>0){
       cout<<"Please check content of "<<configFile; return;
   }

   //retrieve number of categories
   const Int_t NCAT = cat_names.size();
   cout<<"Number of categories is "<<NCAT<<endl;

   TString signalname("T3MSignal");
   TString bkgname("T3MBkg");

   string configFile_prefix =  configFile.erase(configFile.size() - 4);

   TString fileBaseName("CMS_"+signalname + configFile_prefix + "_13TeV");
   TString fileBkgName("CMS_"+bkgname + configFile_prefix + "_13TeV");

   TString card_name(modelCard);
   HLFactory hlf("HLFactory", card_name, false);
   RooWorkspace* w = hlf.GetWs();
   RooFitResult* bkg_fitresults[NCAT];
   RooFitResult* signal_fitresults[NCAT];
   w->var("m3m")->setMin(MMIN);
   w->var("m3m")->setMax(MMAX);

   w->Print();
   AddData(inputfile,w,NCAT,branch_names,cat_names,bdt_val);

   SigModelFit(w, NCAT, cat_names, signal_fitresults, type, Run);
   MakeSigWS(w, NCAT, fileBaseName, cat_names);

   BkgModelFit(w, NCAT, cat_names, bkg_fitresults, blind, cat_names);
   MakeBkgWS(w, NCAT, fileBkgName, cat_names);

   MakeDataCard(w, NCAT, fileBaseName, fileBkgName, configFile_prefix, cat_names, type, Run, blind);

   TString filename("temp_workspace.root");
   w->writeToFile(filename);
   MakePlots(w,NCAT,cat_names,MultiPdf, blind, configFile_prefix);
   //MakePlotsSplusB(w,NCAT,cat_names,MultiPdf, blind,configFile_prefix);
   MakePlotsSgn(w,NCAT,cat_names,configFile_prefix);

   w->Print();

   return;

}


void
SigModelFit(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, RooFitResult** signal_fitresults, TString type, TString Run) {

   RooDataSet* sigToFit[NCAT];
   RooAbsPdf* pdfSigCB[NCAT];
   RooAbsPdf* pdfSigGS[NCAT];
   RooAddPdf* SignalModel[NCAT];

   Float_t minMassFit(MMIN),maxMassFit(MMAX); 

   RooRealVar* m3m = w->var("m3m");  

   m3m->setUnit("GeV");
   m3m->setRange("signal",1.70,1.85);
   m3m->setRange("fullRange",1.62,2.0);

   for (unsigned int category=0; category < NCAT; category++){
      sigToFit[category]     =  (RooDataSet*)  w->data(TString::Format("Sig_%s",cat_names.at(category).c_str()));
      pdfSigCB[category]     =  (RooAbsPdf*)   w->pdf("t3m_sig_CBshape"+TString::Format("_%s",cat_names.at(category).c_str())+"_"+type);
      pdfSigGS[category]     =  (RooAbsPdf*)   w->pdf("t3m_sig_GSshape"+TString::Format("_%s",cat_names.at(category).c_str())+"_"+type);
   }

   for(unsigned int category=0; category< NCAT; category++)
   {

      std::cout<<"category  "<< cat_names.at(category).c_str() << std::endl;


      //parameters before fitting
      RooRealVar* sig_m0         = w->var(TString::Format("sig_m0_%s",cat_names.at(category).c_str())) ;
      RooRealVar* sig_sigma      = w->var(TString::Format("sig_sigma_%s",cat_names.at(category).c_str())) ;
      RooRealVar* sig_sigma_cb   = w->var(TString::Format("sig_sigma_cb_%s",cat_names.at(category).c_str())) ;
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
      TString name_sigma = TString::Format("sigma_fixed_%s",cat_names.at(category).c_str());
      //TString name_sigma_cb = TString::Format("sigma_cb_fixed_%s",cat_names.at(category).c_str());
      TString name_sigma_gaus = TString::Format("sigma_gaus_fixed_%s",cat_names.at(category).c_str());
      TString name_alpha_cb = TString::Format("alpha_cb_fixed_%s",cat_names.at(category).c_str());
      TString name_n_cb = TString::Format("n_cb_fixed_%s",cat_names.at(category).c_str());
      TString name_f_cb = TString::Format("f_cb_%s",cat_names.at(category).c_str());

      RooRealVar mean    (name_mean,"mean", sig_m0->getVal(), sig_m0->getVal(), sig_m0->getVal() );
      RooRealVar sigma (name_sigma,"sigma", sig_sigma->getVal(), sig_sigma->getVal(), sig_sigma->getVal() );
      //RooRealVar sigma_cb (name_sigma_cb,"sigma_cb", sig_sigma_cb->getVal(), sig_sigma_cb->getVal(), sig_sigma_cb->getVal() );
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

      char line[100];
      RooRealVar UncMean(TString::Format("UncMean_%s", cat_names.at(category).c_str()), "UncMean", 0., -5, 5);
      sprintf(line, "(1+0.0009*%s_%s)*%.5f","UncMean", cat_names.at(category).c_str(), sig_m0->getVal()*0.9991); // According to ANv2 L798, “mean” is 0.09% smaller in data. So we scale MC “mean” by 0.9991, and assign 0.0009 uncertainty
      RooFormulaVar fmean(TString::Format("fmean_%s", cat_names.at(category).c_str()),line,RooArgList(UncMean));

      char line2[100];
      RooRealVar UncSigma(TString::Format("UncSigma_%s", cat_names.at(category).c_str()), "UncSigma", 0., -5, 5);
      //sprintf(line2, "(1+0.02*%s_%s)*%.5f", "UncSigma", cat_names.at(category).c_str(), CBFraction->getVal()*sig_sigma->getVal()+(1-CBFraction->getVal())*sig_gaus_sigma->getVal()); // According to Fig47, MC has up to 2% worse resolution! We don’t scale the MC resolution, but only assign 2% uncertainty
      sprintf(line2, "(1+0.02*%s_%s)*%.5f", "UncSigma", cat_names.at(category).c_str(), sig_sigma->getVal()); // According to Fig47, MC has up to 2% worse resolution! We don’t scale the MC resolution, but only assign 2% uncertainty
      RooFormulaVar fsigma(TString::Format("fsigma_%s", cat_names.at(category).c_str()),line2,RooArgList(UncSigma));
      
      //RooCBShape CB_final(TString::Format("CB_final_%s",cat_names.at(category).c_str())+"_"+type+"_"+Run,"CB PDF",*m3m,mean,sigma_cb,*sig_alpha,*sig_n) ;
      //RooGaussian GS_final(TString::Format("GS_final_%s",cat_names.at(category).c_str())+"_"+type+"_"+Run,"GS PDF",*m3m,mean,*sig_gaus_sigma) ;
      //RooAddPdf signal(TString::Format("SignalModel_%s",cat_names.at(category).c_str()),"",RooArgList(CB_final,GS_final), *CBFraction);

      RooCBShape CB_final(TString::Format("CB_final_%s",cat_names.at(category).c_str())+"_"+type+"_"+Run,"CB PDF",*m3m,mean,sigma,alpha_cb,n_cb) ;
      RooGaussian GS_final(TString::Format("GS_final_%s",cat_names.at(category).c_str())+"_"+type+"_"+Run,"GS PDF",*m3m,mean,sigma_gaus) ;
      RooAddPdf signal(TString::Format("SignalModel_%s",cat_names.at(category).c_str()),"",RooArgList(CB_final,GS_final), f_cb);
      
      // then recreate the signal shape using the 2 RooFormulaVar and the other 4 parameters
      //RooGaussian signal1("Signal1","",M3m,fmean,sigma_gaus) ;
      //RooCBShape signal2("Signal2","",M3m,fmean,fsigma,alpha_cb,n_cb) ;
      //RooAddPdf signal("Signal","",RooArgList(signal1,signal2), frac_gaus);

      w->import(mean);
      w->import(sigma);
      w->import(sigma_gaus);
      w->import(n_cb);
      w->import(alpha_cb);
      w->import(f_cb);
      w->defineSet(TString::Format("SigPdfParam_%s",cat_names.at(category).c_str()), RooArgSet(
               mean, //*w->var("sig_m0"+TString::Format("_%s",cat_names.at(category).c_str())),
               sigma, //*w->var("sig_sigma"+TString::Format("_%s",cat_names.at(category).c_str())),
               //sigma_cb,
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
MakePlotsSplusB(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, bool MultiPdf, bool blind, string configs){

   RooDataSet* signalAll[NCAT];
   RooDataSet* dataAll[NCAT];
   RooDataSet* dataToPlot[NCAT];
   RooAbsPdf* sigpdf[NCAT];
   RooAbsPdf* bkgpdf[NCAT]; // exp
   RooAbsPdf* bkgpdf2[NCAT];  // power law

   TCut sidebands;
   RooRealVar* m3m     = w->var("m3m");  
   m3m->setUnit("GeV");

   for(unsigned int category=0; category< NCAT; category++){
      if (category%3==0)      sidebands = TCut("(m3m < 1.75 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.80)");
      else if (category%3==1) sidebands = TCut("(m3m < 1.74 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.82)");
      else if (category%3==2) sidebands = TCut("(m3m < 1.73 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.83)");

      signalAll[category]=  (RooDataSet*) w->data(TString::Format("Sig_%s",cat_names.at(category).c_str()));
      dataAll[category]=    (RooDataSet*) w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str()));

      //blind data
      if(blind) dataToPlot[category] = (RooDataSet*)dataAll[category]->reduce(sidebands);
      else dataToPlot[category] = (RooDataSet*)dataAll[category]->reduce("m3m > 1.62 && m3m < 2.0");
      dataToPlot[category]->Print();

      sigpdf[category] =(RooAbsPdf*)w->pdf("SignalModel"+TString::Format("_%s",cat_names.at(category).c_str()));
      bkgpdf[category] =(RooAbsPdf*)w->pdf(TString::Format("t3m_bkg_expo_%s",cat_names.at(category).c_str()));
      bkgpdf2[category] =(RooAbsPdf*)w->pdf(TString::Format("bkg_powerlawpdf_%s",cat_names.at(category).c_str()));
   }

   m3m->setRange("SB1_A",1.62,1.75);
   m3m->setRange("SB2_A",1.80,2.0);
   m3m->setRange("SB1_B",1.62,1.74);
   m3m->setRange("SB2_B",1.82,2.0);
   m3m->setRange("SB1_C",1.62,1.73);
   m3m->setRange("SB2_C",1.83,2.0);
   m3m->setRange("fullRange",1.62,2.0);

   TLatex *text = new TLatex();
   text->SetNDC();
   text->SetTextSize(0.04);
   cout<<" bkg fit "<<endl;

   RooPlot* plot[NCAT];
   for(unsigned int category=0; category< NCAT; category++){
      plot[category] = m3m->frame();
      signalAll[category]->plotOn( plot[category],RooFit::MarkerColor(kCyan+2),RooFit::MarkerStyle(6),RooFit::MarkerSize(0.0), Binning(38, 1.620000, 2.00000));
      sigpdf[category]->plotOn(plot[category], RooFit::LineColor(kRed),RooFit::LineWidth(3));
  
      //plot data 
      if (category%3==0) dataToPlot[category]->plotOn(plot[category],RooFit::MarkerColor(kBlack),RooFit::MarkerStyle(8),RooFit::MarkerSize(1),RooFit::LineWidth(3), Binning(38, 1.620000, 2.00000));
      if (category%3==1) dataToPlot[category]->plotOn(plot[category],RooFit::MarkerColor(kBlack),RooFit::MarkerStyle(8),RooFit::MarkerSize(1),RooFit::LineWidth(3), Binning(38, 1.620000, 2.00000));
      if (category%3==2) dataToPlot[category]->plotOn(plot[category],RooFit::MarkerColor(kBlack),RooFit::MarkerStyle(8),RooFit::MarkerSize(1),RooFit::LineWidth(3), Binning(38, 1.620000, 2.00000));
      if(blind){
          //plot pdf in sidebands
          if ( category%3==0 ) bkgpdf[category]->plotOn(plot[category], Range("SB1_A,SB2_A"), RooFit::NormRange("SB1_A,SB2_A"), RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==1 ) bkgpdf[category]->plotOn(plot[category], Range("SB1_B,SB2_B"), RooFit::NormRange("SB1_B,SB2_B"), RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==2 ) bkgpdf[category]->plotOn(plot[category], Range("SB1_C,SB2_C"), RooFit::NormRange("SB1_C,SB2_C"), RooFit::LineColor(kBlue), RooFit::LineWidth(3));

          if(MultiPdf){
            if ( category%3==0 ) bkgpdf2[category]->plotOn(plot[category], Range("SB1_A,SB2_A"),RooFit::NormRange("SB1_A,SB2_A"), RooFit::LineColor(kBlue),RooFit::LineWidth(3));
            if ( category%3==1 ) bkgpdf2[category]->plotOn(plot[category], Range("SB1_B,SB2_B"),RooFit::NormRange("SB1_B,SB2_B"), RooFit::LineColor(kBlue),RooFit::LineWidth(3));
            if ( category%3==2 ) bkgpdf2[category]->plotOn(plot[category], Range("SB1_C,SB2_C"),RooFit::NormRange("SB1_B,SB2_B"), RooFit::LineColor(kBlue),RooFit::LineWidth(3));
          }
      }else{
          //plot pdf in full range
          if ( category%3==0 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==1 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==2 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));

          if(MultiPdf){
            if ( category%3==0 ) bkgpdf2[category]->plotOn(plot[category], RooFit::LineColor(kBlue),RooFit::LineWidth(3));
            if ( category%3==1 ) bkgpdf2[category]->plotOn(plot[category], RooFit::LineColor(kBlue),RooFit::LineWidth(3));
            if ( category%3==2 ) bkgpdf2[category]->plotOn(plot[category], RooFit::LineColor(kBlue),RooFit::LineWidth(3));
          }
      }

      //plot signal+bkg
      RooRealVar bkgfrac("bkgfrac", "fraction of background", 0.9, 0., 1.);
      RooAddPdf model("model", "s+b", RooArgList(*bkgpdf[category], *sigpdf[category]), bkgfrac);
      model.fitTo(*dataToPlot[category], RooFit::Extended());
      model.plotOn(plot[category], RooFit::LineColor(kGreen), RooFit::LineWidth(3));

      //bkgpdf[category]->paramOn( plot[category], Format("NELU", AutoPrecision(2)),ShowConstants(), Layout(0.4,0.99,0.9));
      plot[category]->SetTitle(TString::Format("Category %s",cat_names.at(category).c_str()));     
      plot[category]->SetMinimum(0.01);
      plot[category]->SetMaximum(1.40*plot[category]->GetMaximum());
      plot[category]->GetXaxis()->SetTitle("m_{3mu} [GeV]");

      cout<<"chi2 bkg category: "<<cat_names.at(category).c_str()<<" "<<plot[category]->chiSquare()<<endl;

      TCanvas* ctmp_sig = new TCanvas(TString::Format("Category %s",cat_names.at(category).c_str()),"Categories",0,0,660,660);
      ctmp_sig->SetFrameLineWidth(3);
      ctmp_sig->SetTickx();
      ctmp_sig->SetTicky();
      plot[category]->Draw();
      plot[category]->Print();
      plot[category]->Draw("SAME");

      TLegend *legmc = new TLegend(0.50,0.70,0.86,0.86);
      legmc->AddEntry(plot[category]->getObject(0),"MC Signal (B=10^{-7})","LPE");
      legmc->AddEntry(plot[category]->getObject(1),"Signal Model","L");
      legmc->AddEntry(plot[category]->getObject(2),"Data","LPE");
      legmc->AddEntry(plot[category]->getObject(3),"EXP","L");
      if(MultiPdf) legmc->AddEntry(plot[category]->getObject(5),"PowerLaw","L");

      legmc->SetBorderSize(0);
      legmc->SetFillStyle(0);
      legmc->SetTextSize(0.029);

      legmc->Draw();  
      ctmp_sig->SaveAs("plots/"+TString::Format("Category_%s_SplusB",cat_names.at(category).c_str())+configs+".png");
   }
}



void
MakePlots(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, bool MultiPdf, bool blind, string configs){

   RooDataSet* signalAll[NCAT];
   RooDataSet* dataAll[NCAT];
   RooDataSet* dataToPlot[NCAT];
   RooAbsPdf* sigpdf[NCAT];
   RooAbsPdf* bkgpdf[NCAT]; // exp
   RooAbsPdf* bkgpdf2[NCAT];  // power law

   TCut sidebands;
   RooRealVar* m3m     = w->var("m3m");  
   m3m->setUnit("GeV");

   for(unsigned int category=0; category< NCAT; category++){
      if (category%3==0)      sidebands = TCut("(m3m < 1.75 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.80)");
      else if (category%3==1) sidebands = TCut("(m3m < 1.74 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.82)");
      else if (category%3==2) sidebands = TCut("(m3m < 1.73 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.83)");

      signalAll[category]=  (RooDataSet*) w->data(TString::Format("Sig_%s",cat_names.at(category).c_str()));
      dataAll[category]=    (RooDataSet*) w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str()));

      //blind data
      if(blind) dataToPlot[category] = (RooDataSet*)dataAll[category]->reduce(sidebands);
      else dataToPlot[category] = (RooDataSet*)dataAll[category]->reduce("m3m > 1.62 && m3m < 2.0");
      dataToPlot[category]->Print();

      sigpdf[category] =(RooAbsPdf*)w->pdf("SignalModel"+TString::Format("_%s",cat_names.at(category).c_str()));
      bkgpdf[category] =(RooAbsPdf*)w->pdf(TString::Format("t3m_bkg_expo_%s",cat_names.at(category).c_str()));
      bkgpdf2[category] =(RooAbsPdf*)w->pdf(TString::Format("bkg_powerlawpdf_%s",cat_names.at(category).c_str()));
   }

   m3m->setRange("SB1_A",1.62,1.75);
   m3m->setRange("SB2_A",1.80,2.0);
   m3m->setRange("SB1_B",1.62,1.74);
   m3m->setRange("SB2_B",1.82,2.0);
   m3m->setRange("SB1_C",1.62,1.73);
   m3m->setRange("SB2_C",1.83,2.0);

   m3m->setRange("SIG_A",1.75,1.80); //12MeV sigma
   m3m->setRange("SIG_B",1.74,1.82); //19MeV sigma
   m3m->setRange("SIG_C",1.73,1.83); //23MeV sigma
   m3m->setRange("fullRange",1.62,2.0);

   TLatex *text = new TLatex();
   text->SetNDC();
   text->SetTextSize(0.04);
      
   TString filename("yields.txt");
   ofstream outFile(filename);
   outFile << "cat\tsig\tbkg\n" << endl;

   RooPlot* plot[NCAT];
   for(unsigned int category=0; category< NCAT; category++){
      plot[category] = m3m->frame();
      signalAll[category]->plotOn( plot[category],RooFit::MarkerColor(kCyan+2),RooFit::MarkerStyle(6),RooFit::MarkerSize(0.0), Binning(38, 1.620000, 2.00000));
      sigpdf[category]->plotOn(plot[category], RooFit::LineColor(kRed),RooFit::LineWidth(3));

      //signal integral
      RooAbsReal* i_sig;
      if ( category%3==0 ) 
          i_sig = sigpdf[category]->createIntegral(RooArgSet(*m3m), RooArgSet(*m3m), "SIG_A");  
      if ( category%3==1 ) 
          i_sig = sigpdf[category]->createIntegral(RooArgSet(*m3m), RooArgSet(*m3m), "SIG_B");  
      if ( category%3==2 ) 
          i_sig = sigpdf[category]->createIntegral(RooArgSet(*m3m), RooArgSet(*m3m), "SIG_C");  
      //plot data 
      if (category%3==0) dataToPlot[category]->plotOn(plot[category],RooFit::MarkerColor(kBlack),RooFit::MarkerStyle(8),RooFit::MarkerSize(1),RooFit::LineWidth(3), Binning(38, 1.620000, 2.00000));
      if (category%3==1) dataToPlot[category]->plotOn(plot[category],RooFit::MarkerColor(kBlack),RooFit::MarkerStyle(8),RooFit::MarkerSize(1),RooFit::LineWidth(3), Binning(38, 1.620000, 2.00000));
      if (category%3==2) dataToPlot[category]->plotOn(plot[category],RooFit::MarkerColor(kBlack),RooFit::MarkerStyle(8),RooFit::MarkerSize(1),RooFit::LineWidth(3), Binning(38, 1.620000, 2.00000));
      if(blind){
          //plot pdf in sidebands
          if ( category%3==0 ) bkgpdf[category]->plotOn(plot[category], Range("SB1_A,SB2_A"), RooFit::NormRange("SB1_A,SB2_A"), RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==1 ) bkgpdf[category]->plotOn(plot[category], Range("SB1_B,SB2_B"), RooFit::NormRange("SB1_B,SB2_B"), RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==2 ) bkgpdf[category]->plotOn(plot[category], Range("SB1_C,SB2_C"), RooFit::NormRange("SB1_C,SB2_C"), RooFit::LineColor(kBlue), RooFit::LineWidth(3));

          if(MultiPdf){
            if ( category%3==0 ) bkgpdf2[category]->plotOn(plot[category], Range("SB1_A,SB2_A"),RooFit::NormRange("SB1_A,SB2_A"), RooFit::LineColor(kBlue),RooFit::LineWidth(3));
            if ( category%3==1 ) bkgpdf2[category]->plotOn(plot[category], Range("SB1_B,SB2_B"),RooFit::NormRange("SB1_B,SB2_B"), RooFit::LineColor(kBlue),RooFit::LineWidth(3));
            if ( category%3==2 ) bkgpdf2[category]->plotOn(plot[category], Range("SB1_C,SB2_C"),RooFit::NormRange("SB1_B,SB2_B"), RooFit::LineColor(kBlue),RooFit::LineWidth(3));
          }
      }else{
          //plot pdf in full range
          if ( category%3==0 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==1 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==2 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));

          if(MultiPdf){
            if ( category%3==0 ) bkgpdf2[category]->plotOn(plot[category], RooFit::LineColor(kBlue),RooFit::LineWidth(3));
            if ( category%3==1 ) bkgpdf2[category]->plotOn(plot[category], RooFit::LineColor(kBlue),RooFit::LineWidth(3));
            if ( category%3==2 ) bkgpdf2[category]->plotOn(plot[category], RooFit::LineColor(kBlue),RooFit::LineWidth(3));
          }
      }
      //background integral
      RooAbsReal* i_bkg;
      RooAbsReal* i_bkg_sb;
      if ( category%3==0 ) {
          i_bkg = bkgpdf[category]->createIntegral(RooArgSet(*m3m), RooArgSet(*m3m), "SIG_A");  
          i_bkg_sb = bkgpdf[category]->createIntegral(RooArgSet(*m3m), RooArgSet(*m3m), "SB1_A,SB2_A");  
      }
      if ( category%3==1 ) {
          i_bkg = bkgpdf[category]->createIntegral(RooArgSet(*m3m), RooArgSet(*m3m), "SIG_B");  
          i_bkg_sb = bkgpdf[category]->createIntegral(RooArgSet(*m3m), RooArgSet(*m3m), "SB1_B,SB2_B");  
      }
      if ( category%3==2 ) {
          i_bkg = bkgpdf[category]->createIntegral(RooArgSet(*m3m), RooArgSet(*m3m), "SIG_C");  
          i_bkg_sb = bkgpdf[category]->createIntegral(RooArgSet(*m3m), RooArgSet(*m3m), "SB1_B,SB2_B");  
      }
      cout<<category<<" Expected signal yield "<<i_sig->getVal()*signalAll[category]->sumEntries()<<endl;
      cout<<category<<" i_bkg->getVal() "<<i_bkg->getVal()<<endl;
      cout<<category<<" i_bkg_sb->getVal() "<<i_bkg_sb->getVal()<<endl;
      cout<<category<<" dataAll[category]->sumEntries() "<<dataAll[category]->sumEntries()<<endl;
      cout<<category<<" Expected bkg yield based on SB"<<i_bkg->getVal()*dataAll[category]->sumEntries() / i_bkg_sb->getVal()<<endl;
      outFile << TString::Format("%s",cat_names.at(category).c_str())<<"\t"<<i_sig->getVal()*signalAll[category]->sumEntries()<<"\t"<<i_bkg->getVal()*dataAll[category]->sumEntries() / i_bkg_sb->getVal()<<endl;

      //bkgpdf[category]->paramOn( plot[category], Format("NELU", AutoPrecision(2)),ShowConstants(), Layout(0.4,0.99,0.9));
      plot[category]->SetTitle(TString::Format("Category %s",cat_names.at(category).c_str()));     
      plot[category]->SetMinimum(0.01);
      plot[category]->SetMaximum(1.40*plot[category]->GetMaximum());
      plot[category]->GetXaxis()->SetTitle("m_{3mu} [GeV]");

      cout<<"chi2 bkg category: "<<cat_names.at(category).c_str()<<" "<<plot[category]->chiSquare()<<endl;

      TCanvas* ctmp_sig = new TCanvas(TString::Format("Category %s",cat_names.at(category).c_str()),"Categories",0,0,660,660);
      ctmp_sig->SetFrameLineWidth(3);
      ctmp_sig->SetTickx();
      ctmp_sig->SetTicky();
      plot[category]->Draw();
      plot[category]->Print();
      plot[category]->Draw("SAME");

      TLegend *legmc = new TLegend(0.50,0.70,0.86,0.86);
      legmc->AddEntry(plot[category]->getObject(0),"MC Signal (B=10^{-7})","LPE");
      legmc->AddEntry(plot[category]->getObject(1),"Signal Model","L");
      legmc->AddEntry(plot[category]->getObject(2),"Data","LPE");
      legmc->AddEntry(plot[category]->getObject(3),"EXP","L");
      if(MultiPdf) legmc->AddEntry(plot[category]->getObject(5),"PowerLaw","L");

      legmc->SetBorderSize(0);
      legmc->SetFillStyle(0);
      legmc->SetTextSize(0.029);

      legmc->Draw();  
      ctmp_sig->SaveAs("plots/"+TString::Format("Category_%s",cat_names.at(category).c_str())+configs+".png");
   }
   outFile.close();
}


void
MakePlotsSgn(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, string configs){

   RooDataSet* signalAll[NCAT];
   RooAbsPdf* sigpdf[NCAT];
   TFile f("signal_shapes.root","recreate");
   for(unsigned int category=0; category< NCAT; category++){
      signalAll[category] = (RooDataSet*) w->data(TString::Format("Sig_%s",cat_names.at(category).c_str()));
      sigpdf[category] = (RooAbsPdf*)w->pdf("SignalModel"+TString::Format("_%s",cat_names.at(category).c_str()));
   }

   RooRealVar* m3m     = w->var("m3m");  

   m3m->setUnit("GeV");
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
      sigpdf[category]->paramOn( plot_sgn[category], Format("NEU", RooFit::AutoPrecision(3)), ShowConstants(), Layout(0.55,0.9,0.9));
      plot_sgn[category]->getAttText()->SetTextSize(0.025);

      plot_sgn[category]->SetTitle(TString::Format("Category %s",cat_names.at(category).c_str()));     
      plot_sgn[category]->SetMinimum(0.01);
      plot_sgn[category]->SetMaximum(1.40*plot_sgn[category]->GetMaximum());
      plot_sgn[category]->GetXaxis()->SetTitle("m_{3mu} [GeV]");

      TCanvas* ctmp_sig = new TCanvas(TString::Format("Category %s",cat_names.at(category).c_str()),"Categories",0,0,660,660);
      ctmp_sig->SetFrameLineWidth(3);
      ctmp_sig->SetTickx();
      ctmp_sig->SetTicky();
      plot_sgn[category]->Draw();
      plot_sgn[category]->Print();
      plot_sgn[category]->Draw("SAME");
      TLegend *legmc = new TLegend(0.12,0.70,0.43,0.86);

      legmc->AddEntry(plot_sgn[category]->getObject(0),"MC Signal (B=10^{-7})","LPE");
      legmc->AddEntry(plot_sgn[category]->getObject(1),"Signal Model","L");
      
      cout<<"chi2 signal category: "<<cat_names.at(category).c_str()<<" "<<plot_sgn[category]->chiSquare()<<endl;
      //add Lumi and Chi2 to plot
      Double_t Chi2 = plot_sgn[category]->chiSquare();
      std::stringstream stream_chi2;
      stream_chi2 << std::fixed << std::setprecision(2) << Chi2;
      std::string strChi2 = stream_chi2.str();
      TString chi2tstring = "\\chi^{2}\\text{/NDOF} = "+strChi2;
      TLatex* text_chi2 = new TLatex(0.55,0.5, chi2tstring);
      text_chi2->SetTextSize(0.04);
      text_chi2->SetNDC(kTRUE);
      text_chi2->Draw("same");

      legmc->SetBorderSize(0);
      legmc->SetFillStyle(0);
      legmc->SetTextSize(0.029);

      legmc->Draw();  
      ctmp_sig->SaveAs("plots/"+TString::Format("Signal_%s",cat_names.at(category).c_str())+configs+".png");
      ctmp_sig->Write();
   }
   f.Close();
}

void 
AddData(TString file, RooWorkspace* w, const Int_t NCAT, std::vector<string> branch_names, std::vector<string> cat_names, std::vector<string> bdt_val){

   //outputTree,tripletMass,bdt,category,isMC,weight
   TString tree_name = branch_names.at(0);
   TString m3m_name = branch_names.at(1);
   TString bdt_name = branch_names.at(2);
   TString categ_name = branch_names.at(3);
   TString MClable_name = branch_names.at(4);
   TString weight_name = branch_names.at(5);

   //build strings for bdt cut selection
   vector<TString> bdt_cuts; // reserved to handle bdt cuts (full selection string)
   for (unsigned int category=0; category < NCAT; category++){
       if(category<3)
           bdt_cuts.push_back( TString::Format("%s>%s", bdt_name.Data(), bdt_val.at(category).c_str()) );
       else
           bdt_cuts.push_back( TString::Format("%s<=%s && %s>%s", bdt_name.Data(), bdt_val.at(category-3).c_str(), bdt_name.Data(), bdt_val.at(category).c_str()) );
   }

   TFile *f = new TFile(file,"READ");
   TTree *tree = (TTree *) f->Get(tree_name);

   RooRealVar m3m(m3m_name, m3m_name, 1.62, 2.0);
   RooRealVar bdt(bdt_name, bdt_name, -2, 2);
   RooRealVar categ(categ_name, categ_name, 0, 2);//mass resolution category 0=A, 1=B, 2=C
   RooRealVar isMC(MClable_name, MClable_name, 0, 4); //0=data, 1=Ds, 2=B0, 3=Bp, 4=W
   RooRealVar weight(weight_name, weight_name, 0, 1); //normalisation of MC including corrections i.e. PU reweighting

   RooArgSet variables(m3m);
   variables.add(bdt);
   variables.add(categ);
   variables.add(isMC);
   variables.add(weight);

   TString name, bdtcut, category_cut;

   for(unsigned int category=0; category< NCAT; category++){
      name = TString::Format("Sig_%s",cat_names.at(category).c_str());
      bdtcut = bdt_cuts.at(category);
      TString mc_cut = MClable_name+">0";

      cout<<"Importing signal "<<name<<" bdt selection "<<bdtcut<<endl;      
      for(int i = 0; i < 3; i++) {
          if(category%3==i) 
              category_cut = categ_name+"=="+std::to_string(i);
      }
      std::cout<<"-------------------------- "<< category_cut <<  "---------- "<< bdtcut<< std::endl;
      RooDataSet sigds(name, name, variables, Import(*tree), Cut("("+mc_cut+"&&"+category_cut+"&&"+bdtcut+")"), WeightVar(weight_name));
      sigds.Print();
      w->import(sigds,Rename(name),RooFit::RenameVariable(m3m_name,"m3m"));
   }
   for(unsigned int category=0; category< NCAT; category++){
      name = TString::Format("Bkg_%s",cat_names.at(category).c_str());
      bdtcut = bdt_cuts.at(category);
      TString mc_cut = MClable_name+"==0";

      cout<<"Importing background "<<name<<" bdt selection "<<bdtcut<<endl;      
      for(int i = 0; i < 3; i++) {
          if(category%3==i) 
              category_cut = categ_name+"=="+std::to_string(i);
      }
      RooDataSet bkgds(name, name, variables, Import(*tree), Cut("("+mc_cut+"&&"+category_cut+"&&"+bdtcut+")"));
      bkgds.Print();
      w->import(bkgds,Rename(name),RooFit::RenameVariable(m3m_name,"m3m"));
   }
   f->Close();
}

void 
BkgModelFit(RooWorkspace* w, const Int_t NCAT, std::vector<string>, RooFitResult** bkg_fitresults, bool blind, std::vector<string> cat_names){

   RooDataSet* dataAll[NCAT];
   RooDataSet* dataToFit[NCAT];
   RooAbsPdf* pdfBkgExp[NCAT];
   RooAbsPdf* BkgModel[NCAT];
   RooAbsPdf* bkg_powerlawpdf[NCAT];

   RooRealVar* exp_offset[NCAT];

   RooRealVar* m3m     = w->var("m3m");  
   TCut sidebands;

   m3m->setUnit("GeV");
   m3m->setRange("SB1_A",1.62,1.75);
   m3m->setRange("SB2_A",1.80,2.0);
   m3m->setRange("SB1_B",1.62,1.74);
   m3m->setRange("SB2_B",1.82,2.0);
   m3m->setRange("SB1_C",1.62,1.73);
   m3m->setRange("SB2_C",1.83,2.0);
   m3m->setRange("fullRange",1.62,2.0);

   for(unsigned int category=0; category< NCAT; category++)
   {
      dataAll[category]   = (RooDataSet*) w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str()));
      if (category%3==0)      sidebands = TCut("(m3m < 1.75 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.80)");
      else if (category%3==1) sidebands = TCut("(m3m < 1.74 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.82)");
      else if (category%3==2) sidebands = TCut("(m3m < 1.73 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.83)");

      //blind data
      if(blind) dataToFit[category] = (RooDataSet*)dataAll[category]->reduce(sidebands);
      else dataToFit[category] = (RooDataSet*)dataAll[category]->reduce("m3m > 1.62 && m3m < 2.0");
      dataToFit[category]->Print();

      pdfBkgExp[category]   =  (RooAbsPdf*)  w->pdf("t3m_bkg_expo"+TString::Format("_%s",cat_names.at(category).c_str()));

      //parameters before fitting
      exp_offset[category] = w->var(TString::Format("bkg_exp_offset_%s",cat_names.at(category).c_str())) ;

      BkgModel[category] = new RooAddPdf(TString::Format("BkgModel_fit_%s",cat_names.at(category).c_str()),"expo",RooArgList(*pdfBkgExp[category]), RooArgList(*exp_offset[category]));
      //fit SB1, SB2, combined
      if(blind){
          if ( category%3==0 )
              bkg_fitresults[category] = BkgModel[category]->fitTo(*dataToFit[category], Range("SB1_A,SB2_A"), Save()) ;
          if ( category%3==1 )
              bkg_fitresults[category] = BkgModel[category]->fitTo(*dataToFit[category], Range("SB1_B,SB2_B"), Save()) ;
          if ( category%3==2 )
              bkg_fitresults[category] = BkgModel[category]->fitTo(*dataToFit[category], Range("SB1_C,SB2_C"), Save()) ;
          }
      else bkg_fitresults[category]=BkgModel[category]->fitTo(*dataToFit[category],  Range("fullRange"), Save());

      bkg_powerlawpdf[category] = new RooGenericPdf(TString::Format("bkg_powerlawpdf_%s",cat_names.at(category).c_str()), "pow(@0, @1)", 
						    RooArgList(*w->var("m3m"), 
							       *w->var(TString::Format("bkg_powerlaw_slope_%s",cat_names.at(category).c_str()))));  

      bkg_fitresults[category]=bkg_powerlawpdf[category]->fitTo(*dataToFit[category], Strategy(2), Minos(kFALSE), SumW2Error(kTRUE), Save(kTRUE),RooFit::PrintEvalErrors(-1));

      w->import(*BkgModel[category]);
      w->import(*pdfBkgExp[category]);
      w->import(*bkg_powerlawpdf[category]);
   }
}


void 
MakeSigWS(RooWorkspace* w, const Int_t NCAT, const char* fileBaseName,  std::vector<string> cat_names) {

   TString wsDir   = "workspaces/";
   RooWorkspace *wAll = new RooWorkspace("w_all","w_all");
   RooAbsPdf* SigPdf[NCAT];
   cout << "-----------------------------------Write signal workspace in: " <<std::endl;

   for(unsigned int category=0; category < NCAT; category++){

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
MakeBkgWS(RooWorkspace* w, const Int_t NCAT, const char* fileBaseName, std::vector<string> cat_names) {
   TString wsDir   = "workspaces/";

   bool blind_WP = false;
   TCut sidebands;

   RooWorkspace *wAll = new RooWorkspace("w_all","w_all");
   RooDataSet* dataAll[NCAT];
   RooDataSet* dataToWp[NCAT];
   RooExtendPdf* bkg_fitPdf[NCAT];

   for(unsigned int category=0; category < NCAT; category++){

      if (category%3==0)      sidebands = TCut("(m3m < 1.75 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.80)");
      else if (category%3==1) sidebands = TCut("(m3m < 1.74 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.82)");
      else if (category%3==2) sidebands = TCut("(m3m < 1.73 && m3m > 1.62) || (m3m < 2.0 && m3m > 1.83)");

      dataAll[category] = (RooDataSet*) w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str()));
      //blind data
      if(blind_WP) dataToWp[category] = (RooDataSet*)dataAll[category]->reduce(sidebands);
      else dataToWp[category] = (RooDataSet*)dataAll[category]->reduce("m3m > 1.62 && m3m < 2.0");

      wAll->import(*dataToWp[category],Rename(TString::Format("data_obs_%s",cat_names.at(category).c_str())));
      wAll->import(*w->pdf(TString::Format("t3m_bkg_expo_%s",cat_names.at(category).c_str())));
      wAll->import(*w->pdf(TString::Format("bkg_powerlawpdf_%s",cat_names.at(category).c_str())));
      //wAll->import(*w->data(TString::Format("Bkg_%s",cat_names.at(category).c_str())));
   }
   TString filename(wsDir+TString(fileBaseName)+".root");
   wAll->writeToFile(filename);

   return;
}





void MakeDataCard(RooWorkspace* w, const Int_t NCAT, const char* fileBaseName, const char* fileBkgName, string configFile,  std::vector<string> cat_names, TString type, TString Run, bool blind){

   TString cardDir = "datacards/";
   TString wsDir   = "../workspaces/";

   RooDataSet* data[NCAT];
   RooDataSet* signal[NCAT];

   for (int c = 0; c < NCAT; ++c) {
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
      outFile << Form("shapes bkg %s ", cat_names.at(c).c_str())   << wsDir+TString(fileBkgName)+".root " << Form("w_all:t3m_bkg_expo_%s",cat_names.at(c).c_str()) << endl;
      outFile << Form("shapes signal %s ", cat_names.at(c).c_str()) << wsDir+TString(fileBaseName)+".root " << Form("w_all:SignalModel_%s",cat_names.at(c).c_str()) << endl;

      outFile << "---------------" << endl;
      outFile << Form("bin            %s  ", cat_names.at(c).c_str()) << endl;
      if(blind) outFile << "observation   -1" << endl;
      else      outFile << "observation   "  <<  data[c]->sumEntries() << endl;
      outFile << "------------------------------" << endl;

      outFile << Form("bin               %s        %s     ",cat_names.at(c).c_str(),cat_names.at(c).c_str())<<  endl;
      outFile << "process              signal     bkg     " << endl;
      outFile << "process                0          1      " << endl;
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
         outFile << "UncTrigger_13TeV  lnN  1.08      - " << endl; 
         outFile << "UncBDTCut_13TeV   lnN  1.05      - " << endl;
         outFile << "UncRatioAcc_13TeV lnN  1.01      - " << endl;
         if(type=="threeGlobal"){
             outFile << "UncMuonEff_13TeV  lnN  1.016     - " << endl;
             outFile << "UncMVAshape_13TeV  lnN  1.10     - " <<endl;
         }else{
             outFile << "UncMuonEff_13TeV  lnN  1.08     - " << endl; //TrackerNotGlobal SF
             outFile << "UncMVAshape_13TeV  lnN  1.10     - " <<endl;
         }
      }

      if (Run.Contains("2017")){
         //    outFile << "MuES_13TeV        lnN  1.007     - " << endl;
         //    outFile << "MuRes_13TeV       lnN  1.025     - " << endl;
         outFile << "DsNorm_13TeV      lnN  1.062      - " <<endl;
         outFile << "BRDToTau_13TeV    lnN  1.03      - " <<endl;
         outFile << "BRDsPhiPi_13TeV   lnN  1.08      - " <<endl;
         outFile << "BRBtoD_13TeV      lnN  1.05      - " <<endl;
         outFile << "BRBtoTau_13TeV    lnN  1.03      - " <<endl;
         outFile << "fUnc_13TeV        lnN  1.07      - " <<endl; // updated on 13 April
         outFile << "DpmScaling_13TeV  lnN  1.03      - " <<endl;
         outFile << "BsScaling_13TeV   lnN  1.04      - " <<endl;
         outFile << "UncTrigger_13TeV  lnN  1.11      - " <<endl;
         outFile << "UncBDTCut_13TeV   lnN  1.05      - " <<endl;
         outFile << "UncRatioAcc_13TeV lnN  1.01      - " <<endl;
         if(type=="threeGlobal"){
             outFile << "UncMuonEff_13TeV  lnN  1.015     - " << endl;
             outFile << "UncMVAshape_13TeV  lnN  1.10     - " <<endl;
         }else{
             outFile << "UncMuonEff_13TeV  lnN  1.04     - " << endl; //TrackerNotGlobal SF
             outFile << "UncMVAshape_13TeV  lnN  1.10     - " <<endl;
         }
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

void tokenize(std::string const &str, const char delim,
            std::vector<std::string> &out)
{
    size_t start;
    size_t end = 0;

    while ((start = str.find_first_not_of(delim, end)) != std::string::npos)
    {
        end = str.find(delim, start);
        out.push_back(str.substr(start, end - start));
    }
}
