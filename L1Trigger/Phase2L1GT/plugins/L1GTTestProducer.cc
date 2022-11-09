#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/allowedValues.h"
#include "DataFormats/Common/interface/Handle.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/View.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"

#include "L1Trigger/DemonstratorTools/interface/BoardDataWriter.h"
#include "L1Trigger/DemonstratorTools/interface/utilities.h"

#include "L1GTTestInterface.h"

#include <vector>
#include <array>
#include <string>
#include <unordered_map>
#include <fstream>
#include <limits>

#include <optional>
#include <random>

using namespace l1t;

class L1GTTestProducer : public edm::one::EDProducer<> {
public:
  explicit L1GTTestProducer(const edm::ParameterSet &);
  ~L1GTTestProducer() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions &);

private:
  void produce(edm::Event &, const edm::EventSetup &) override;
  int nextValue(int mean = 1000, bool sign = false, int max = std::numeric_limits<int>::max());

  int nextPt() {
    return std::max<int>(0,
                         nextValue(300, false, (1 << P2GTCandidate::hwPT_t::width) - 1) +
                             std::normal_distribution<double>(0, 500)(randomGenerator_));
  }
  int nextEta() {
    return std::uniform_int_distribution<int>(-(1 << (P2GTCandidate::hwEta_t::width - 1)),
                                              (1 << (P2GTCandidate::hwEta_t::width - 1)) - 1)(randomGenerator_);
  }
  int nextPhi() {
    return std::uniform_int_distribution<int>(-(1 << (P2GTCandidate::hwPhi_t::width - 1)),
                                              (1 << (P2GTCandidate::hwPhi_t::width - 1)) - 1)(randomGenerator_);
  }

  void writeInputPatterns(
      const std::unordered_map<std::string, std::vector<std::unique_ptr<l1t::L1TGT_BaseInterface>>> &inputObjects);

  void endJob() override;

  std::mt19937 randomGenerator_;
  l1t::demo::BoardDataWriter boardDataWriter_;
};

template <typename T, std::size_t low, std::size_t high, std::size_t incr = 1>
static constexpr std::array<T, high - low> arange() {
  std::array<T, high - low> array;
  T value = low;
  for (T &el : array) {
    el = value;
    value += incr;
  }
  return array;
}

template <typename T, std::size_t low, std::size_t high, std::size_t incr = 1>
static std::vector<T> vrange() {
  std::array<T, high - low> arr(arange<T, low, high, incr>());
  return std::vector(std::begin(arr), std::end(arr));
}

static const l1t::demo::BoardDataWriter::ChannelMap_t CHANNEL_MAP_VU9P{
    {{"GTT", 0}, {{6, 0}, vrange<std::size_t, 0, 6>()}},
    {{"GTT", 1}, {{6, 0}, vrange<std::size_t, 6, 12>()}},
    {{"CL2", 0}, {{6, 0}, vrange<std::size_t, 28, 34>()}},
    {{"CL2", 1}, {{6, 0}, vrange<std::size_t, 34, 40>()}},
    {{"GCT", 0}, {{6, 0}, vrange<std::size_t, 54, 60>()}},
    {{"GMT", 0}, {{18, 0}, vrange<std::size_t, 60, 78>()}},
    {{"CL2", 2}, {{6, 0}, vrange<std::size_t, 80, 86>()}},
    {{"GTT", 2}, {{6, 0}, vrange<std::size_t, 104, 110>()}},
    {{"GTT", 3}, {{6, 0}, vrange<std::size_t, 110, 116>()}}};

static const l1t::demo::BoardDataWriter::ChannelMap_t CHANNEL_MAP_VU13P{
    {{"GTT", 0}, {{6, 0}, vrange<std::size_t, 0, 6>()}},
    {{"GTT", 1}, {{6, 0}, vrange<std::size_t, 6, 12>()}},
    {{"GCT", 0}, {{6, 0}, vrange<std::size_t, 24, 30>()}},
    {{"CL2", 0}, {{6, 0}, vrange<std::size_t, 32, 38>()}},
    {{"CL2", 1}, {{6, 0}, vrange<std::size_t, 38, 44>()}},
    {{"GMT", 0}, {{18, 0}, {48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 68, 69, 70, 71, 72, 73}}},
    {{"CL2", 2}, {{6, 0}, vrange<std::size_t, 80, 86>()}},
    {{"GTT", 2}, {{6, 0}, vrange<std::size_t, 112, 118>()}},
    {{"GTT", 3}, {{6, 0}, vrange<std::size_t, 118, 124>()}}};

L1GTTestProducer::L1GTTestProducer(const edm::ParameterSet &config)
    : randomGenerator_(config.exists("random_seed") ? config.getParameter<unsigned int>("random_seed")
                                                    : std::random_device()()),
      boardDataWriter_(l1t::demo::FileFormat::EMP,
                       config.getParameter<std::string>("outputFilename"),
                       9,
                       1,
                       config.exists("maxLines") ? config.getParameter<unsigned int>("maxLines") : 1024,
                       config.getParameter<std::string>("platform") == "VU13P" ? CHANNEL_MAP_VU13P : CHANNEL_MAP_VU9P) {
  produces<P2GTCandidateCollection>("GCT NonIsoEg");
  produces<P2GTCandidateCollection>("GCT IsoEg");
  produces<P2GTCandidateCollection>("GCT Jets");
  produces<P2GTCandidateCollection>("GCT Taus");
  produces<P2GTCandidateCollection>("GCT HtSum");
  produces<P2GTCandidateCollection>("GCT EtSum");
  produces<P2GTCandidateCollection>("GMT SaPromptMuons");
  produces<P2GTCandidateCollection>("GMT SaDisplacedMuons");
  produces<P2GTCandidateCollection>("GMT TkMuons");
  produces<P2GTCandidateCollection>("GMT Topo");
  produces<P2GTCandidateCollection>("GTT PromptJets");
  produces<P2GTCandidateCollection>("GTT DisplacedJets");
  produces<P2GTCandidateCollection>("GTT PhiCandidates");
  produces<P2GTCandidateCollection>("GTT RhoCandidates");
  produces<P2GTCandidateCollection>("GTT BsCandidates");
  produces<P2GTCandidateCollection>("GTT HadronicTaus");
  produces<P2GTCandidateCollection>("GTT PrimaryVert");
  produces<P2GTCandidateCollection>("GTT PromptHtSum");
  produces<P2GTCandidateCollection>("GTT DisplacedHtSum");
  produces<P2GTCandidateCollection>("GTT EtSum");
  produces<P2GTCandidateCollection>("CL2 Jets");
  produces<P2GTCandidateCollection>("CL2 Taus");
  produces<P2GTCandidateCollection>("CL2 Electrons");
  produces<P2GTCandidateCollection>("CL2 Photons");
  produces<P2GTCandidateCollection>("CL2 HtSum");
  produces<P2GTCandidateCollection>("CL2 EtSum");
}

void L1GTTestProducer::fillDescriptions(edm::ConfigurationDescriptions &description) {
  edm::ParameterSetDescription desc;
  desc.addOptional<unsigned int>("random_seed");
  desc.addOptional<unsigned int>("maxLines", 1024);
  desc.addOptional<std::string>("outputFilename");
  desc.ifValue(edm::ParameterDescription<std::string>("platform", "VU9P", true),
               edm::allowedValues<std::string>("VU9P", "VU13P"));
  description.addWithDefaultLabel(desc);
}

int L1GTTestProducer::nextValue(int mean, bool sign, int max) {
  bool positive = sign ? std::bernoulli_distribution(0.5)(randomGenerator_) : true;

  int result;
  do {
    result = std::poisson_distribution<int>(mean)(randomGenerator_);
  } while (result > max);

  return positive ? result : -result;
}

template <typename... Args>
static std::vector<ap_uint<64>> vpack(const Args &...vobjects) {
  std::vector<ap_uint<64>> vpacked;

  (
      [&vpacked](const std::vector<std::unique_ptr<l1t::L1TGT_BaseInterface>> &objects) {
        std::optional<ap_uint<64>> next_packed;
        for (const auto &object : objects) {
          if (object->packed_width() == 64) {
            const l1t::L1TGT_Interface<64> &interface_obj = dynamic_cast<const l1t::L1TGT_Interface<64> &>(*object);
            vpacked.emplace_back(interface_obj.pack());
          } else if (object->packed_width() == 96) {
            const l1t::L1TGT_Interface<96> &interface_obj = dynamic_cast<const l1t::L1TGT_Interface<96> &>(*object);
            ap_uint<96> packed = interface_obj.pack();
            if (next_packed.has_value()) {
              vpacked.emplace_back(packed(95, 64) << 32 | next_packed.value());
              next_packed.reset();
            } else {
              next_packed = packed(95, 64);
            }

            vpacked.emplace_back(packed(63, 0));

          } else if (object->packed_width() == 128) {
            const l1t::L1TGT_Interface<128> &interface_obj = dynamic_cast<const l1t::L1TGT_Interface<128> &>(*object);
            ap_uint<128> packed = interface_obj.pack();
            vpacked.emplace_back(packed(63, 0));
            vpacked.emplace_back(packed(127, 64));
          }
        }
      }(vobjects),
      ...);

  return vpacked;
}

void L1GTTestProducer::writeInputPatterns(
    const std::unordered_map<std::string, std::vector<std::unique_ptr<l1t::L1TGT_BaseInterface>>> &inputObjects) {
  boardDataWriter_.addEvent(l1t::demo::EventData{
      {{{"GTT", 0},
        vpack(inputObjects.at("GTT PromptJets"),
              inputObjects.at("GTT DisplacedJets"),
              inputObjects.at("GTT PromptHtSum"),
              inputObjects.at("GTT DisplacedHtSum"),
              inputObjects.at("GTT EtSum"))},
       {{"GTT", 1}, vpack(inputObjects.at("GTT HadronicTaus"))},
       {{"CL2", 0}, vpack(inputObjects.at("CL2 Jets"), inputObjects.at("CL2 HtSum"), inputObjects.at("CL2 EtSum"))},
       {{"CL2", 1}, vpack(inputObjects.at("CL2 Taus"))},
       {{"GCT", 0},
        vpack(inputObjects.at("GCT NonIsoEg"),
              inputObjects.at("GCT IsoEg"),
              inputObjects.at("GCT Jets"),
              inputObjects.at("GCT Taus"),
              inputObjects.at("GCT HtSum"),
              inputObjects.at("GCT EtSum"))},
       {{"GMT", 0},
        vpack(inputObjects.at("GMT SaPromptMuons"),
              inputObjects.at("GMT SaDisplacedMuons"),
              inputObjects.at("GMT TkMuons"),
              inputObjects.at("GMT Topo"))},
       {{"CL2", 2}, vpack(inputObjects.at("CL2 Electrons"), inputObjects.at("CL2 Photons"))},
       {{"GTT", 2},
        vpack(inputObjects.at("GTT PhiCandidates"),
              inputObjects.at("GTT RhoCandidates"),
              inputObjects.at("GTT BsCandidates"))},
       {{"GTT", 3}, vpack(inputObjects.at("GTT PrimaryVert"))}}});
}

void L1GTTestProducer::produce(edm::Event &event, const edm::EventSetup &setup) {
  // Generate random input objects
  std::unordered_map<std::string, std::vector<std::unique_ptr<l1t::L1TGT_BaseInterface>>> inputObjects;
  for (std::size_t i = 0; i < 12; ++i) {
    // Global Muon Trigger
    inputObjects["GMT SaPromptMuons"].emplace_back(std::make_unique<l1t::L1TGT_GMT_PromptDisplacedMuon>(
        true, nextPt(), nextEta(), nextPhi(), nextValue(), nextValue(), nextValue(), nextValue()));

    inputObjects["GMT SaDisplacedMuons"].emplace_back(std::make_unique<l1t::L1TGT_GMT_PromptDisplacedMuon>(
        true, nextPt(), nextEta(), nextPhi(), nextValue(), nextValue(), nextValue(), nextValue()));
    inputObjects["GMT TkMuons"].emplace_back(std::make_unique<l1t::L1TGT_GMT_TrackMatchedmuon>(true,
                                                                                               nextPt(),
                                                                                               nextEta(),
                                                                                               nextPhi(),
                                                                                               nextValue(),
                                                                                               nextValue(),
                                                                                               nextValue(),
                                                                                               nextValue(),
                                                                                               nextValue(),
                                                                                               nextValue()));
    inputObjects["GMT Topo"].emplace_back(
        std::make_unique<l1t::L1TGT_GMT_TopoObject>(true, nextPt(), nextEta(), nextPhi(), nextValue(), nextValue()));

    // Global Calorimeter Trigger
    inputObjects["GCT NonIsoEg"].emplace_back(
        std::make_unique<l1t::L1TGT_GCT_EgammaNonIsolated6p6>(true, nextPt(), nextEta(), nextPhi()));
    inputObjects["GCT IsoEg"].emplace_back(
        std::make_unique<l1t::L1TGT_GCT_EgammaIsolated6p6>(true, nextPt(), nextEta(), nextPhi()));
    inputObjects["GCT Jets"].emplace_back(
        std::make_unique<l1t::L1TGT_GCT_jet6p6>(true, nextPt(), nextEta(), nextPhi()));
    inputObjects["GCT Taus"].emplace_back(
        std::make_unique<l1t::L1TGT_GCT_tau6p6>(true, nextPt(), nextEta(), nextPhi(), nextValue()));

    // Global Track Trigger
    inputObjects["GTT PrimaryVert"].emplace_back(
        std::make_unique<l1t::L1TGT_GTT_PrimaryVert>(true, nextPt(), nextEta(), nextPhi(), nextValue(), nextValue()));
    inputObjects["GTT PromptJets"].emplace_back(
        std::make_unique<l1t::L1TGT_GTT_PromptJet>(true, nextPt(), nextEta(), nextPhi(), nextValue(), nextValue()));
    inputObjects["GTT DisplacedJets"].emplace_back(std::make_unique<l1t::L1TGT_GTT_DisplacedJet>(
        true, nextPt(), nextEta(), nextPhi(), nextValue(), nextValue(), nextValue()));
    inputObjects["GTT HadronicTaus"].emplace_back(std::make_unique<l1t::L1TGT_GTT_HadronicTau>(
        true, nextPt(), nextEta(), nextPhi(), nextValue(), nextValue(), nextValue(), nextValue()));
    inputObjects["GTT PhiCandidates"].emplace_back(
        std::make_unique<l1t::L1TGT_GTT_LightMeson>(true, nextPt(), nextEta(), nextPhi(), nextValue()));
    inputObjects["GTT RhoCandidates"].emplace_back(
        std::make_unique<l1t::L1TGT_GTT_LightMeson>(true, nextPt(), nextEta(), nextPhi(), nextValue()));
    inputObjects["GTT BsCandidates"].emplace_back(
        std::make_unique<l1t::L1TGT_GTT_LightMeson>(true, nextPt(), nextEta(), nextPhi(), nextValue()));

    // Correlator Layer-2
    inputObjects["CL2 Jets"].emplace_back(
        std::make_unique<l1t::L1TGT_CL2_Jet>(true, nextPt(), nextEta(), nextPhi(), nextValue()));
    inputObjects["CL2 Electrons"].emplace_back(std::make_unique<l1t::L1TGT_CL2_Electron>(
        true, nextPt(), nextEta(), nextPhi(), nextValue(), nextValue(), nextValue(), nextValue()));
    inputObjects["CL2 Photons"].emplace_back(
        std::make_unique<l1t::L1TGT_CL2_Photon>(true, nextPt(), nextEta(), nextPhi(), nextValue(), nextValue()));
    inputObjects["CL2 Taus"].emplace_back(std::make_unique<l1t::L1TGT_CL2_Tau>(
        true, nextPt(), nextEta(), nextPhi(), nextValue(), nextValue(), nextValue(), nextValue()));
  }

  inputObjects["CL2 HtSum"].emplace_back(
      std::make_unique<l1t::L1TGT_CL2_Sum>(true, nextValue(), nextValue(), nextValue()));
  inputObjects["CL2 EtSum"].emplace_back(
      std::make_unique<l1t::L1TGT_CL2_Sum>(true, nextValue(), nextValue(), nextValue()));
  inputObjects["GCT HtSum"].emplace_back(
      std::make_unique<l1t::L1TGT_GCT_Sum2>(true, nextValue(), nextValue(), nextValue()));
  inputObjects["GCT EtSum"].emplace_back(
      std::make_unique<l1t::L1TGT_GCT_Sum2>(true, nextValue(), nextValue(), nextValue()));

  inputObjects["GTT PromptHtSum"].emplace_back(
      std::make_unique<l1t::L1TGT_GTT_Sum>(true, nextValue(), nextValue(), nextValue()));
  inputObjects["GTT DisplacedHtSum"].emplace_back(
      std::make_unique<l1t::L1TGT_GTT_Sum>(true, nextValue(), nextValue(), nextValue()));
  inputObjects["GTT EtSum"].emplace_back(
      std::make_unique<l1t::L1TGT_GTT_Sum>(true, nextValue(), nextValue(), nextValue()));

  // Write them to a pattern file
  writeInputPatterns(inputObjects);

  for (const auto &[key, inputCollection] : inputObjects) {
    std::unique_ptr<P2GTCandidateCollection> gtCollection = std::make_unique<P2GTCandidateCollection>();
    for (const auto &object : inputCollection) {
      gtCollection->emplace_back(object->to_GTObject());
    }

    event.put(std::move(gtCollection), key);
  }
}

void L1GTTestProducer::endJob() { boardDataWriter_.flush(); }

DEFINE_FWK_MODULE(L1GTTestProducer);
