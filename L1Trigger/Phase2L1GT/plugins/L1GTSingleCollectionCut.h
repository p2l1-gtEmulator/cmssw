#ifndef L1Trigger_Phase2L1GT_L1GTSingleCollectionCut_h
#define L1Trigger_Phase2L1GT_L1GTSingleCollectionCut_h

#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"

#include "L1Trigger/Phase2L1GT/interface/L1GTScales.h"

#include "L1GTOptionalParam.h"
#include "L1GTSingleInOutLUT.h"

#include <algorithm>
#include <optional>

namespace l1t {

  class L1GTSingleCollectionCut {
  public:
    L1GTSingleCollectionCut(const edm::ParameterSet& config,
                            const edm::ParameterSet& lutConfig,
                            const L1GTScales& scales)
        : scales_(scales),
          tag_(config.getParameter<edm::InputTag>("tag")),
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
          minZ0_(getOptionalParam<int, double>(
              "minZ0", config, std::bind(&L1GTScales::to_hw_z0, scales, std::placeholders::_1))),
          maxZ0_(getOptionalParam<int, double>(
              "maxZ0", config, std::bind(&L1GTScales::to_hw_z0, scales, std::placeholders::_1))),
          minScalarSumPt_(getOptionalParam<int, double>(
              "minScalarSumPt", config, std::bind(&L1GTScales::to_hw_pT, scales, std::placeholders::_1))),
          qual_(config.exists("qual") ? config.getParameter<std::vector<unsigned int>>("qual")
                                      : std::vector<unsigned int>()),
          minEtaAbs_(getOptionalParam<int, double>(
              "minEtaAbs", config, std::bind(&L1GTScales::to_hw_eta, scales, std::placeholders::_1))),
          maxEtaAbs_(getOptionalParam<int, double>(
              "maxEtaAbs", config, std::bind(&L1GTScales::to_hw_eta, scales, std::placeholders::_1))),
          regionsAbsEtaLowerBounds_(config.exists("regionsAbsEtaLowerBounds")
                                        ? config.getParameter<std::vector<double>>("regionsAbsEtaLowerBounds")
                                        : std::vector<double>()),
          regionsQual_(config.exists("regionsQual") ? config.getParameter<std::vector<unsigned int>>("regionsQual")
                                                    : std::vector<unsigned int>()),
          regionsMaxIso_(config.exists("regionsMaxIso") ? config.getParameter<std::vector<double>>("regionsMaxIso")
                                                        : std::vector<double>()),
          regionsPt_(config.exists("regionsPt") ? config.getParameter<std::vector<double>>("regionsPt")
                                                 : std::vector<double>()),
          maxIso_(getOptionalParam<int, double>(
              "maxIso", config, std::bind(&L1GTScales::to_hw_isolation, scales, std::placeholders::_1))),
          oneOverIsoLUT_(lutConfig.getParameterSet("one_over_iso_lut")) {}

    bool checkEtaDependendcuts(const std::vector<double> etavec,
                               const std::vector<unsigned int> qualvec,
                               const std::vector<double> isovec,
                               const std::vector<double> ptvec,
                               const P2GTCandidate& obj) const {
      bool res = 1;

      unsigned int index;
      index = atIndex(etavec, obj.hwEta());
      res &= ptvec.empty() ? true : (obj.hwPT() > scales_.to_hw_pT(ptvec[index]));
      res &= isovec.empty()
                 ? true
                 : std::round(oneOverIsoLUT_.output_scale() * isovec[index]) < oneOverIsoLUT_[obj.hwIso()] * obj.hwPT();
      res &= qualvec.empty() ? true : checkForQualMask(qualvec[index], obj.hwQual().to_uint());
      return res;
    }

    bool checkForQualMask(const int value, const int mask) const {
      int masked_value = value & mask;
      if (masked_value == mask) {
        return 1;
      } else {
        return 0;
      }
    }

    unsigned int atIndex(const std::vector<double> absetarange, const int objeta) const {
      for (unsigned int i = 0; i < absetarange.size(); i++) {
        if (std::abs(objeta) >= scales_.to_hw_eta(absetarange[i]) &&
            std::abs(objeta) < scales_.to_hw_eta(absetarange[i + 1])) {
          return i;
        }
      }
      return absetarange.size() - 1;
    }

    bool checkObject(const P2GTCandidate& obj) const {
      bool result = true;

      result &= minPt_ ? (obj.hwPT() > minPt_) : true;

      result &= minEta_ ? (obj.hwEta() > minEta_) : true;
      result &= maxEta_ ? (obj.hwEta() < maxEta_) : true;

      result &= minPhi_ ? (obj.hwPhi() > minPhi_) : true;
      result &= maxPhi_ ? (obj.hwPhi() < maxPhi_) : true;

      result &= minZ0_ ? (obj.hwZ0() > minZ0_) : true;
      result &= maxZ0_ ? (obj.hwZ0() < maxZ0_) : true;

      result &= minEtaAbs_ ? (abs(obj.hwEta()) > minEtaAbs_) : true;
      result &= maxEtaAbs_ ? (abs(obj.hwEta()) < maxEtaAbs_) : true;

      result &= minScalarSumPt_ ? (obj.hwSca_sum() > minScalarSumPt_) : true;

      result &= qual_.empty() ? true : std::find(qual_.begin(), qual_.end(), obj.hwQual().to_uint()) != qual_.end();
      result &= maxIso_ ? std::round(oneOverIsoLUT_.output_scale() * maxIso_.value()) <
                              oneOverIsoLUT_[obj.hwIso()] * obj.hwPT()
                        : true;
      result &= regionsAbsEtaLowerBounds_.empty()
                    ? true
                    : checkEtaDependendcuts(regionsAbsEtaLowerBounds_, regionsQual_, regionsMaxIso_, regionsPt_, obj);
      return result;
    }

    static void fillDescriptions(edm::ParameterSetDescription& desc) {
      desc.add<edm::InputTag>("tag");
      desc.addOptional<double>("minPt");
      desc.addOptional<double>("minEta");
      desc.addOptional<double>("maxEta");
      desc.addOptional<double>("minPhi");
      desc.addOptional<double>("maxPhi");
      desc.addOptional<double>("minZ0");
      desc.addOptional<double>("maxZ0");
      desc.addOptional<double>("minScalarSumPt");
      desc.addOptional<std::vector<unsigned int>>("qual");
      desc.addOptional<double>("minEtaAbs");
      desc.addOptional<double>("maxEtaAbs");
      desc.addOptional<std::vector<double>>("regionsAbsEtaLowerBounds");
      desc.addOptional<std::vector<unsigned int>>("regionsQual");
      desc.addOptional<std::vector<double>>("regionsMaxIso");
      desc.addOptional<std::vector<double>>("regionsPt");
      desc.addOptional<double>("maxIso");
    }

    const edm::InputTag& tag() const { return tag_; }

  private:
    const L1GTScales scales_;
    const edm::InputTag tag_;
    const std::optional<int> minPt_;
    const std::optional<int> minEta_;
    const std::optional<int> maxEta_;
    const std::optional<int> minPhi_;
    const std::optional<int> maxPhi_;
    const std::optional<int> minZ0_;
    const std::optional<int> maxZ0_;
    const std::optional<int> minScalarSumPt_;
    const std::vector<unsigned int> qual_;
    const std::optional<int> minEtaAbs_;
    const std::optional<int> maxEtaAbs_;
    const std::vector<double> regionsAbsEtaLowerBounds_;
    const std::vector<unsigned int> regionsQual_;
    const std::vector<double> regionsMaxIso_;
    const std::vector<double> regionsPt_;
    const std::optional<double> maxIso_;
    const L1GTSingleInOutLUT oneOverIsoLUT_;
  };

}  // namespace l1t

#endif  // L1Trigger_Phase2L1GT_L1GTSingleCollectionCut_h
