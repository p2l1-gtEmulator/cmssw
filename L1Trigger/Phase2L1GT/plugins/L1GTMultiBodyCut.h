#ifndef L1Trigger_Phase2L1GT_L1GTMultiBodyCut_h
#define L1Trigger_Phase2L1GT_L1GTMultiBodyCut_h

#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"

#include "L1Trigger/Phase2L1GT/interface/L1GTInvariantMassError.h"

#include "L1Trigger/Phase2L1GT/interface/L1GTScales.h"

#include "L1GTSingleInOutLUT.h"
#include "L1GTOptionalParam.h"

#include <optional>

namespace l1t {

  class L1GTMultiBodyCut {
  public:
    L1GTMultiBodyCut(const edm::ParameterSet& config,
                     const edm::ParameterSet& lutConfig,
                     const L1GTScales& scales,
                     bool inv_mass_checks = false)
        : scales_(scales),
          coshEtaLUT_(lutConfig.getParameterSet("cosh_eta_lut")),
          coshEtaLUT2_(lutConfig.getParameterSet("cosh_eta_lut2")),
          cosPhiLUT_(lutConfig.getParameterSet("cos_phi_lut")),
          minInvMassSqrDiv2_(getOptionalParam<double, double>(
              "minInvMass", config, [&scales](double value) { return scales.to_hw_InvMassSqrDiv2(value); })),
          maxInvMassSqrDiv2_(getOptionalParam<double, double>(
              "maxInvMass", config, [&scales](double value) { return scales.to_hw_InvMassSqrDiv2(value); })),
          minTransMassSqrDiv2_(getOptionalParam<double, double>(
              "minTransMass", config, [&scales](double value) { return scales.to_hw_TransMassSqrDiv2(value); })),
          maxTransMassSqrDiv2_(getOptionalParam<double, double>(
              "maxTransMass", config, [&scales](double value) { return scales.to_hw_TransMassSqrDiv2(value); })),
          scale_normal_factor_(std::ceil(std::ceil(coshEtaLUT_.output_scale() / coshEtaLUT2_.output_scale()))),
          inv_mass_checks_(inv_mass_checks) {}

    bool checkObjects(const P2GTCandidate& obj1,
                      const P2GTCandidate& obj2,
                      const P2GTCandidate& obj3,
                      const P2GTCandidate& obj4,
                      InvariantMassErrorCollection& massErrors) const {
      bool res = true;

      if (minInvMassSqrDiv2_ || maxInvMassSqrDiv2_) {
        int64_t invMassSqrDiv2 = calc2BodyInvMass(obj1, obj2, massErrors) + calc2BodyInvMass(obj1, obj3, massErrors) +
                                 calc2BodyInvMass(obj2, obj3, massErrors) + calc2BodyInvMass(obj1, obj4, massErrors) +
                                 calc2BodyInvMass(obj2, obj4, massErrors) + calc2BodyInvMass(obj3, obj4, massErrors);

        res &= minInvMassSqrDiv2_ ? invMassSqrDiv2 > std::round(minInvMassSqrDiv2_.value() * coshEtaLUT_.output_scale())
                                  : true;
        res &= maxInvMassSqrDiv2_ ? invMassSqrDiv2 < std::round(maxInvMassSqrDiv2_.value() * coshEtaLUT_.output_scale())
                                  : true;
      }

      if (minTransMassSqrDiv2_ || maxTransMassSqrDiv2_) {
        int64_t transMassDiv2 = calc2BodyTransMass(obj1, obj2) + calc2BodyTransMass(obj1, obj3) +
                                calc2BodyTransMass(obj2, obj3) + calc2BodyTransMass(obj1, obj4) +
                                calc2BodyTransMass(obj2, obj4) + calc2BodyTransMass(obj3, obj4);

        res &= minTransMassSqrDiv2_
                   ? transMassDiv2 > std::round(minTransMassSqrDiv2_.value() * cosPhiLUT_.output_scale())
                   : true;
        res &= maxTransMassSqrDiv2_
                   ? transMassDiv2 < std::round(maxTransMassSqrDiv2_.value() * cosPhiLUT_.output_scale())
                   : true;
      }

      return res;
    }

    bool checkObjects(const P2GTCandidate& obj1,
                      const P2GTCandidate& obj2,
                      const P2GTCandidate& obj3,
                      InvariantMassErrorCollection& massErrors) const {
      bool res = true;

      if (minInvMassSqrDiv2_ || maxInvMassSqrDiv2_) {
        int64_t invMassSqrDiv2 = calc2BodyInvMass(obj1, obj2, massErrors) + calc2BodyInvMass(obj1, obj3, massErrors) +
                                 calc2BodyInvMass(obj2, obj3, massErrors);

        res &= minInvMassSqrDiv2_ ? invMassSqrDiv2 > std::round(minInvMassSqrDiv2_.value() * coshEtaLUT_.output_scale())
                                  : true;
        res &= maxInvMassSqrDiv2_ ? invMassSqrDiv2 < std::round(maxInvMassSqrDiv2_.value() * coshEtaLUT_.output_scale())
                                  : true;
      }

      if (minTransMassSqrDiv2_ || maxTransMassSqrDiv2_) {
        int64_t transMassDiv2 =
            calc2BodyTransMass(obj1, obj2) + calc2BodyTransMass(obj1, obj3) + calc2BodyTransMass(obj2, obj3);

        res &= minTransMassSqrDiv2_
                   ? transMassDiv2 > std::round(minTransMassSqrDiv2_.value() * cosPhiLUT_.output_scale())
                   : true;
        res &= maxTransMassSqrDiv2_
                   ? transMassDiv2 < std::round(maxTransMassSqrDiv2_.value() * cosPhiLUT_.output_scale())
                   : true;
      }

      return res;
    }

    static void fillPSetDescription(edm::ParameterSetDescription& desc) {
      desc.addOptional<double>("minInvMass");
      desc.addOptional<double>("maxInvMass");
      desc.addOptional<double>("minTransMass");
      desc.addOptional<double>("maxTransMass");
    }

  private:
    static constexpr int HW_PI = 1 << (P2GTCandidate::hwPhi_t::width - 1);  // assumes phi in [-pi, pi)

    int64_t calc2BodyInvMass(const P2GTCandidate& obj1,
                             const P2GTCandidate& obj2,
                             InvariantMassErrorCollection& massErrors) const {
      uint32_t dEta = (obj1.hwEta() > obj2.hwEta()) ? obj1.hwEta().to_int() - obj2.hwEta().to_int()
                                                    : obj2.hwEta().to_int() - obj1.hwEta().to_int();
      int32_t lutCoshDEta = dEta < L1GTSingleInOutLUT::DETA_LUT_SPLIT
                                ? coshEtaLUT_[dEta]
                                : coshEtaLUT2_[dEta - L1GTSingleInOutLUT::DETA_LUT_SPLIT];

      // Ensure dPhi is always the smaller angle, i.e. always between [0, pi]
      uint32_t dPhi = HW_PI - abs(abs(obj1.hwPhi().to_int() - obj2.hwPhi().to_int()) - HW_PI);

      // Optimization: (cos(x + pi) = -cos(x), x in [0, pi))
      int32_t lutCosDPhi = dPhi >= HW_PI ? -cosPhiLUT_[dPhi] : cosPhiLUT_[dPhi];

      int64_t invMassSqrDiv2;

      if (dEta < L1GTSingleInOutLUT::DETA_LUT_SPLIT) {
        // dEta [0, 2pi)
        invMassSqrDiv2 = obj1.hwPT().to_int64() * obj2.hwPT().to_int64() * (lutCoshDEta - lutCosDPhi);
      } else {
        // dEta [2pi, 4pi), ignore cos
        invMassSqrDiv2 = obj1.hwPT().to_int64() * obj2.hwPT().to_int64() * lutCoshDEta;
      }

      if (inv_mass_checks_) {
        double precInvMass =
            scales_.pT_lsb() * std::sqrt(2 * obj1.hwPT().to_double() * obj2.hwPT().to_double() *
                                         (std::cosh(dEta * scales_.eta_lsb()) - std::cos(dPhi * scales_.phi_lsb())));

        double lutInvMass =
            scales_.pT_lsb() * std::sqrt(2 * static_cast<double>(invMassSqrDiv2) /
                                         (dEta < L1GTSingleInOutLUT::DETA_LUT_SPLIT ? coshEtaLUT_.output_scale()
                                                                                    : coshEtaLUT2_.output_scale()));

        double error = std::abs(precInvMass - lutInvMass);
        massErrors.emplace_back(InvariantMassError{error, error / precInvMass, precInvMass});
      }

      // Normalize scales required due to LUT split in dEta with different scale factors.
      return dEta < L1GTSingleInOutLUT::DETA_LUT_SPLIT ? invMassSqrDiv2 : invMassSqrDiv2 * scale_normal_factor_;
    }

    int64_t calc2BodyTransMass(const P2GTCandidate& obj1, const P2GTCandidate& obj2) const {
      // Ensure dPhi is always the smaller angle, i.e. always between [0, pi]
      uint32_t dPhi = HW_PI - abs(abs(obj1.hwPhi().to_int() - obj2.hwPhi().to_int()) - HW_PI);

      // Optimization: (cos(x + pi) = -cos(x), x in [0, pi))
      int32_t lutCosDPhi = dPhi >= HW_PI ? -cosPhiLUT_[dPhi] : cosPhiLUT_[dPhi];

      return obj1.hwPT().to_int64() * obj2.hwPT().to_int64() *
             (static_cast<int64_t>(std::round(cosPhiLUT_.output_scale())) - lutCosDPhi);
    }

    const L1GTScales& scales_;

    const L1GTSingleInOutLUT coshEtaLUT_;   // [0, 2pi)
    const L1GTSingleInOutLUT coshEtaLUT2_;  // [2pi, 4pi)
    const L1GTSingleInOutLUT cosPhiLUT_;

    const std::optional<double> minInvMassSqrDiv2_;
    const std::optional<double> maxInvMassSqrDiv2_;
    const std::optional<double> minTransMassSqrDiv2_;
    const std::optional<double> maxTransMassSqrDiv2_;

    const int64_t scale_normal_factor_;
    const bool inv_mass_checks_;
  };

}  // namespace l1t

#endif  // L1Trigger_Phase2L1GT_L1GTMultiBodyCut_h
