#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"

#include <cmath>

namespace l1t {
  P2GTCandidate::P2GTCandidate() {}

  P2GTCandidate::P2GTCandidate(const TkElectron& obj)
      : hwPT_(std::round(obj.pt() / 0.03125) /* TEMPORARY */), hwPhi_(obj.hwPhi()), hwEta_(obj.hwEta()) /* TODO */ {}

  P2GTCandidate::P2GTCandidate(const TkEm& obj)
      : hwPT_(std::round(obj.pt() / 0.03125) /* TEMPORARY */), hwPhi_(obj.hwPhi()), hwEta_(obj.hwEta()) /* TODO */ {}

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
