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

void AddData(TString, TString, RooWorkspace*, const Int_t NCAT, std::vector<string> branch_names, std::vector<string> cat_names, std::vector<string> bdt_val);
void SigModelFit(RooWorkspace*, const Int_t NCAT, std::vector<string>, RooFitResult** signal_fitresults, TString type, TString Run);
void BkgModelFit(RooWorkspace*, const Int_t NCAT, std::vector<string>, RooFitResult** bkg_fitresults, bool blind, std::vector<string> cat_names, TString m3m_name, bool dp, TString type, TString Run);
void MakeSigWS(RooWorkspace* w, const Int_t NCAT, const char* filename,  std::vector<string>);
void MakeBkgWS(RooWorkspace* w, const Int_t NCAT, const char* filename,  std::vector<string>, bool dp, TString type, TString Run);
void MakeDataCard(RooWorkspace* w, const Int_t NCAT, const char* fileBaseName, const char* fileBkgName, string configFile,  std::vector<string> cat_names, TString type, TString Run, bool blind, bool dp);
void MakePlots(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, bool dp, bool blind, string configs, TString type, TString Run);
void MakePlotsSplusB(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, bool dp, bool blind, string configs, TString type, TString Run);
void MakePlotsSgn(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, string configs);

void SetConstantParams(const RooArgSet* params);
void tokenize(std::string const &str, const char delim, std::vector<std::string> &out);

void
createDataCards(TString inputfile, int signalsample = 0, bool blind = true, string modelCard="model_card.rs", string configFile="config.txt", TString type="threeGlobal", TString Run="2017", bool dp = true, bool doscan = false)
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

   TString m3m_name = branch_names.at(1);

   TString signalname("T3MSignal");
   TString bkgname("T3MBkg");

   string configFile_prefix =  configFile.erase(configFile.size() - 4);
   if(!doscan) configFile_prefix = "";

   TString  fileBaseName("CMS_"+signalname + configFile_prefix + "_13TeV");
   TString  fileBkgName("CMS_"+bkgname + configFile_prefix + "_13TeV");

   TString card_name(modelCard);
   HLFactory hlf("HLFactory", card_name, false);
   RooWorkspace* w = hlf.GetWs();
   RooFitResult* bkg_fitresults[NCAT];
   RooFitResult* signal_fitresults[NCAT];
   w->var("m3m")->setMin(MMIN);
   w->var("m3m")->setMax(MMAX);

   //w->Print();
   AddData(inputfile, Run, w,NCAT,branch_names,cat_names,bdt_val);

   SigModelFit(w, NCAT, cat_names, signal_fitresults, type, Run);
   MakeSigWS(w, NCAT, fileBaseName, cat_names);

   BkgModelFit(w, NCAT, cat_names, bkg_fitresults, blind, cat_names, m3m_name, dp, type, Run);
   MakeBkgWS(w, NCAT, fileBkgName, cat_names, dp, type, Run);

   MakeDataCard(w, NCAT, fileBaseName, fileBkgName, configFile_prefix, cat_names, type, Run, blind, dp);

   TString filename("temp_workspace.root");
   w->writeToFile(filename);
   MakePlots(w,NCAT,cat_names, dp, blind, configFile_prefix, type, Run);
   //MakePlotsSplusB(w,NCAT,cat_names, dp, blind,configFile_prefix, type, Run);
   MakePlotsSgn(w,NCAT,cat_names,configFile_prefix);

   w->Print();

   return;

}


void
SigModelFit(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, RooFitResult** signal_fitresults, TString type, TString Run) {

   RooAbsPdf* pdfSigCB[NCAT];
   RooAbsPdf* pdfSigGS[NCAT];
   RooAddPdf* SignalModel[NCAT];

   RooRealVar* sig_f[NCAT];
   RooRealVar* f_cb[NCAT];

   RooRealVar* sig_sigma[NCAT];
   RooRealVar* sig_gaus_sigma[NCAT];

   RooRealVar* sigma[NCAT];
   RooRealVar* sigma_gaus[NCAT];

   Float_t minMassFit(MMIN),maxMassFit(MMAX); 

   RooRealVar* m3m = w->var("m3m");  

   m3m->setUnit("GeV");
   m3m->setRange("signal",1.69,1.86);
   m3m->setRange("fullRange",1.62,2.0);

   //A,B,C
   TString cat_reso[] = {"A", "B", "C"};
   for(int cr = 0; cr < 3; cr++) {
      std::cout<<">>> mass resolution category  "<< cat_reso[cr] << std::endl;
      //Define roofit categories for simultaneous fit	
      std::map<std::string, RooDataSet*> samplemap;
      RooCategory c("c", "c");
      for (unsigned int category=0; category < NCAT; category++){
          std::string cat_name = cat_names.at(category).c_str();
          if(cat_name.rfind(cat_reso[cr], 0) == 0){ //A1,A2,A3
              //define category
              c.defineType(cat_name.c_str());
              //map category - dataset
              samplemap[cat_name] = (RooDataSet*)  w->data(TString::Format("Sig_%s",cat_name.c_str()));
          }
      }

      RooDataSet combData("combData", "combined data", *m3m, Index(c), Import(samplemap));

      // Construct a simultaneous pdf using category "c" as index
      RooSimultaneous simPdf("simPdf", "simultaneous pdf", c);

      //parameters in common
      RooRealVar* sig_m0         = w->var("sig_m0_"+cat_reso[cr]);
      RooRealVar* sig_alpha      = w->var("sig_alpha_"+cat_reso[cr]);
      RooRealVar* sig_n          = w->var("sig_n_"+cat_reso[cr]);

      for (unsigned int category=0; category < NCAT; category++){
          std::string cat_name = cat_names.at(category).c_str();
          TString tcat_name = cat_names.at(category).c_str();
          if(cat_name.rfind(cat_reso[cr], 0) == 0){ //A1,A2,A3
              //parameters and pdf per subcategory
              pdfSigCB[category] = (RooAbsPdf*)   w->pdf("t3m_sig_CBshape_"+tcat_name+"_"+type);
              pdfSigGS[category] = (RooAbsPdf*)   w->pdf("t3m_sig_GSshape_"+tcat_name+"_"+type);

              sig_f[category]          = w->var("cb_fraction_"+tcat_name);
              sig_sigma[category]      = w->var("sig_sigma_"+tcat_name);
              sig_gaus_sigma[category] = w->var("sig_gaus_sigma_"+tcat_name);

              SignalModel[category] = new RooAddPdf(TString::Format("SignalModel_fit_%s", cat_name.c_str()),"g+c",RooArgList(*pdfSigCB[category], *pdfSigGS[category]), *sig_f[category]);
          }
      }

      // Associate model with the categories
      for (unsigned int category=0; category < NCAT; category++){
          std::string cat_name = cat_names.at(category).c_str();
          if(cat_name.rfind(cat_reso[cr], 0) == 0){ //A1,A2,A3
              //simPdf.addPdf(*SignalModel[cr], cat_name.c_str());
              simPdf.addPdf(*SignalModel[category], cat_name.c_str());
          }
      }

      //SignalModel is fitted to data for each mass resolution category separately
      // ---------------------------------------------------
      // P e r f o r m   a   s i m u l t a n e o u s   f i t
      RooFitResult * r = simPdf.fitTo(combData, Save(true));
      cout<<"Fit results"<<endl;
      r->floatParsFinal().Print("s");

      //retrieving parameters from fitted shape

      // fix all the parameters expect for the nomralisation of signal
      TString name_mean       = "m0_"+cat_reso[cr];
      TString name_alpha_cb   = "alpha_cb_"+cat_reso[cr];
      TString name_n_cb       = "n_cb_"+cat_reso[cr];

      RooRealVar mean    (name_mean,"mean", sig_m0->getVal(), sig_m0->getVal(), sig_m0->getVal() );
      RooRealVar alpha_cb (name_alpha_cb,"alpha_cb",sig_alpha->getVal(), sig_alpha->getVal(), sig_alpha->getVal());
      RooRealVar n_cb (name_n_cb,"n_cb",sig_n->getVal(), sig_n->getVal(), sig_n->getVal());

      mean.setError(sig_m0->getError());
      alpha_cb.setError(sig_alpha->getError());
      n_cb.setError(sig_n->getError());

      for (unsigned int category=0; category < NCAT; category++){
          std::string cat_name = cat_names.at(category).c_str();
          if(cat_name.rfind(cat_reso[cr], 0) == 0){ //A1,A2,A3
              //fraction can change depending on subcategory
              TString name_f_cb   = TString::Format("f_cb_%s", cat_name.c_str());
              f_cb[category] = new RooRealVar (name_f_cb,"f_cb",sig_f[category]->getVal(), sig_f[category]->getVal(), sig_f[category]->getVal());
              f_cb[category]->setError(sig_f[category]->getError());

              //sigmas can change depending on subcategory
              TString name_sigma  = TString::Format("sigma_%s", cat_name.c_str());
              sigma[category] = new RooRealVar(name_sigma,"sigma",sig_sigma[category]->getVal(), sig_sigma[category]->getVal(), sig_sigma[category]->getVal());              
              sigma[category]->setError(sig_sigma[category]->getError());

              TString name_sigma_gaus = TString::Format("sigma_gaus_%s", cat_name.c_str());
              sigma_gaus[category] = new RooRealVar(name_sigma_gaus,"sigma_gaus",sig_gaus_sigma[category]->getVal(), sig_gaus_sigma[category]->getVal(), sig_gaus_sigma[category]->getVal());              
              sigma_gaus[category]->setError(sig_gaus_sigma[category]->getError());
          }
      }

      for (unsigned int category=0; category < NCAT; category++){
          std::string cat_name = cat_names.at(category).c_str();
          TString tcat_name = cat_names.at(category).c_str();
          if(cat_name.rfind(cat_reso[cr], 0) == 0){ //A1,A2,A3

              //Apply correction to the fixed mass      
              RooRealVar UncMean("UncMean", "UncMean", 0., -5, 5);
              // According to ANv2 L798, "mean" is 0.09% smaller in data. So we scale MC mean by 0.9991, and assign 0.0009 uncertainty
              TString line = "(1+0.0009*UncMean)*" + std::to_string(sig_m0->getVal()*0.9991); 
              RooFormulaVar fmean("fmean_"+tcat_name,line,RooArgList(UncMean));

              //Apply correction to the fixed sigmas
              RooRealVar UncSigma("UncSigma", "UncSigma", 0., -5, 5);
              // According to Fig47, MC has up to 2% worse resolution! We don't scale the MC resolution, but only assign 2% uncertainty
              TString line2 = "(1+0.02*UncSigma)*" + std::to_string(sigma[category]->getVal()); 
              RooFormulaVar fsigma("fsigma_"+tcat_name,line2,RooArgList(UncSigma));

              //Define pdf for each subcategory
              //RooCBShape  CB_final("CB_final_"+tcat_name+"_"+type+"_"+Run,"CB PDF",*m3m,mean,*sigma[category],alpha_cb,n_cb) ;
              //RooGaussian GS_final("GS_final_"+tcat_name+"_"+type+"_"+Run,"GS PDF",*m3m,mean,*sigma_gaus[category]) ;
              //RooAddPdf signal("SignalModel_"+tcat_name,"",RooArgList(CB_final,GS_final), *f_cb[category]);
              
              // then recreate the signal shape using the 2 RooFormulaVar and the other 4 parameters
              RooCBShape CB_final("CB_final_"+tcat_name+"_"+type+"_"+Run,"CB PDF",*m3m,fmean,fsigma,alpha_cb,n_cb) ;
              RooGaussian GS_final("GS_final_"+tcat_name+"_"+type+"_"+Run,"GS PDF",*m3m,fmean,*sigma_gaus[category]) ;
              RooAddPdf signal("SignalModel_"+tcat_name,"",RooArgList(CB_final,GS_final), *f_cb[category]);

              w->defineSet("SigPdfParam_"+tcat_name, RooArgSet(
                       //mean, //*w->var("sig_m0_"+cat_reso[cr]+subc),
                       //*sigma[category], //*w->var("sig_sigma_"+cat_reso[cr]+subc),
                       *sigma_gaus[category], //*w->var("sig_gaus_sigma_"+cat_reso[cr]+subc),
                       alpha_cb, //*w->var("sig_alpha_"+cat_reso[cr]+subc),
                       n_cb, //*w->var("sig_n_"+cat_reso[cr]+subc),
                       *f_cb[category] //*w->var("sig_f_"+cat_reso[cr]+subc)
              ), true); 
              SetConstantParams(w->set("SigPdfParam_"+tcat_name));

             //add mean and sigma to named set
              w->import(mean);
              w->import(*sigma[category]);
              w->extendSet("SigPdfParam_"+tcat_name, "m0_"+cat_reso[cr]);
              w->extendSet("SigPdfParam_"+tcat_name, "sigma_"+tcat_name);

              w->import(signal);
          }
       }
   }
   //for debugging
   std::cout<<"WP after signal fit"<<std::endl;
   w->Print();
}

void
MakePlotsSplusB(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, bool dp, bool blind, string configs, TString type, TString Run){

   RooDataSet* signalAll[NCAT];
   RooDataSet* dataAll[NCAT];
   RooDataSet* dataToPlot[NCAT];
   RooAbsPdf* sigpdf[NCAT];
   RooAbsPdf* bkgpdf[NCAT];

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
      if(dp){
          RooMultiPdf* multipdf = (RooMultiPdf*) w->pdf(TString::Format("multipdf_%s",cat_names.at(category).c_str()));
          bkgpdf[category] =(RooAbsPdf*)multipdf->getCurrentPdf();
      }
      else bkgpdf[category] =(RooAbsPdf*)w->pdf(TString::Format("t3m_bkg_expo_"+type+"_"+Run+"_%s",cat_names.at(category).c_str()));
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
      }else{
          //plot pdf in full range
          if ( category%3==0 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==1 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==2 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));
      }

      //plot signal+bkg
      RooRealVar bkgfrac("bkgfrac", "fraction of background", 0.9, 0., 1.);
      RooAddPdf model("model", "s+b", RooArgList(*bkgpdf[category], *sigpdf[category]), bkgfrac);
      model.fitTo(*dataToPlot[category], RooFit::Extended());
      model.plotOn(plot[category], RooFit::LineColor(kGreen), RooFit::LineWidth(3));

      //bkgpdf[category]->paramOn( plot[category], Format("NELU", AutoPrecision(2)),ShowConstants(), Layout(0.4,0.99,0.9));
      plot[category]->SetTitle(TString::Format("Category %s",cat_names.at(category).c_str()));     
      plot[category]->SetMinimum(0.00);
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
      legmc->AddEntry(plot[category]->getObject(3),"Bkg Model","L");

      legmc->SetBorderSize(0);
      legmc->SetFillStyle(0);
      legmc->SetTextSize(0.029);

      legmc->Draw();  
      ctmp_sig->SaveAs("plots/"+TString::Format("Category_%s_SplusB",cat_names.at(category).c_str())+".png");
   }
}



void
MakePlots(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, bool dp, bool blind, string configs, TString type, TString Run){

   RooDataSet* signalAll[NCAT];
   RooDataSet* dataAll[NCAT];
   RooDataSet* dataToPlot[NCAT];
   RooAbsPdf* sigpdf[NCAT];
   RooAbsPdf* bkgpdf[NCAT];

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
      if(dp) {
          RooMultiPdf* multipdf = (RooMultiPdf*) w->pdf(TString::Format("multipdf_%s",cat_names.at(category).c_str()));
          bkgpdf[category] =(RooAbsPdf*)multipdf->getCurrentPdf();
      }
      else bkgpdf[category] =(RooAbsPdf*)w->pdf(TString::Format("t3m_bkg_expo_"+type+"_"+Run+"_%s",cat_names.at(category).c_str()));
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
      
   TString filename(type+"_"+Run+"_yields.txt");
   //TString filename("yields.txt");
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
      }else{
          //plot pdf in full range
          if ( category%3==0 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==1 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));
          if ( category%3==2 ) bkgpdf[category]->plotOn(plot[category], RooFit::LineColor(kBlue), RooFit::LineWidth(3));
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
      plot[category]->SetMinimum(0.00);
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
      legmc->AddEntry(plot[category]->getObject(3),"Bkg Model","L");

      legmc->SetBorderSize(0);
      legmc->SetFillStyle(0);
      legmc->SetTextSize(0.029);

      legmc->Draw();  
      ctmp_sig->SaveAs("plots/"+TString::Format("Category_%s",cat_names.at(category).c_str())+".png");
   }
   outFile.close();
}


void
MakePlotsSgn(RooWorkspace* w, const Int_t NCAT, std::vector<string> cat_names, string configs){

   RooDataSet* signalAll[NCAT];
   RooAbsPdf* sigpdf[NCAT];
   RooArgSet* params[NCAT];

   TFile f("signal_shapes.root","recreate");
   for(unsigned int category=0; category< NCAT; category++){
      signalAll[category] = (RooDataSet*) w->data(TString::Format("Sig_%s",cat_names.at(category).c_str()));
      sigpdf[category] = (RooAbsPdf*)w->pdf("SignalModel"+TString::Format("_%s",cat_names.at(category).c_str()));
      params[category] = (RooArgSet*)w->set("SigPdfParam"+TString::Format("_%s",cat_names.at(category).c_str()));
      //TO DO: display mass and sigma on canvases
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
      signalAll[category]->plotOn( plot_sgn[category],RooFit::MarkerColor(kBlack),RooFit::MarkerStyle(6),RooFit::MarkerSize(0.75));
      //signalAll[category]->statOn( plot_sgn[category],Layout(0.65,0.99,0.9)) ;
      sigpdf[category]->plotOn( plot_sgn[category], RooFit::LineColor(kRed),RooFit::LineWidth(2));
      sigpdf[category]->paramOn( plot_sgn[category], RooFit::Parameters(*params[category]), Format("NEU", RooFit::AutoPrecision(2)), ShowConstants(true), Layout(0.45,0.9,0.9));
      plot_sgn[category]->getAttText()->SetTextSize(0.025);

      plot_sgn[category]->SetTitle(TString::Format("Category %s",cat_names.at(category).c_str()));     
      plot_sgn[category]->SetMinimum(0.0);
      plot_sgn[category]->SetMaximum(1.50*plot_sgn[category]->GetMaximum());
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


      //draw contour
      //need to retrieve fit results!
      //sigpdf[category]->plotOn( plot_sgn[category], RooFit::LineColor(kRed),RooFit::VisualizeError(results,2), RooFit::FillColor(kYellow),RooFit::FillStyle(3001)) ;
      //sigpdf[category]->plotOn( plot_sgn[category], RooFit::LineColor(kRed),RooFit::VisualizeError(results,2), RooFit::FillColor(kGreen), RooFit::FillStyle(3001)) ;
      
      ctmp_sig->SaveAs("plots/"+TString::Format("Signal_%s",cat_names.at(category).c_str())+".png");
      ctmp_sig->Write();
   }
   f.Close();
}

void 
AddData(TString file, TString era, RooWorkspace* w, const Int_t NCAT, std::vector<string> branch_names, std::vector<string> cat_names, std::vector<string> bdt_val){

   //outputTree,tripletMass,bdt,category,isMC,weight
   TString tree_name = branch_names.at(0);
   TString m3m_name = branch_names.at(1);
   TString bdt_name = branch_names.at(2);
   TString categ_name = branch_names.at(3);
   TString MClable_name = branch_names.at(4);
   TString weight_name = branch_names.at(5);

   //additional var pre-app comment
   TString dimu1_name = branch_names.at(6);
   TString dimu2_name = branch_names.at(7);
   TString omega_cut = "abs("+dimu1_name+"-0.782)>0.01 && abs("+dimu2_name+"-0.782)>0.01";

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
   RooRealVar weight(weight_name, weight_name, 0, 1); //normalisation of MC

   RooRealVar dimu1(dimu1_name, dimu1_name, 0.2, 1.8); //dimu_OS1
   RooRealVar dimu2(dimu2_name, dimu2_name, 0.2, 1.8); //dimu_OS2

   RooArgSet variables(m3m);
   variables.add(bdt);
   variables.add(categ);
   variables.add(isMC);
   variables.add(weight);

   variables.add(dimu1);
   variables.add(dimu2);

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
      RooDataSet sigds(name, name, variables, Import(*tree), Cut("("+mc_cut+"&&"+category_cut+"&&"+bdtcut+"&&"+omega_cut+")"), WeightVar(weight_name));
      sigds.Print();
      //reduce to only one variable
      RooDataSet* sigds_reduced = (RooDataSet*) sigds.reduce(RooArgSet(m3m));
      w->import(*sigds_reduced,Rename(name),RooFit::RenameVariable(m3m_name,"m3m"));
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
      RooDataSet bkgds(name, name, variables, Import(*tree), Cut("("+mc_cut+"&&"+category_cut+"&&"+bdtcut+"&&"+omega_cut+")"));
      bkgds.Print();
      //reduce to only one variable
      RooDataSet* bkgds_reduced = (RooDataSet*) bkgds.reduce(RooArgSet(m3m));
      w->import(*bkgds_reduced,Rename(name),RooFit::RenameVariable(m3m_name,"m3m"));
   }
   f->Close();
}

void 
BkgModelFit(RooWorkspace* w, const Int_t NCAT, std::vector<string>, RooFitResult** bkg_fitresults, bool blind, std::vector<string> cat_names, TString m3m_name, bool discpf, TString type, TString Run){

   RooDataSet* dataAll[NCAT];
   RooDataSet* dataToFit[NCAT];
   RooAbsPdf* pdfBkgExp[NCAT];
   RooAbsPdf* BkgModel[NCAT];

   RooRealVar* bkg_norm[NCAT];

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

      bkg_norm[category] = w->var(TString::Format("bkg_norm_%s",cat_names.at(category).c_str())) ;
      //define bkg model
      if(!discpf) {
          pdfBkgExp[category]   =  (RooAbsPdf*)  w->pdf(TString::Format("t3m_bkg_expo_"+type+"_"+Run+"_%s",cat_names.at(category).c_str()));
      }else{
          //open rootfile created by running discrete_profiling_HF.py
          TString dp_filepath = "../python/MultiPdfWorkspaces/"+Run+"_"+type+"_"+cat_names.at(category).c_str()+".root";
          cout<<"Bkg model from external wp "<<dp_filepath<<endl;
          TFile *f = new TFile(dp_filepath,"READ");
          RooWorkspace* wdf = (RooWorkspace*)f->Get("ospace");
          RooMultiPdf* multipdf = (RooMultiPdf*) wdf->pdf("multipdf")->Clone(TString::Format("multipdf_%s",cat_names.at(category).c_str()));
          w->import(*multipdf, RooFit::RenameVariable(m3m_name, "m3m")); //, Rename( TString::Format("multipdf_%s",cat_names.at(category).c_str()) ));
          //In this way you take the best fit pdf or the exponential, depending on what was done in discrete_profiling_HF.py
          pdfBkgExp[category] = (RooAbsPdf*) multipdf->getCurrentPdf(); //->Clone("t3m_bkg_dp_"+TString::Format("%s",cat_names.at(category).c_str()));
      }
      BkgModel[category] = new RooAddPdf(TString::Format("BkgModel_fit_%s",cat_names.at(category).c_str()),"expo",RooArgList(*pdfBkgExp[category]), RooArgList(*bkg_norm[category]));

      //fit SB1, SB2, combined
      if(blind){
          if ( category%3==0 )
              bkg_fitresults[category] = BkgModel[category]->fitTo(*dataToFit[category], Range("SB1_A,SB2_A"), Save(), Extended(true), SumW2Error(true), Verbose(true)) ;
          if ( category%3==1 )
              bkg_fitresults[category] = BkgModel[category]->fitTo(*dataToFit[category], Range("SB1_B,SB2_B"), Save(), Extended(true), SumW2Error(true), Verbose(true)) ;
          if ( category%3==2 )
              bkg_fitresults[category] = BkgModel[category]->fitTo(*dataToFit[category], Range("SB1_C,SB2_C"), Save(), Extended(true), SumW2Error(true), Verbose(true)) ;
          }
      else bkg_fitresults[category]=BkgModel[category]->fitTo(*dataToFit[category],  Range("fullRange"), Save(), Extended(true), SumW2Error(true));

      //Important! Should switch to "m3m" in discrete_profiling.py
      w->import(*BkgModel[category], RooFit::RenameVariable(m3m_name, "m3m"));
      w->Print();
   }
}


void 
MakeSigWS(RooWorkspace* w, const Int_t NCAT, const char* fileBaseName,  std::vector<string> cat_names) {

   TString wsDir   = "workspaces/";
   RooWorkspace *wAll = new RooWorkspace("w_all","w_all");
   RooAbsPdf* SigPdf[NCAT];
   cout << "-----------------------------------Write signal workspace--------------" <<std::endl;

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
MakeBkgWS(RooWorkspace* w, const Int_t NCAT, const char* fileBaseName, std::vector<string> cat_names, bool discpf, TString type, TString Run) {
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
      if(!discpf)
         wAll->import(*w->pdf(TString::Format("t3m_bkg_expo_"+type+"_"+Run+"_%s",cat_names.at(category).c_str())));
      else{
         //wAll->import(*w->pdf(TString::Format("t3m_bkg_dp_%s",cat_names.at(category).c_str())));
         wAll->import(*w->pdf(TString::Format("multipdf_%s",cat_names.at(category).c_str() )));
      }
   }
   TString filename(wsDir+TString(fileBaseName)+".root");
   wAll->writeToFile(filename);

   return;
}





void MakeDataCard(RooWorkspace* w, const Int_t NCAT, const char* fileBaseName, const char* fileBkgName, string configFile,  std::vector<string> cat_names, TString type, TString Run, bool blind, bool dp){

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
      if(dp) outFile << Form("shapes bkg %s ", cat_names.at(c).c_str())   << wsDir+TString(fileBkgName)+".root " << Form("w_all:multipdf_%s",cat_names.at(c).c_str()) << endl;
      // if(dp) outFile << Form("shapes bkg %s ", cat_names.at(c).c_str())   << wsDir+TString(fileBkgName)+".root " << Form("w_all:t3m_bkg_dp_%s",cat_names.at(c).c_str()) << endl;
      else outFile << Form("shapes bkg %s ", cat_names.at(c).c_str())   << wsDir+TString(fileBkgName)+".root " << Form("w_all:t3m_bkg_expo_"+type+"_"+Run+"_%s",cat_names.at(c).c_str()) << endl;
      outFile << Form("shapes sig %s ", cat_names.at(c).c_str()) << wsDir+TString(fileBaseName)+".root " << Form("w_all:SignalModel_%s",cat_names.at(c).c_str()) << endl;

      outFile << "---------------" << endl;
      outFile << Form("bin            %s  ", cat_names.at(c).c_str()) << endl;
      if(blind) outFile << "observation   -1" << endl;
      else      outFile << "observation   "  <<  data[c]->sumEntries() << endl;
      outFile << "------------------------------" << endl;

      outFile << Form("bin               %s        %s     ",cat_names.at(c).c_str(),cat_names.at(c).c_str())<<  endl;
      outFile << "process              sig     bkg     " << endl;
      outFile << "process                0          1      " << endl;
      outFile << "rate                "  << " " << signal[c]->sumEntries()*signalScaler << "    " <<  data[c]->sumEntries()  << endl;
      outFile << "--------------------------------" << endl;


      //Correlated uncertanties across categories and years
      //outFile << "lumi_13TeV       lnN  1.027      - " << endl;
      outFile << "ySig_dstn         lnN  1.03      - " << endl; //unc. on BR(Ds->taunu)
      outFile << "ySig_dsmmp        lnN  1.08      - " << endl; //unc. on BR(Ds->phi(mumu)pi)
      outFile << "ySig_bds          lnN  1.05      - " << endl; //unc. on BR(B->D+X)
      outFile << "ySig_bt           lnN  1.03      - " << endl; //unc. on BR(B->tau+X)   
      outFile << "ySig_dscal        lnN  1.03      - " << endl; //unc. on scaling Ds to include D+
      outFile << "ySig_bscal        lnN  1.04      - " << endl; //unc. on scaling B0 and B+ to include Bs

      //Uncorrelated uncertanties across years
      if (Run.Contains("2018")){ 
         outFile << "DsNorm_18      lnN  1.04      - " << endl; // normalisation factor computed on control channel
         outFile << "fUnc_18        lnN  1.02      - " << endl; // B/D ratio
         outFile << "UncHLT_18      lnN  1.05      - " << endl; // uncertanty on 2018 HLT
         outFile << "UncL1_18       lnN  1.02      - " << endl; // events triggered by TripleMu
         outFile << "UncBDTCut_18   lnN  1.05      - " << endl; //unc. on BDT selection
         outFile << "UncRatioAcc_18 lnN  1.01      - " << endl; //unc. on 3mu/2mu ratio acceptance
         outFile << "UncPionEff_18  lnN  1.021      - " << endl; //unc. on pion reconstruction efficiency

         //Uncorrelated uncertanties across categories
         if(type=="threeGlobal"){
             outFile << "WNorm_18_3glb       lnN  1.05      - " << endl; // 100% unc. on 5% additional W yield
             outFile << "UncMuonEff_18_3glb  lnN  1.016     - " << endl; //GlobalMu ID tag&probe
             outFile << "UncMVAshape_18_3glb  lnN  1.06     - " <<endl;  //MVAglb correction
         }else{
             outFile << "UncMuonEff_18_2glbtk  lnN  1.08     - " << endl; //TrackerNotGlobal ID tag&probe
             outFile << "UncMVAshape_18_2glbtk  lnN  1.04     - " <<endl; //MVAtk correction
         }
      }

      if (Run.Contains("2017")){
         outFile << "DsNorm_17      lnN  1.062      - " <<endl; //normalisation factor computed on control channel
         outFile << "fUnc_17        lnN  1.02      - " <<endl;  //B/D ratio
         outFile << "UncL1_17       lnN  1.05      - " <<endl;  //events triggered by TripleMu
         outFile << "UncBDTCut_17   lnN  1.05      - " <<endl;  //unc. on BDT selection
         outFile << "UncRatioAcc_17 lnN  1.01      - " <<endl;  //unc. on 3mu/2mu ratio acceptance
         outFile << "UncPionEff_17  lnN  1.022      - " << endl; //unc. on pion reconstruction efficiency

         //Uncorrelated uncertanties across categories
         if(type=="threeGlobal"){
             outFile << "WNorm_17_3glb       lnN  1.03      - " << endl; // 100% unc. on 5% additional W yield
             outFile << "UncMuonEff_17_3glb  lnN  1.015     - " << endl; //GlobalMu ID tag&probe
             outFile << "UncMVAshape_17_3glb  lnN  1.03     - " <<endl;  //MVAglb correction
         }else{
             outFile << "UncMuonEff_17_2glbtk  lnN  1.04     - " << endl; //TrackerNotGlobal ID tag&probe
             outFile << "UncMVAshape_17_2glbtk  lnN  1.04     - " <<endl; //MVAtk correction
         }
      }
//      outFile << Form("bkg_norm_%s rateParam %s bkg 1.", cat_names.at(c).c_str(), cat_names.at(c).c_str()) << endl;
      if(dp) {
          outFile << Form("roomultipdf_cat_"+Run+"_"+type+"_%s discrete", cat_names.at(c).c_str()) << endl;
      } else {
          outFile << Form("bkg_exp_slope_"+type+"_"+Run+"_%s flatParam", cat_names.at(c).c_str()) << endl;
      }
      outFile << "UncMean	param 	0.0	1.0	" << endl;
      outFile << "UncSigma	param 	0.0	1.0	" << endl;
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
