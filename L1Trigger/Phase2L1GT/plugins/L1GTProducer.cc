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

#include "DataFormats/L1Trigger/interface/TkJetWord.h"
#include "DataFormats/L1Trigger/interface/VertexWord.h"

#include "DataFormats/L1TMuonPhase2/interface/SAMuon.h"
#include "DataFormats/L1TMuonPhase2/interface/TrackerMuon.h"

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

  const edm::InputTag gttPromptJetTag_;
  const edm::InputTag gttDisplacedJetTag_;
  const edm::InputTag gttPrimaryVertexTag_;

  const edm::InputTag gmtSaPromptMuonTag_;
  const edm::InputTag gmtSaDisplacedMuonTag_;
  const edm::InputTag gmtTkMuonTag_;
};

template <typename T>
static inline T getOptionalParam(const char *name, const edm::ParameterSet &config) {
  if (config.exists(name)) {
    return config.getParameter<T>(name);
  }
  return T();
}

L1GTProducer::L1GTProducer(const edm::ParameterSet &config)
    : gttPromptJetTag_(getOptionalParam<edm::InputTag>("GTTPromptJets", config)),
      gttDisplacedJetTag_(getOptionalParam<edm::InputTag>("GTTDisplacedJets", config)),
      gttPrimaryVertexTag_(getOptionalParam<edm::InputTag>("GTTPrimaryVert", config)),
      gmtSaPromptMuonTag_(getOptionalParam<edm::InputTag>("GMTSaPromptMuons", config)),
      gmtSaDisplacedMuonTag_(getOptionalParam<edm::InputTag>("GMTSaDisplacedMuons", config)),
      gmtTkMuonTag_(getOptionalParam<edm::InputTag>("GMTTkMuons", config)) {
  consumes<TkJetWordCollection>(gttPromptJetTag_);
  consumes<TkJetWordCollection>(gttDisplacedJetTag_);
  consumes<VertexWordCollection>(gttPrimaryVertexTag_);

  consumes<SAMuonCollection>(gmtSaPromptMuonTag_);
  consumes<SAMuonCollection>(gmtSaDisplacedMuonTag_);
  consumes<TrackerMuonCollection>(gmtTkMuonTag_);

  produces<P2GTCandidateCollection>("GTTPromptJets");
  produces<P2GTCandidateCollection>("GTTDisplacedJets");
  produces<P2GTCandidateCollection>("GTTPrimaryVert");

  produces<P2GTCandidateCollection>("GMTSaPromptMuons");
  produces<P2GTCandidateCollection>("GMTSaDisplacedMuons");
  produces<P2GTCandidateCollection>("GMTTkMuons");
}

void L1GTProducer::fillDescriptions(edm::ConfigurationDescriptions &description) {
  edm::ParameterSetDescription desc;
  desc.addOptional<edm::InputTag>("GTTPromptJets");
  desc.addOptional<edm::InputTag>("GTTDisplacedJets");
  desc.addOptional<edm::InputTag>("GTTPrimaryVert");

  desc.addOptional<edm::InputTag>("GMTSaPromptMuons");
  desc.addOptional<edm::InputTag>("GMTSaDisplacedMuons");
  desc.addOptional<edm::InputTag>("GMTTkMuons");

  description.addWithDefaultLabel(desc);
}

template <typename T, std::size_t MAX_COLLECTION_SIZE = 12>
static void produceByTag(const std::string &productName, const edm::InputTag &tag, edm::Event &event) {
  std::unique_ptr<P2GTCandidateCollection> outputCollection = std::make_unique<P2GTCandidateCollection>();
  edm::Handle<T> inputCollection;
  if (event.getByLabel(tag, inputCollection)) {
    std::size_t idx = 0;
    for (const auto &object : *inputCollection) {
      if (idx >= MAX_COLLECTION_SIZE) {
        break;
      }

      outputCollection->emplace_back(P2GTCandidate(object));
      ++idx;
    }
  }

  event.put(std::move(outputCollection), productName);
}

void L1GTProducer::produce(edm::Event &event, const edm::EventSetup &setup) {
  produceByTag<TkJetWordCollection>("GTTPromptJets", gttPromptJetTag_, event);
  produceByTag<TkJetWordCollection>("GTTDisplacedJets", gttDisplacedJetTag_, event);
  produceByTag<VertexWordCollection, 10>("GTTPrimaryVert", gttPrimaryVertexTag_, event);

  produceByTag<SAMuonCollection>("GMTSaPromptMuons", gmtSaPromptMuonTag_, event);
  produceByTag<SAMuonCollection>("GMTSaDisplacedMuons", gmtSaDisplacedMuonTag_, event);
  produceByTag<TrackerMuonCollection>("GMTTkMuons", gmtTkMuonTag_, event);
}

DEFINE_FWK_MODULE(L1GTProducer);
