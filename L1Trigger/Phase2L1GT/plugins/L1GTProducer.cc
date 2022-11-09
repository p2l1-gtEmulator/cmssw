#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "DataFormats/Common/interface/Handle.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/View.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"

#include "DataFormats/L1TCorrelator/interface/TkElectronFwd.h"
#include "DataFormats/L1TCorrelator/interface/TkEmFwd.h"

#include "DataFormats/L1TCorrelator/interface/TkElectron.h"
#include "DataFormats/L1TCorrelator/interface/TkEm.h"

#include <vector>
#include <array>
#include <string>

using namespace l1t;

class L1GTProducer : public edm::stream::EDProducer<> {
public:
  explicit L1GTProducer(const edm::ParameterSet &);
  ~L1GTProducer() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions &);

private:
  void produce(edm::Event &, const edm::EventSetup &) override;

  const std::vector<edm::InputTag> cl2ElectronTags;
  const std::vector<edm::InputTag> cl2PhotonTags;
};

template <typename T>
static inline T getOptionalParam(const char *name, const edm::ParameterSet &config) {
  if (config.exists(name)) {
    return config.getParameter<T>(name);
  }
  return T();
}

L1GTProducer::L1GTProducer(const edm::ParameterSet &config)
    : cl2ElectronTags(getOptionalParam<std::vector<edm::InputTag>>("CL2Electrons", config)),
      cl2PhotonTags(getOptionalParam<std::vector<edm::InputTag>>("CL2Photons", config)) {
  for (const edm::InputTag &tag : cl2ElectronTags) {
    consumes<TkElectronCollection>(tag);
  }

  for (const edm::InputTag &tag : cl2PhotonTags) {
    consumes<TkEmCollection>(tag);
  }

  produces<P2GTCandidateCollection>("CL2 Electrons");
  produces<P2GTCandidateCollection>("CL2 Photons");
}

void L1GTProducer::fillDescriptions(edm::ConfigurationDescriptions &description) {
  edm::ParameterSetDescription desc;
  desc.addOptional<std::vector<edm::InputTag>>("CL2Electrons");
  desc.addOptional<std::vector<edm::InputTag>>("CL2Photons");

  description.addWithDefaultLabel(desc);
}

template <typename T>
static void produceByTags(const std::string &productName, const std::vector<edm::InputTag> &tags, edm::Event &event) {
  std::unique_ptr<P2GTCandidateCollection> outputCollection = std::make_unique<P2GTCandidateCollection>();
  for (const edm::InputTag &tag : tags) {
    edm::Handle<T> inputCollection;
    if (event.getByLabel(tag, inputCollection)) {
      for (const auto &object : *inputCollection) {
        outputCollection->emplace_back(P2GTCandidate(object));
      }
    }
  }

  event.put(std::move(outputCollection), productName);
}

void L1GTProducer::produce(edm::Event &event, const edm::EventSetup &setup) {
  produceByTags<TkElectronCollection>("CL2 Electrons", cl2ElectronTags, event);
  produceByTags<TkEmCollection>("CL2 Photons", cl2PhotonTags, event);
}

DEFINE_FWK_MODULE(L1GTProducer);
