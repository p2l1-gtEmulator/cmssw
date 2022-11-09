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

#include <set>

#include <ap_int.h>

using namespace l1t;

class L1GTTripleObjectCond : public edm::stream::EDFilter<> {
public:
  explicit L1GTTripleObjectCond(const edm::ParameterSet&);
  ~L1GTTripleObjectCond() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  bool filter(edm::Event&, edm::EventSetup const&) override;
  bool checkObjects(const P2GTCandidate&, const P2GTCandidate&, const P2GTCandidate&) const;

  const L1GTScales scales_;

  const L1GTSingleCollectionCut collection1_;
  const L1GTSingleCollectionCut collection2_;
  const L1GTSingleCollectionCut collection3_;

  const bool os_;  // Opposite sign
  const bool ss_;  // Same sign
};

L1GTTripleObjectCond::L1GTTripleObjectCond(const edm::ParameterSet& config)
    : scales_(config.getParameter<edm::ParameterSet>("scales")),
      collection1_(config.getParameter<edm::ParameterSet>("collection1"), scales_),
      collection2_(config.getParameter<edm::ParameterSet>("collection2"), scales_),
      collection3_(config.getParameter<edm::ParameterSet>("collection3"), scales_),
      os_(config.exists("os") ? config.getParameter<bool>("os") : false),
      ss_(config.exists("ss") ? config.getParameter<bool>("ss") : false) {
  consumes<P2GTCandidateCollection>(collection1_.tag());
  produces<P2GTCandidateVectorRef>(collection1_.tag().instance());

  if (!(collection1_.tag() == collection2_.tag())) {
    consumes<P2GTCandidateCollection>(collection2_.tag());
    produces<P2GTCandidateVectorRef>(collection2_.tag().instance());
  }

  if (!(collection1_.tag() == collection3_.tag()) && !(collection2_.tag() == collection3_.tag())) {
    consumes<P2GTCandidateCollection>(collection3_.tag());
    produces<P2GTCandidateVectorRef>(collection3_.tag().instance());
  }
}

void L1GTTripleObjectCond::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
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

  desc.addOptional<bool>("os", false);
  desc.addOptional<bool>("ss", false);

  edm::ParameterSetDescription scalesDesc;
  L1GTScales::fillDescriptions(scalesDesc);
  desc.add<edm::ParameterSetDescription>("scales", scalesDesc);

  descriptions.addWithDefaultLabel(desc);
}

bool L1GTTripleObjectCond::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<P2GTCandidateCollection> col1;
  edm::Handle<P2GTCandidateCollection> col2;
  edm::Handle<P2GTCandidateCollection> col3;
  event.getByLabel(collection1_.tag(), col1);
  event.getByLabel(collection2_.tag(), col2);
  event.getByLabel(collection3_.tag(), col3);

  bool condition_result = false;

  std::set<std::size_t> triggeredIdcs1;
  std::set<std::size_t> triggeredIdcs2;
  std::set<std::size_t> triggeredIdcs3;

  for (std::size_t idx1 = 0; idx1 < col1->size(); ++idx1) {
    for (std::size_t idx2 = 0; idx2 < col2->size(); ++idx2) {
      for (std::size_t idx3 = 0; idx3 < col3->size(); ++idx3) {
        // If we're looking at the same collection then we shouldn't use the same object in one comparison.
        if (col1.product() == col2.product() && idx1 == idx2) {
          continue;
        }

        if (col1.product() == col3.product() && idx1 == idx3) {
          continue;
        }

        if (col2.product() == col3.product() && idx2 == idx3) {
          continue;
        }

        bool pass{checkObjects(col1->at(idx1), col2->at(idx2), col3->at(idx3))};
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
        }
      }
    }
  }

  if (condition_result) {
    std::unique_ptr<P2GTCandidateVectorRef> triggerCol1 = std::make_unique<P2GTCandidateVectorRef>();

    for (std::size_t idx : triggeredIdcs1) {
      triggerCol1->push_back(P2GTCandidateRef(col1, idx));
    }
    event.put(std::move(triggerCol1), collection1_.tag().instance());

    if (col1.product() != col2.product()) {
      std::unique_ptr<P2GTCandidateVectorRef> triggerCol2 = std::make_unique<P2GTCandidateVectorRef>();

      for (std::size_t idx : triggeredIdcs2) {
        triggerCol2->push_back(P2GTCandidateRef(col2, idx));
      }
      event.put(std::move(triggerCol2), collection2_.tag().instance());
    }

    if (col1.product() != col3.product() && col2.product() != col3.product()) {
      std::unique_ptr<P2GTCandidateVectorRef> triggerCol3 = std::make_unique<P2GTCandidateVectorRef>();

      for (std::size_t idx : triggeredIdcs3) {
        triggerCol3->push_back(P2GTCandidateRef(col3, idx));
      }
      event.put(std::move(triggerCol3), collection3_.tag().instance());
    }
  }

  return condition_result;
}

bool L1GTTripleObjectCond::checkObjects(const P2GTCandidate& obj1,
                                        const P2GTCandidate& obj2,
                                        const P2GTCandidate& obj3) const {
  bool res{true};
  res &= collection1_.checkObject(obj1);
  res &= collection2_.checkObject(obj2);
  res &= collection3_.checkObject(obj3);

  res &= ss_ ? (obj1.hwCharge() == obj2.hwCharge() && obj1.hwCharge() == obj3.hwCharge()) : true;
  res &= os_ ? !(obj1.hwCharge() == obj2.hwCharge() && obj1.hwCharge() == obj3.hwCharge()) : true;

  return res;
}

DEFINE_FWK_MODULE(L1GTTripleObjectCond);
