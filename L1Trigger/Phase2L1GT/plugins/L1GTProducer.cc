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

#include "DataFormats/L1TParticleFlow/interface/PFJet.h"
#include "DataFormats/L1TCorrelator/interface/TkEmFwd.h"
#include "DataFormats/L1TCorrelator/interface/TkEm.h"
#include "DataFormats/L1TCorrelator/interface/TkElectronFwd.h"
#include "DataFormats/L1TCorrelator/interface/TkElectron.h"

#include "DataFormats/L1Trigger/interface/EtSum.h"

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

  const edm::InputTag cl2JetTag_;
  const edm::InputTag cl2PhotonTag_;
  const edm::InputTag cl2ElectronTag_;
  const edm::InputTag cl2EtSumTag_;
  const edm::InputTag cl2HtSumTag_;
};

L1GTProducer::L1GTProducer(const edm::ParameterSet &config)
    : gttPromptJetTag_(config.getParameter<edm::InputTag>("GTTPromptJets")),
      gttDisplacedJetTag_(config.getParameter<edm::InputTag>("GTTDisplacedJets")),
      gttPrimaryVertexTag_(config.getParameter<edm::InputTag>("GTTPrimaryVert")),
      gmtSaPromptMuonTag_(config.getParameter<edm::InputTag>("GMTSaPromptMuons")),
      gmtSaDisplacedMuonTag_(config.getParameter<edm::InputTag>("GMTSaDisplacedMuons")),
      gmtTkMuonTag_(config.getParameter<edm::InputTag>("GMTTkMuons")),
      cl2JetTag_(config.getParameter<edm::InputTag>("CL2Jets")),
      cl2PhotonTag_(config.getParameter<edm::InputTag>("CL2Photons")),
      cl2ElectronTag_(config.getParameter<edm::InputTag>("CL2Electrons")),
      cl2EtSumTag_(config.getParameter<edm::InputTag>("CL2EtSum")),
      cl2HtSumTag_(config.getParameter<edm::InputTag>("CL2HtSum")) {
  consumes<TkJetWordCollection>(gttPromptJetTag_);
  consumes<TkJetWordCollection>(gttDisplacedJetTag_);
  consumes<VertexWordCollection>(gttPrimaryVertexTag_);

  consumes<SAMuonCollection>(gmtSaPromptMuonTag_);
  consumes<SAMuonCollection>(gmtSaDisplacedMuonTag_);
  consumes<TrackerMuonCollection>(gmtTkMuonTag_);

  consumes<PFJetCollection>(cl2JetTag_);
  consumes<TkEmCollection>(cl2PhotonTag_);
  consumes<TkElectronCollection>(cl2ElectronTag_);
  consumes<std::vector<l1t::EtSum>>(cl2EtSumTag_);
  consumes<std::vector<l1t::EtSum>>(cl2HtSumTag_);

  produces<P2GTCandidateCollection>("GTTPromptJets");
  produces<P2GTCandidateCollection>("GTTDisplacedJets");
  produces<P2GTCandidateCollection>("GTTPrimaryVert");

  produces<P2GTCandidateCollection>("GMTSaPromptMuons");
  produces<P2GTCandidateCollection>("GMTSaDisplacedMuons");
  produces<P2GTCandidateCollection>("GMTTkMuons");

  produces<P2GTCandidateCollection>("CL2Jets");
  produces<P2GTCandidateCollection>("CL2Photons");
  produces<P2GTCandidateCollection>("CL2Electrons");
  produces<P2GTCandidateCollection>("CL2EtSum");
  produces<P2GTCandidateCollection>("CL2HtSum");
}

void L1GTProducer::fillDescriptions(edm::ConfigurationDescriptions &description) {
  edm::ParameterSetDescription desc;
  desc.addOptional<edm::InputTag>("GTTPromptJets");
  desc.addOptional<edm::InputTag>("GTTDisplacedJets");
  desc.addOptional<edm::InputTag>("GTTPrimaryVert");

  desc.addOptional<edm::InputTag>("GMTSaPromptMuons");
  desc.addOptional<edm::InputTag>("GMTSaDisplacedMuons");
  desc.addOptional<edm::InputTag>("GMTTkMuons");

  desc.addOptional<edm::InputTag>("CL2Jets");
  desc.addOptional<edm::InputTag>("CL2Photons");
  desc.addOptional<edm::InputTag>("CL2Electrons");
  desc.addOptional<edm::InputTag>("CL2EtSum");
  desc.addOptional<edm::InputTag>("CL2HtSum");

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

static void produceCl2HtSum(const std::string &productName, const edm::InputTag &tag, edm::Event &event) {
  std::unique_ptr<P2GTCandidateCollection> outputCollection = std::make_unique<P2GTCandidateCollection>();
  edm::Handle<std::vector<EtSum>> htCollection;
  event.getByLabel(tag, htCollection);
  outputCollection->emplace_back(P2GTCandidate(htCollection->at(0), htCollection->at(1)));
  event.put(std::move(outputCollection), productName);
}

void L1GTProducer::produce(edm::Event &event, const edm::EventSetup &setup) {
  produceByTag<TkJetWordCollection>("GTTPromptJets", gttPromptJetTag_, event);
  produceByTag<TkJetWordCollection>("GTTDisplacedJets", gttDisplacedJetTag_, event);
  produceByTag<VertexWordCollection, 10>("GTTPrimaryVert", gttPrimaryVertexTag_, event);

  produceByTag<SAMuonCollection>("GMTSaPromptMuons", gmtSaPromptMuonTag_, event);
  produceByTag<SAMuonCollection>("GMTSaDisplacedMuons", gmtSaDisplacedMuonTag_, event);
  produceByTag<TrackerMuonCollection>("GMTTkMuons", gmtTkMuonTag_, event);

  produceByTag<PFJetCollection>("CL2Jets", cl2JetTag_, event);
  produceByTag<TkEmCollection>("CL2Photons", cl2PhotonTag_, event);
  produceByTag<TkElectronCollection>("CL2Electrons", cl2ElectronTag_, event);
  produceByTag<std::vector<EtSum>, 1>("CL2EtSum", cl2EtSumTag_, event);
  produceCl2HtSum("CL2HtSum", cl2HtSumTag_, event);
}

DEFINE_FWK_MODULE(L1GTProducer);
