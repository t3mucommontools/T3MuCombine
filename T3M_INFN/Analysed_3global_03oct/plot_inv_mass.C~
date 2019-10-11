#include "TH1F.h"
#include <cmath>


void plot_inv_mass() 
{
    TString cat[6] = {"A1", "A2", "B1", "B2", "C1", "C2"};
    double SigYield_2016[6] = {6.3, 10.4, 4.0, 19.2, 8.9, 9.0};
    double BkgYield_2016[6] = {360, 2502, 110, 2229, 389, 1549};
    cout<<"Opening data file"<<endl;
    TFile *f = new TFile("AnalysedTree_3global_data_2017_tau3mu_03oct.root","READ");
    cout<<"Opened data file"<<endl;
    TH1F *h_tripletmass;    
    TH1F *h_tripletmass_total;    
    //h_tripletmass_total = (TH1F*)f->Get("AfterCuts/h_FinalInvMass_");
    TCanvas *c1 = new TCanvas("c1","c1",150,10,990,660);
    TFile *fAll = new TFile("datacardT3MuAllCat.root","recreate");
    /*
    for(int i=0; i<20; i++){
       float value = 1.73 + i*0.005;
       h_tripletmass_total->SetBinContent( h_tripletmass_total->FindBin(value), 0 );
       }*/

    //h_tripletmass_total->Draw();
    cout<<"Opening signal file"<<endl;
    TFile *f2 = new TFile("AnalysedTree_3global_MC_AllSignals_tau3mu_03oct.root","READ");
    TH1F *h_tripletmass_MC;

    for (int k =0; k<6; k++){
    h_tripletmass = (TH1F*)f->Get("AfterCuts/h_FinalInvMass_"+cat[k]);
    h_tripletmass_MC = (TH1F*)f2->Get("AfterCuts/h_FinalInvMass_"+cat[k]);

    TCanvas *c2 = new TCanvas("c2","c2",150,10,990,660);
    Double_t normMC = h_tripletmass_MC->GetEntries();
    //Normalizing Monte Carlo 

    //Number of Ds from data
    Double_t N_Ds = 85629;    
    //Double_t xsection_mc = 1.09e7; //average on 6 files
    Double_t fB = 0.23;

    //Integrated Luminosity collected in 2017
    //Double_t Lumi_data = 38;  //total fb-1

    //Branching ratio B -> tau
    Double_t BR1 = 0.027;
    //Branching ratio B -> Ds
    Double_t BR2 = 0.016;
    //Branching ratio tau -> mu (theory)
    Double_t BR3mu = 1E-7;
    //Total number of events in the MC sample
    //int N_MC = 151424;
    //    int N_MC = 3002413 + 2005362;
    float selEff = 0.03;
    int N_MC =1;
    int zoom = 1;
    Double_t wNorm = selEff*fB * N_Ds * (BR1/(0.08* BR2)) * BR3mu / N_MC * zoom;
    double xsMC =21800000000;
    double lumi = 38;
    Double_t wNormMC = 0.0014;
    cout<<"wNomr "<<wNorm<<endl;
    //h_tripletmass_MC->Scale(wNorm);
    cout<<cat[k]<<endl;
    cout<<"Bkg Integral="<<h_tripletmass->Integral()<<endl;
    cout<<"Sig Integral="<<h_tripletmass_MC->Integral()<<endl;

    h_tripletmass_MC->Scale(wNormMC);   
    //h_tripletmass->Scale(BkgYield_2016[k]/h_tripletmass->Integral());   


    //plot makeup
    gStyle->SetLineWidth(2);
    //h_tripletmass_MC->SetFillColor(kBlue);
    //h_tripletmass_MC->SetFillStyle(3154);
    h_tripletmass_MC->SetLineColor(kBlue);
    h_tripletmass_MC->GetYaxis()->SetTitle("a.u.");

    //h_tripletmass->SetFillColor(kRed);
    //h_tripletmass->SetFillStyle(3145);
    h_tripletmass->SetLineColor(kRed);

    //blinding data
    /*
    for(int i=0; i<20; i++){
       float value = 1.73 + i*0.005;
        h_tripletmass->SetBinContent( h_tripletmass->FindBin(value), 0 );
	}*/

    h_tripletmass->Draw("histe");
    h_tripletmass_MC->Draw("histesame");

    cout<<"Bkg Integral="<<h_tripletmass->Integral()<<endl;
    cout<<"Sig Integral="<<h_tripletmass_MC->Integral()<<endl;


    TLegend*leg = new TLegend(0.1,0.35,0.48,0.55);
    leg->AddEntry(h_tripletmass_MC,"MC","f");
    leg->AddEntry(h_tripletmass,"data, cat."+cat[k],"f");
    leg->Draw();
    c2->Update();

    TFile *fOut = new TFile("datacardT3Mu_"+cat[k]+".root","recreate");
    h_tripletmass->Write("background");
    h_tripletmass->Write("data_obs");
    h_tripletmass_MC->Write("signal");

    //blinding data                                                                                                                                                         
                                                                                                                                                                     
    for(int i=0; i<20; i++){                                                                                                                                                
      float value = 1.73 + i*0.005;                                                                                                                                        
      h_tripletmass->SetBinContent( h_tripletmass->FindBin(value), 0 );                                                                                                   
    }

    fAll->cd();
    h_tripletmass->Write("background"+cat[k]);
    h_tripletmass->Write("data_obs"+cat[k]);
    h_tripletmass_MC->Write("signal"+cat[k]);

    c2->SaveAs("InvariantMass_cat"+cat[k]+".png");
}
}
