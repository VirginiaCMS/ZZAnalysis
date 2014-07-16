/** \class EleFiller
 *
 *  No description available.
 *
 *  $Date: 2013/05/24 15:42:42 $
 *  $Revision: 1.28 $
 *  \author N. Amapane (Torino)
 *  \author S. Bolognesi (JHU)
 *  \author C. Botta (CERN)
 *  \author S. Casasso (Torino)
 */

#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDProducer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <FWCore/Framework/interface/ESHandle.h>

//#include <DataFormats/PatCandidates/interface/Electron.h>
#include <EGamma/EGammaAnalysisTools/interface/ElectronEffectiveArea.h>
//#include "DataFormats/VertexReco/interface/Vertex.h"

#include <ZZAnalysis/AnalysisStep/interface/CutSet.h>
#include <ZZAnalysis/AnalysisStep/interface/LeptonIsoHelper.h>
//#include "BDTId.h"

#include <vector>
#include <string>

using namespace edm;
using namespace std;
using namespace reco;


//bool recomputeBDT = false;

class EleFiller : public edm::EDProducer {
 public:
  /// Constructor
  explicit EleFiller(const edm::ParameterSet&);
    
  /// Destructor
  ~EleFiller(){
    //delete bdt;
  };  

 private:
  virtual void beginJob(){};  
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob(){};

  const edm::InputTag theCandidateTag;
  int sampleType;
  int setup;
  const StringCutObjectSelector<pat::Electron, true> cut;
  const CutSet<pat::Electron> flags;
  //BDTId* bdt;
};


EleFiller::EleFiller(const edm::ParameterSet& iConfig) :
  theCandidateTag(iConfig.getParameter<InputTag>("src")),
  sampleType(iConfig.getParameter<int>("sampleType")),
  setup(iConfig.getParameter<int>("setup")),
  cut(iConfig.getParameter<std::string>("cut")),
  flags(iConfig.getParameter<ParameterSet>("flags"))//, 
  //bdt(0)
{
  //if (recomputeBDT) bdt = new BDTId;
  produces<pat::ElectronCollection>();
}


void
EleFiller::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{  

  // Get leptons and rho
  edm::Handle<pat::ElectronRefVector> electronHandle;
  iEvent.getByLabel(theCandidateTag, electronHandle);

  InputTag theRhoTag = LeptonIsoHelper::getEleRhoTag(sampleType,setup);
  edm::Handle<double> rhoHandle;
  iEvent.getByLabel(theRhoTag, rhoHandle); 
  double rho = *rhoHandle;

  edm::Handle<vector<Vertex> >  vertexs;
  iEvent.getByLabel("goodPrimaryVertices",vertexs);

  // Output collection
  auto_ptr<pat::ElectronCollection> result( new pat::ElectronCollection() );

  //FIXME: effective areas to be updated!
  const float AreaEcal[2]    = {0.101, 0.046};   //   barrel/endcap
  const float AreaHcal[2]    = {0.021, 0.040};   //   barrel/endcap

  for (unsigned int i = 0; i< electronHandle->size(); ++i){
    //---Clone the pat::Electron
    pat::Electron l(*((*electronHandle)[i].get()));

    //--- Rho-corrected isolation and loose iso
    float tkIso   = l.userIsolation(pat::User1Iso);
    float ecalIso = l.dr03EcalRecHitSumEt();
    float hcalIso = l.dr03HcalTowerSumEt();

    Int_t ifid = 1;
    if (l.isEB()) ifid = 0;
    ecalIso = ecalIso - AreaEcal[ifid]*rho;
    hcalIso = hcalIso - AreaHcal[ifid]*rho;
    
    float combRelIso = (ecalIso + hcalIso + tkIso)/l.pt();

    //--- PF ISO
    float PFChargedHadIso   = l.chargedHadronIso();
    float PFNeutralHadIso   = l.neutralHadronIso();
    float PFPhotonIso       = l.photonIso();

    //float fSCeta = fabs(l.eta()); 
    float fSCeta = fabs(l.superCluster()->eta());

    float combRelIsoPF = LeptonIsoHelper::combRelIsoPF(sampleType, setup, rho, l);

    //--- SIP, dxy, dz
    float IP      = fabs(l.dB(pat::Electron::PV3D));
    float IPError = l.edB(pat::Electron::PV3D);
    float SIP     = IP/IPError;

    float dxy = 999.;
    float dz  = 999.;
    const Vertex* vertex = 0;
    if (vertexs->size()>0) {
      vertex = &(vertexs->front());
      dxy = fabs(l.gsfTrack()->dxy(vertex->position()));
      dz  = fabs(l.gsfTrack()->dz(vertex->position()));
    } 

    
    // BDT value from PAT prodiuction
    float BDT = 0;
    //if (recomputeBDT) {
    //  BDT = bdt->compute(l);
    //} else {
    //BDT = l.electronID("mvaNonTrigV0");//RH
    //}
    

    float pt = l.pt();
    bool isBDT = (pt <= 10 && (( fSCeta < 0.8 && BDT > 0.47)  ||
			       (fSCeta >= 0.8 && fSCeta < 1.479 && BDT > 0.004) ||
			       (fSCeta >= 1.479               && BDT > 0.295))) || 
                 //Moriond13 eID cuts updated for the paper
		 //(pt >  10 && ((fSCeta < 0.8 && BDT > 0.5)  ||
		 //	       (fSCeta >= 0.8 && fSCeta < 1.479 && BDT > 0.12) || 
                 (pt >  10 && ((fSCeta < 0.8 && BDT > -0.34)  ||
			       (fSCeta >= 0.8 && fSCeta < 1.479 && BDT > -0.65) || 
			       (fSCeta >= 1.479               && BDT > 0.6)));


// Forget mva ISO for the time being.
//     float mvaIsoRings = l.userFloat("mvaIsoRings");
//     bool isMvaIsoRings = false;
    
//     //"reference WP" from https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMultivariateIsoElectrons#Reference_Working_Point r10
//     if ((pt < 10 && fSCeta < 0.8                   && mvaIsoRings >  0.385) ||
// 	(pt < 10 && fSCeta >= 0.8 && fSCeta < 1.479  && mvaIsoRings > -0.083) ||
// 	(pt < 10 && fSCeta > 1.479                 && mvaIsoRings > -0.573) ||
// 	(pt >= 10 && fSCeta < 0.8                  && mvaIsoRings >  0.413) ||
// 	(pt >= 10 && fSCeta >= 0.8 && fSCeta < 1.479 && mvaIsoRings >  0.271) ||
// 	(pt >= 10 && fSCeta > 1.479                && mvaIsoRings >  0.135)) {
//       isMvaIsoRings = true;      
//      }
    
	//-- Missing hit  
	int missingHit = l.gsfTrack()->trackerExpectedHitsInner().numberOfHits();
    //--- Trigger matching
    int HLTMatch = 0; //FIXME
    
    //--- Embed user variables
    l.addUserFloat("looseIso",tkIso/l.pt());
    l.addUserFloat("combRelIso",combRelIso);
    l.addUserFloat("PFChargedHadIso",PFChargedHadIso);
    l.addUserFloat("PFNeutralHadIso",PFNeutralHadIso);
    l.addUserFloat("PFPhotonIso",PFPhotonIso);
    l.addUserFloat("combRelIsoPF",combRelIsoPF);
    l.addUserFloat("rho",rho);
//    l.addUserFloat("isMvaIsoRings", isMvaIsoRings);
    l.addUserFloat("SIP",SIP);
    l.addUserFloat("dxy",dxy);
    l.addUserFloat("dz",dz);
    l.addUserFloat("BDT",BDT);    
    l.addUserFloat("isBDT",isBDT);
    l.addUserFloat("HLTMatch", HLTMatch);
	l.addUserFloat("missingHit", missingHit);

    //--- MC parent code 
//     MCHistoryTools mch(iEvent);
//     if (mch.isMC()) {
//       int MCParentCode = 0;
//       //      int MCParentCode = mch.getParentCode(&l); //FIXME: does not work on cmg
//       l.addUserFloat("MCParentCode",MCParentCode);
//     }

    //--- Check selection cut. Being done here, flags are not available; but this way we 
    //    avoid wasting time on rejected leptons.
    if (!cut(l)) continue;

    //--- Embed flags (ie flags specified in the "flags" pset)
    for(CutSet<pat::Electron>::const_iterator flag = flags.begin(); flag != flags.end(); ++flag) {
      l.addUserFloat(flag->first,int((*(flag->second))(l)));
    }

    result->push_back(l);
  }
  iEvent.put(result);
}


#include <FWCore/Framework/interface/MakerMacros.h>
DEFINE_FWK_MODULE(EleFiller);

