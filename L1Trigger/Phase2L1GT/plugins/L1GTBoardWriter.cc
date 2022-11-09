/**
 * BoardDataWriter for validation with hardware. Currently only writing the algo bits is implemented.
 **/

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "L1Trigger/DemonstratorTools/interface/BoardDataWriter.h"
#include "L1Trigger/DemonstratorTools/interface/utilities.h"

#include "FWCore/Utilities/interface/EDGetToken.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include "FWCore/Framework/interface/TriggerNamesService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "ap_int.h"

#include <vector>
#include <map>
#include <cmath>
#include <algorithm>
#include <string>
#include <optional>

class L1GTBoardWriter : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit L1GTBoardWriter(const edm::ParameterSet&);

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  struct AlgoBit {
    unsigned int bitPos_;
    std::string path;
    std::optional<std::size_t> idx;

    bool isSet(const edm::TriggerResults& triggerResults, const std::vector<std::string>& paths) {
      if (!idx) {
        auto it = std::find(paths.begin(), paths.end(), path);
        if (it == paths.end()) {
          edm::LogError("L1GTBoardWriter") << "path not found: " << path;
        }
        idx = it - paths.begin();
      }
      return triggerResults[idx.value()].accept();
    }
  };

private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;

  l1t::demo::BoardDataWriter boardDataWriter_;
  edm::EDGetTokenT<edm::TriggerResults> trigResults_;
  std::map<size_t, std::vector<AlgoBit>> algoBitMap_;
};

static l1t::demo::BoardDataWriter::ChannelMap_t generateChannelMap(const edm::ParameterSet& config) {
  l1t::demo::BoardDataWriter::ChannelMap_t channelMap;
  for (auto& param : config.getParameterSetVector("channelConfig")) {
    l1t::demo::LinkId id{"Algos", param.getParameter<unsigned int>("channel")};

    const edm::VParameterSet& algoBits = param.getParameterSetVector("algoBits");

    unsigned int maxBit = 0;

    for (const auto& algoBit : algoBits) {
      maxBit = std::max(algoBit.getParameter<unsigned int>("bitPos"), maxBit);
    }

    l1t::demo::ChannelSpec spec{1, static_cast<size_t>(9 - std::ceil(static_cast<float>(maxBit + 1) / 64)), 0};

    channelMap.insert({id, {spec, {id.channel}}});
  }

  return channelMap;
}

L1GTBoardWriter::L1GTBoardWriter(const edm::ParameterSet& config)
    : boardDataWriter_(l1t::demo::FileFormat::EMP,
                       config.getParameter<std::string>("outputFilename"),
                       9,
                       1,
                       config.exists("maxLines") ? config.getParameter<unsigned int>("maxLines") : 1024,
                       generateChannelMap(config)),
      trigResults_(consumes<edm::TriggerResults>(edm::InputTag(
          "TriggerResults", "", config.exists("processName") ? config.getParameter<std::string>("processName") : ""))) {
  for (const edm::ParameterSet& param : config.getParameterSetVector("channelConfig")) {
    std::vector<AlgoBit> algoBits;
    for (const edm::ParameterSet& algoConfig : param.getParameterSetVector("algoBits")) {
      algoBits.emplace_back(AlgoBit{
          algoConfig.getParameter<unsigned int>("bitPos"), algoConfig.getParameter<std::string>("path"), std::nullopt});
    }

    std::sort(algoBits.begin(), algoBits.end(), [](const AlgoBit& lhs, const AlgoBit& rhs) {
      return lhs.bitPos_ < rhs.bitPos_;
    });

    algoBitMap_.emplace(param.getParameter<unsigned int>("channel"), algoBits);
  }
}

void L1GTBoardWriter::analyze(const edm::Event& event, const edm::EventSetup& iSetup) {
  edm::Service<edm::service::TriggerNamesService> tns;
  std::vector<std::string> triggerPaths;

  const edm::TriggerResults& trigResults = event.get(trigResults_);

  if (!tns.isAvailable() || !tns->getTrigPaths(trigResults, triggerPaths)) {
    edm::LogError("L1GTBoardWriter") << "TriggerNamesService not available!";
  }

  l1t::demo::EventData eventData;
  for (auto& [channel, algoBits] : algoBitMap_) {
    std::vector<ap_uint<64>> bits(std::ceil(static_cast<float>(algoBits.back().bitPos_ + 1) / 64), 0);

    for (AlgoBit& algoBit : algoBits) {
      bits[algoBit.bitPos_ / 64].set(algoBit.bitPos_ % 64, algoBit.isSet(trigResults, triggerPaths));
    }

    eventData.add({"Algos", channel}, bits);
  }

  boardDataWriter_.addEvent(eventData);
}

void L1GTBoardWriter::endJob() { boardDataWriter_.flush(); }

void L1GTBoardWriter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription algoDesc;
  algoDesc.add<unsigned int>("bitPos");
  algoDesc.add<std::string>("path");

  edm::ParameterSetDescription algosDesc;
  algosDesc.add<unsigned int>("channel");
  algosDesc.addVPSet("algoBits", algoDesc);

  edm::ParameterSetDescription desc;
  desc.add<std::string>("outputFilename");
  desc.addVPSet("channelConfig", algosDesc);
  desc.addOptional<unsigned int>("maxLines", 1024);
  desc.addOptional<std::string>("processName", "");

  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(L1GTBoardWriter);
