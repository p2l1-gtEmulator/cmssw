#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"

#include "DataFormats/L1Trigger/interface/TkJetWord.h"
#include "DataFormats/L1Trigger/interface/VertexWord.h"

#include "DataFormats/L1TMuonPhase2/interface/SAMuon.h"
#include "DataFormats/L1TMuonPhase2/interface/TrackerMuon.h"

#include "DataFormats/L1TParticleFlow/interface/PFJet.h"
#include "DataFormats/L1TCorrelator/interface/TkEm.h"
#include "DataFormats/L1TCorrelator/interface/TkElectron.h"

#include "DataFormats/L1TParticleFlow/interface/gt_datatypes.h"
#include "DataFormats/L1TParticleFlow/interface/egamma.h"

namespace l1t {
  P2GTCandidate::P2GTCandidate() {}

  P2GTCandidate::P2GTCandidate(const VertexWord& obj)
      : hwZ0_(obj.z0Word().V.to_int()),
        hwQual_(obj.qualityWord().V.to_int()),
        hwSum_pT_pv_(obj.multiplicityWord().V.to_int()),
        hwNumber_of_tracks_in_pv_(obj.multiplicityWord().V.to_int()),
        hwNumber_of_tracks_not_in_pv_(obj.inverseMultiplicityWord().V.to_int()) {}

  P2GTCandidate::P2GTCandidate(const TkJetWord& obj)
      : hwPT_(obj.ptWord().V.to_int()),
        hwPhi_(obj.glbPhiWord().V.to_int()),
        hwEta_(obj.glbEtaWord().V.to_int()),
        hwZ0_(obj.z0Word().V.to_int()),
        hwNumber_of_tracks_(obj.ntWord().V.to_int()) {}

  P2GTCandidate::P2GTCandidate(const SAMuon& obj)
      : hwPT_(obj.hwPt()),
        hwPhi_(obj.hwPhi()),
        hwEta_(obj.hwEta()),
        hwZ0_(obj.hwZ0()),
        hwQual_(obj.hwQual()),
        hwCharge_(obj.hwCharge()),
        hwD0_(obj.hwD0()) {}

  P2GTCandidate::P2GTCandidate(const TrackerMuon& obj)
      : hwPT_(obj.hwPt()),
        hwPhi_(obj.hwPhi()),
        hwEta_(obj.hwEta()),
        hwZ0_(obj.hwZ0()),
        hwIso_(obj.hwIso()),
        hwQual_(obj.hwQual()),
        hwCharge_(obj.hwCharge()),
        hwD0_(obj.hwD0()),
        hwBeta_(obj.hwBeta()) {}

  P2GTCandidate P2GTCandidate::initPFJet(const PFJet& edmJet) {
    l1gt::Jet gtJet = l1gt::Jet::unpack(const_cast<PFJet&>(edmJet).encodedJet());
    P2GTCandidate gtCandiate;
    gtCandiate.hwPT_ = gtJet.v3.pt.V.to_int();
    gtCandiate.hwPhi_ = gtJet.v3.phi.V.to_int();
    gtCandiate.hwEta_ = gtJet.v3.eta.V.to_int();
    gtCandiate.hwZ0_ = gtJet.z0.V.to_int();

    return gtCandiate;
  }

  P2GTCandidate P2GTCandidate::initTkEm(const TkEm& edmTkEm) {
    l1gt::Photon gtPhoton = l1ct::EGIsoObj::unpack(const_cast<TkEm&>(edmTkEm).egBinaryWord<96>()).toGT();
    P2GTCandidate gtCandiate;
    gtCandiate.hwPT_ = gtPhoton.v3.pt.V.to_int();
    gtCandiate.hwPhi_ = gtPhoton.v3.phi.V.to_int();
    gtCandiate.hwEta_ = gtPhoton.v3.eta.V.to_int();
    gtCandiate.hwIso_ = gtPhoton.isolation.V.to_int();
    gtCandiate.hwQual_ = gtPhoton.quality.V.to_int();

    return gtCandiate;
  }

  P2GTCandidate P2GTCandidate::initTkElectron(const TkElectron& edmTkElectron) {
    l1gt::Electron gtElectron =
        l1ct::EGIsoEleObj::unpack(const_cast<TkElectron&>(edmTkElectron).egBinaryWord<96>()).toGT();
    P2GTCandidate gtCandiate;
    gtCandiate.hwPT_ = gtElectron.v3.pt.V.to_int();
    gtCandiate.hwPhi_ = gtElectron.v3.phi.V.to_int();
    gtCandiate.hwEta_ = gtElectron.v3.eta.V.to_int();
    gtCandiate.hwZ0_ = gtElectron.z0.V.to_int();
    gtCandiate.hwIso_ = gtElectron.isolation.V.to_int();
    gtCandiate.hwQual_ = gtElectron.quality.V.to_int();
    gtCandiate.hwCharge_ = gtElectron.charge.V.to_int();

    return gtCandiate;
  }

  P2GTCandidate::P2GTCandidate(const PFJet& obj) : P2GTCandidate(initPFJet(obj)) {}
  P2GTCandidate::P2GTCandidate(const TkEm& obj) : P2GTCandidate(initTkEm(obj)) {}
  P2GTCandidate::P2GTCandidate(const TkElectron& obj) : P2GTCandidate(initTkElectron(obj)) {}

  bool P2GTCandidate::operator==(const P2GTCandidate& rhs) const {
    return hwPT_ == rhs.hwPT_ && hwPhi_ == rhs.hwPhi_ && hwEta_ == rhs.hwEta_ && hwZ0_ == rhs.hwZ0_ &&
           hwIso_ == rhs.hwIso_ && hwQual_ == rhs.hwQual_ && hwCharge_ == rhs.hwCharge_ && hwD0_ == rhs.hwD0_ &&
           hwBeta_ == rhs.hwBeta_ && hwMass_ == rhs.hwMass_ && hwIndex_ == rhs.hwIndex_ &&
           hwSeed_pT_ == rhs.hwSeed_pT_ && hwSeed_z0_ == rhs.hwSeed_z0_ && hwSca_sum_ == rhs.hwSca_sum_ &&
           hwPrimvertdz_ == rhs.hwPrimvertdz_ && hwNumber_of_tracks_ == rhs.hwNumber_of_tracks_ &&
           hwSum_pT_pv_ == rhs.hwSum_pT_pv_ && hwType_ == rhs.hwType_ &&
           hwNumber_of_tracks_in_pv_ == rhs.hwNumber_of_tracks_in_pv_ &&
           hwNumber_of_tracks_not_in_pv_ == rhs.hwNumber_of_tracks_not_in_pv_;
  }

  bool P2GTCandidate::operator!=(const P2GTCandidate& rhs) const {
    return hwPT_ != rhs.hwPT_ && hwPhi_ != rhs.hwPhi_ && hwEta_ != rhs.hwEta_ && hwZ0_ != rhs.hwZ0_ &&
           hwIso_ != rhs.hwIso_ && hwQual_ != rhs.hwQual_ && hwCharge_ != rhs.hwCharge_ && hwD0_ != rhs.hwD0_ &&
           hwBeta_ != rhs.hwBeta_ && hwMass_ != rhs.hwMass_ && hwIndex_ != rhs.hwIndex_ &&
           hwSeed_pT_ != rhs.hwSeed_pT_ && hwSeed_z0_ != rhs.hwSeed_z0_ && hwSca_sum_ != rhs.hwSca_sum_ &&
           hwPrimvertdz_ != rhs.hwPrimvertdz_ && hwNumber_of_tracks_ != rhs.hwNumber_of_tracks_ &&
           hwSum_pT_pv_ != rhs.hwSum_pT_pv_ && hwType_ != rhs.hwType_ &&
           hwNumber_of_tracks_in_pv_ != rhs.hwNumber_of_tracks_in_pv_ &&
           hwNumber_of_tracks_not_in_pv_ != rhs.hwNumber_of_tracks_not_in_pv_;
  };
}  // namespace l1t
