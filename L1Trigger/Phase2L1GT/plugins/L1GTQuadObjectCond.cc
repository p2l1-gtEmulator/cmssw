#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"

#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/Ref.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "L1Trigger/Phase2L1GT/interface/L1GTScales.h"
#include "L1GTSingleCollectionCut.h"

#include <cinttypes>
#include <memory>
#include <vector>
#include <set>

#include <ap_int.h>

using namespace l1t;

class L1GTQuadObjectCond : public edm::stream::EDFilter<> {
public:
  explicit L1GTQuadObjectCond(const edm::ParameterSet&);
  ~L1GTQuadObjectCond() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  bool filter(edm::Event&, edm::EventSetup const&) override;
  bool checkObjects(const P2GTCandidate&, const P2GTCandidate&, const P2GTCandidate&, const P2GTCandidate&) const;

  const L1GTScales scales_;

  const L1GTSingleCollectionCut collection1Cuts_;
  const L1GTSingleCollectionCut collection2Cuts_;
  const L1GTSingleCollectionCut collection3Cuts_;
  const L1GTSingleCollectionCut collection4Cuts_;

  const bool os_;  // Opposite sign
  const bool ss_;  // Same sign
};

L1GTQuadObjectCond::L1GTQuadObjectCond(const edm::ParameterSet& config)
    : scales_(config.getParameter<edm::ParameterSet>("scales")),
      collection1Cuts_(config.getParameter<edm::ParameterSet>("collection1"), scales_),
      collection2Cuts_(config.getParameter<edm::ParameterSet>("collection2"), scales_),
      collection3Cuts_(config.getParameter<edm::ParameterSet>("collection3"), scales_),
      collection4Cuts_(config.getParameter<edm::ParameterSet>("collection4"), scales_),
      os_(config.exists("os") ? config.getParameter<bool>("os") : false),
      ss_(config.exists("ss") ? config.getParameter<bool>("ss") : false) {
  consumes<P2GTCandidateCollection>(collection1Cuts_.tag());
  produces<P2GTCandidateVectorRef>(collection1Cuts_.tag().instance());

  if (!(collection1Cuts_.tag() == collection2Cuts_.tag())) {
    consumes<P2GTCandidateCollection>(collection2Cuts_.tag());
    produces<P2GTCandidateVectorRef>(collection2Cuts_.tag().instance());
  }

  if (!(collection1Cuts_.tag() == collection3Cuts_.tag()) && !(collection2Cuts_.tag() == collection3Cuts_.tag())) {
    consumes<P2GTCandidateCollection>(collection3Cuts_.tag());
    produces<P2GTCandidateVectorRef>(collection3Cuts_.tag().instance());
  }

  if (!(collection1Cuts_.tag() == collection4Cuts_.tag()) && !(collection2Cuts_.tag() == collection4Cuts_.tag()) &&
      !(collection3Cuts_.tag() == collection4Cuts_.tag())) {
    consumes<P2GTCandidateCollection>(collection4Cuts_.tag());
    produces<P2GTCandidateVectorRef>(collection4Cuts_.tag().instance());
  }
}

void L1GTQuadObjectCond::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;

  edm::ParameterSetDescription collection1Desc;
  L1GTSingleCollectionCut::fillDescriptions(collection1Desc);
  desc.add<edm::ParameterSetDescription>("collection1", collection1Desc);

  edm::ParameterSetDescription collection2Desc;
  L1GTSingleCollectionCut::fillDescriptions(collection2Desc);
  desc.add<edm::ParameterSetDescription>("collection2", collection2Desc);

  edm::ParameterSetDescription collection3Desc;
  L1GTSingleCollectionCut::fillDescriptions(collection3Desc);
  desc.add<edm::ParameterSetDescription>("collection3", collection3Desc);

  edm::ParameterSetDescription collection4Desc;
  L1GTSingleCollectionCut::fillDescriptions(collection4Desc);
  desc.add<edm::ParameterSetDescription>("collection4", collection4Desc);

  desc.addOptional<bool>("os", false);
  desc.addOptional<bool>("ss", false);

  edm::ParameterSetDescription scalesDesc;
  L1GTScales::fillDescriptions(scalesDesc);
  desc.add<edm::ParameterSetDescription>("scales", scalesDesc);

  descriptions.addWithDefaultLabel(desc);
}

bool L1GTQuadObjectCond::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<P2GTCandidateCollection> col1;
  edm::Handle<P2GTCandidateCollection> col2;
  edm::Handle<P2GTCandidateCollection> col3;
  edm::Handle<P2GTCandidateCollection> col4;
  event.getByLabel(collection1Cuts_.tag(), col1);
  event.getByLabel(collection2Cuts_.tag(), col2);
  event.getByLabel(collection3Cuts_.tag(), col3);
  event.getByLabel(collection4Cuts_.tag(), col4);

  bool condition_result = false;

  std::set<std::size_t> triggeredIdcs1;
  std::set<std::size_t> triggeredIdcs2;
  std::set<std::size_t> triggeredIdcs3;
  std::set<std::size_t> triggeredIdcs4;

  for (std::size_t idx1 = 0; idx1 < col1->size(); ++idx1) {
    for (std::size_t idx2 = 0; idx2 < col2->size(); ++idx2) {
      for (std::size_t idx3 = 0; idx3 < col3->size(); ++idx3) {
        for (std::size_t idx4 = 0; idx3 < col3->size(); ++idx3) {
          // If we're looking at the same collection then we shouldn't use the same object in one comparison.
          if (col1.product() == col2.product() && idx1 == idx2) {
            continue;
          }

          if (col2.product() == col3.product() && idx2 == idx3) {
            continue;
          }

          if (col1.product() == col3.product() && idx1 == idx3) {
            continue;
          }

          if (col1.product() == col4.product() && idx1 == idx4) {
            continue;
          }

          if (col2.product() == col4.product() && idx2 == idx4) {
            continue;
          }

          if (col3.product() == col4.product() && idx3 == idx4) {
            continue;
          }

          bool pass{checkObjects(col1->at(idx1), col2->at(idx2), col3->at(idx3), col4->at(idx4))};
          condition_result |= pass;

          if (pass) {
            triggeredIdcs1.emplace(idx1);

            if (col1.product() != col2.product()) {
              triggeredIdcs2.emplace(idx2);
            } else {
              triggeredIdcs1.emplace(idx2);
            }

            if (col1.product() != col3.product() && col2.product() != col3.product()) {
              triggeredIdcs3.emplace(idx3);
            } else if (col1.product() == col3.product()) {
              triggeredIdcs1.emplace(idx3);
            } else {
              triggeredIdcs2.emplace(idx3);
            }

            if (col1.product() != col4.product() && col2.product() != col4.product() &&
                col3.product() != col4.product()) {
              triggeredIdcs4.emplace(idx4);
            } else if (col1.product() == col4.product()) {
              triggeredIdcs1.emplace(idx4);
            } else if (col2.product() == col4.product()) {
              triggeredIdcs2.emplace(idx4);
            } else {
              triggeredIdcs3.emplace(idx4);
            }
          }
        }
      }
    }
  }

  if (condition_result) {
    std::unique_ptr<P2GTCandidateVectorRef> triggerCol1 = std::make_unique<P2GTCandidateVectorRef>();

    for (std::size_t idx : triggeredIdcs1) {
      triggerCol1->push_back(P2GTCandidateRef(col1, idx));
    }
    event.put(std::move(triggerCol1), collection1Cuts_.tag().instance());

    if (col1.product() != col2.product()) {
      std::unique_ptr<P2GTCandidateVectorRef> triggerCol2 = std::make_unique<P2GTCandidateVectorRef>();

      for (std::size_t idx : triggeredIdcs2) {
        triggerCol2->push_back(P2GTCandidateRef(col2, idx));
      }
      event.put(std::move(triggerCol2), collection2Cuts_.tag().instance());
    }

    if (col1.product() != col3.product() && col2.product() != col3.product()) {
      std::unique_ptr<P2GTCandidateVectorRef> triggerCol3 = std::make_unique<P2GTCandidateVectorRef>();

      for (std::size_t idx : triggeredIdcs3) {
        triggerCol3->push_back(P2GTCandidateRef(col3, idx));
      }
      event.put(std::move(triggerCol3), collection3Cuts_.tag().instance());
    }

    if (col1.product() != col4.product() && col2.product() != col4.product() && col3.product() != col4.product()) {
      std::unique_ptr<P2GTCandidateVectorRef> triggerCol4 = std::make_unique<P2GTCandidateVectorRef>();

      for (std::size_t idx : triggeredIdcs4) {
        triggerCol4->push_back(P2GTCandidateRef(col4, idx));
      }
      event.put(std::move(triggerCol4), collection4Cuts_.tag().instance());
    }
  }

  return condition_result;
}

bool L1GTQuadObjectCond::checkObjects(const P2GTCandidate& obj1,
                                      const P2GTCandidate& obj2,
                                      const P2GTCandidate& obj3,
                                      const P2GTCandidate& obj4) const {
  bool res{true};

  res &= collection1Cuts_.checkObject(obj1);
  res &= collection2Cuts_.checkObject(obj2);
  res &= collection3Cuts_.checkObject(obj3);
  res &= collection4Cuts_.checkObject(obj4);

  res &= ss_ ? (obj1.hwCharge() == obj2.hwCharge() && obj1.hwCharge() == obj3.hwCharge() &&
                obj1.hwCharge() == obj4.hwCharge())
             : true;

  res &= os_ ? !(obj1.hwCharge() == obj2.hwCharge() && obj1.hwCharge() == obj3.hwCharge() &&
                 obj1.hwCharge() == obj4.hwCharge())
             : true;

  return res;
}

DEFINE_FWK_MODULE(L1GTQuadObjectCond);
