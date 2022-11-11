#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"

#include "DataFormats/L1Trigger/interface/TkJetWord.h"
#include "DataFormats/L1Trigger/interface/VertexWord.h"

#include <cmath>

namespace l1t {
  P2GTCandidate::P2GTCandidate() {}

  P2GTCandidate::P2GTCandidate(const VertexWord& obj)
      : hwDZ_(obj.z0Word().V.to_int()),
        hwQual_(obj.qualityWord().V.to_int()),
        hwSum_pT_pv_(obj.multiplicityWord().V.to_int()),
        hwNumber_of_tracks_in_pv_(obj.multiplicityWord().V.to_int()),
        hwNumber_of_tracks_not_in_pv_(obj.inverseMultiplicityWord().V.to_int()) {}

  P2GTCandidate::P2GTCandidate(const TkJetWord& obj)
      : hwPT_(obj.ptWord().V.to_int()),
        hwPhi_(obj.glbPhiWord().V.to_int()),
        hwEta_(obj.glbEtaWord().V.to_int()),
        hwDZ_(obj.z0Word().V.to_int()),
        hwNumber_of_tracks_(obj.ntWord().V.to_int()) {}

  bool P2GTCandidate::operator==(const P2GTCandidate& rhs) const {
    return hwPT_ == rhs.hwPT_ && hwPhi_ == rhs.hwPhi_ && hwEta_ == rhs.hwEta_ && hwDZ_ == rhs.hwDZ_ &&
           hwIso_ == rhs.hwIso_ && hwQual_ == rhs.hwQual_ && hwCharge_ == rhs.hwCharge_ && hwDD_ == rhs.hwDD_ &&
           hwBeta_ == rhs.hwBeta_ && hwMass_ == rhs.hwMass_ && hwIndex_ == rhs.hwIndex_ &&
           hwSeed_pT_ == rhs.hwSeed_pT_ && hwSeed_dZ_ == rhs.hwSeed_dZ_ && hwSca_sum_ == rhs.hwSca_sum_ &&
           hwPrimvertdz_ == rhs.hwPrimvertdz_ && hwNumber_of_tracks_ == rhs.hwNumber_of_tracks_ &&
           hwSum_pT_pv_ == rhs.hwSum_pT_pv_ && hwType_ == rhs.hwType_ &&
           hwNumber_of_tracks_in_pv_ == rhs.hwNumber_of_tracks_in_pv_ &&
           hwNumber_of_tracks_not_in_pv_ == rhs.hwNumber_of_tracks_not_in_pv_;
  }

  bool P2GTCandidate::operator!=(const P2GTCandidate& rhs) const {
    return hwPT_ != rhs.hwPT_ && hwPhi_ != rhs.hwPhi_ && hwEta_ != rhs.hwEta_ && hwDZ_ != rhs.hwDZ_ &&
           hwIso_ != rhs.hwIso_ && hwQual_ != rhs.hwQual_ && hwCharge_ != rhs.hwCharge_ && hwDD_ != rhs.hwDD_ &&
           hwBeta_ != rhs.hwBeta_ && hwMass_ != rhs.hwMass_ && hwIndex_ != rhs.hwIndex_ &&
           hwSeed_pT_ != rhs.hwSeed_pT_ && hwSeed_dZ_ != rhs.hwSeed_dZ_ && hwSca_sum_ != rhs.hwSca_sum_ &&
           hwPrimvertdz_ != rhs.hwPrimvertdz_ && hwNumber_of_tracks_ != rhs.hwNumber_of_tracks_ &&
           hwSum_pT_pv_ != rhs.hwSum_pT_pv_ && hwType_ != rhs.hwType_ &&
           hwNumber_of_tracks_in_pv_ != rhs.hwNumber_of_tracks_in_pv_ &&
           hwNumber_of_tracks_not_in_pv_ != rhs.hwNumber_of_tracks_not_in_pv_;
  };
}  // namespace l1t
