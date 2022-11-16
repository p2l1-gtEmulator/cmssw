import FWCore.ParameterSet.Config as cms

L1GTProducer = cms.EDProducer(
    "L1GTProducer",
    GTTPromptJets = cms.InputTag("L1TrackJetsEmulation", "L1TrackJets"),
    GTTDisplacedJets = cms.InputTag("L1TrackJetsExtendedEmulation", "L1TrackJetsExtended"),
    GTTPrimaryVert = cms.InputTag("L1VertexFinderEmulator", "l1verticesEmulation"),
    GMTSaPromptMuons = cms.InputTag("L1SAMuonsGmt", "promptSAMuons"),
    GMTSaDisplacedMuons = cms.InputTag("L1SAMuonsGmt", "displacedSAMuons"),
    GMTTkMuons = cms.InputTag("L1TkMuonsGmt")
)
