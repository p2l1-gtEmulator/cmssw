#ifndef L1GTCollection_h
#define L1GTCollection_h

#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"

#include "L1Trigger/Phase2L1GT/interface/L1GTScales.h"

#include "L1GTOptionalParam.h"

#include <optional>

namespace l1t {

  class L1GTSingleCollectionCut {
  public:
    L1GTSingleCollectionCut(const edm::ParameterSet& config, const L1GTScales& scales)
        : tag_(config.getParameter<edm::InputTag>("tag")),
          minPt_(getOptionalParam<int, double>(
              "minPt", config, std::bind(&L1GTScales::to_hw_pT, scales, std::placeholders::_1))),
          minEta_(getOptionalParam<int, double>(
              "minEta", config, std::bind(&L1GTScales::to_hw_eta, scales, std::placeholders::_1))),
          maxEta_(getOptionalParam<int, double>(
              "maxEta", config, std::bind(&L1GTScales::to_hw_eta, scales, std::placeholders::_1))),
          minPhi_(getOptionalParam<int, double>(
              "minPhi", config, std::bind(&L1GTScales::to_hw_phi, scales, std::placeholders::_1))),
          maxPhi_(getOptionalParam<int, double>(
              "maxPhi", config, std::bind(&L1GTScales::to_hw_phi, scales, std::placeholders::_1))),
          minDz_(getOptionalParam<int, double>(
              "minDz", config, std::bind(&L1GTScales::to_hw_dZ, scales, std::placeholders::_1))),
          maxDz_(getOptionalParam<int, double>(
              "maxDz", config, std::bind(&L1GTScales::to_hw_dZ, scales, std::placeholders::_1))),
          qual_(getOptionalParam<unsigned int>("qual", config)),
          iso_(getOptionalParam<unsigned int>("iso", config)) {}

    bool checkObject(const P2GTCandidate& obj) const {
      bool result = true;

      result &= minPt_ ? (obj.hwPT() > minPt_) : true;

      result &= minEta_ ? (obj.hwEta() > minEta_) : true;
      result &= maxEta_ ? (obj.hwEta() < maxEta_) : true;

      result &= minPhi_ ? (obj.hwPhi() > minPhi_) : true;
      result &= maxPhi_ ? (obj.hwPhi() < maxPhi_) : true;

      result &= minDz_ ? (obj.hwDZ() > minDz_) : true;
      result &= maxDz_ ? (obj.hwDZ() < maxDz_) : true;

      result &= qual_ ? (obj.hwQual() == qual_) : true;
      result &= iso_ ? (obj.hwIso() == iso_) : true;

      return result;
    }

    static void fillDescriptions(edm::ParameterSetDescription& desc) {
      desc.add<edm::InputTag>("tag");
      desc.addOptional<double>("minPt");
      desc.addOptional<double>("minEta");
      desc.addOptional<double>("maxEta");
      desc.addOptional<double>("minPhi");
      desc.addOptional<double>("maxPhi");
      desc.addOptional<double>("minDz");
      desc.addOptional<double>("maxDz");
      desc.addOptional<unsigned int>("qual");
      desc.addOptional<unsigned int>("iso");
    }

    const edm::InputTag& tag() const { return tag_; }

  private:
    const edm::InputTag tag_;
    const std::optional<int> minPt_;
    const std::optional<int> minEta_;
    const std::optional<int> maxEta_;
    const std::optional<int> minPhi_;
    const std::optional<int> maxPhi_;
    const std::optional<int> minDz_;
    const std::optional<int> maxDz_;
    const std::optional<int> qual_;
    const std::optional<int> iso_;
  };

}  // namespace l1t

#endif  // L1GTCollection_h
