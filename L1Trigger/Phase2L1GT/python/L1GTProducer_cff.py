import FWCore.ParameterSet.Config as cms

L1GTProducer = cms.EDProducer(
    "L1GTProducer",
    GTTPromptJets = cms.InputTag("L1TrackJetsEmulation", "L1TrackJets"),
    GTTDisplacedJets = cms.InputTag("L1TrackJetsExtendedEmulation", "L1TrackJetsExtended"),
    GTTPrimaryVert = cms.InputTag("L1VertexFinderEmulator", "l1verticesEmulation"),
    GMTSaPromptMuons = cms.InputTag("L1SAMuonsGmt", "promptSAMuons"),
    GMTSaDisplacedMuons = cms.InputTag("L1SAMuonsGmt", "displacedSAMuons"),
    GMTTkMuons = cms.InputTag("L1TkMuonsGmt"),
    CL2Jets = cms.InputTag("scPFL1PuppiCorrectedEmulator"),
    CL2Electrons = cms.InputTag("l1ctLayer2EG", "L1CtTkElectron"),
    CL2Photons = cms.InputTag("l1ctLayer2EG", "L1CtTkEm"),
    CL2EtSum = cms.InputTag("L1MetPfProducer"),
    CL2HtSum = cms.InputTag("scPFL1PuppiCorrectedEmulatorMHT")
)
