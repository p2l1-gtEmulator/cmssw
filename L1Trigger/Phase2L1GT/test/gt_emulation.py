import FWCore.ParameterSet.Config as cms

process = cms.Process('L1TEmulation')

############################################################
# import standard configurations
############################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.Geometry.GeometryExtended2026D77Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D77_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag

process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.INFO.limit = cms.untracked.int32(0)  # default: 0

############################################################
# Source
############################################################

process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring(
                                '/store/relval/CMSSW_12_3_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v3_2026D77PU200-v1/2580000/c6df2819-ed05-4b98-8f92-81b7d1b1092e.root',
                                '/store/relval/CMSSW_12_3_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v3_2026D77PU200-v1/2580000/3f476d95-1ef7-4be6-977b-6bcd1a7c5678.root',
                                '/store/relval/CMSSW_12_3_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v3_2026D77PU200-v1/2580000/68d651da-4cb7-4bf4-b002-66aecc57a2bc.root',
                                '/store/relval/CMSSW_12_3_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v3_2026D77PU200-v1/2580000/db0e0ce2-4c5a-4988-9dbd-52066e40b9d2.root',
                                '/store/relval/CMSSW_12_3_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v3_2026D77PU200-v1/2580000/257a9712-0a96-47b7-897e-f5d980605e46.root',
                                '/store/relval/CMSSW_12_3_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v3_2026D77PU200-v1/2580000/bee31399-8559-4243-b539-cae1ea897def.root',
                                '/store/relval/CMSSW_12_3_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v3_2026D77PU200-v1/2580000/24629540-2377-4168-9ae5-518ddd4c43a9.root',
                                '/store/relval/CMSSW_12_3_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v3_2026D77PU200-v1/2580000/e31ba8f0-332a-4a1a-8bc0-91a12a5fe3db.root',
                                '/store/relval/CMSSW_12_3_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v3_2026D77PU200-v1/2580000/17902198-4db6-4fcc-9e8c-787991b4db32.root',
                            ),
                            duplicateCheckMode=cms.untracked.string('noDuplicateCheck'),
                            inputCommands=cms.untracked.vstring(
                                "keep *", "drop l1tTkPrimaryVertexs_L1TkPrimaryVertex__*")
                            )

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(30))

############################################################
# L1 Global Track Trigger Emulation
############################################################

from SimTracker.TrackTriggerAssociation.TTClusterAssociation_cfi import *
from L1Trigger.TrackTrigger.TTStubAlgorithmRegister_cfi import *

process.load('L1Trigger.TrackTrigger.TrackTrigger_cff')

# DTC emulation
process.load('L1Trigger.TrackerDTC.ProducerES_cff')
process.load('L1Trigger.TrackerDTC.ProducerED_cff')
process.dtc = cms.Path(process.TrackerDTCProducer)  # *process.TrackerDTCAnalyzer)

process.load("L1Trigger.TrackFindingTracklet.L1HybridEmulationTracks_cff")
process.load("L1Trigger.L1TTrackMatch.L1TrackSelectionProducer_cfi")
process.load("L1Trigger.L1TTrackMatch.L1GTTInputProducer_cfi")
process.load("L1Trigger.L1TTrackMatch.L1TrackJetEmulationProducer_cfi")
process.load("L1Trigger.L1TTrackMatch.L1TrackerEtMissEmulatorProducer_cfi")
process.load("L1Trigger.L1TTrackMatch.L1TkHTMissEmulatorProducer_cfi")
process.load('L1Trigger.VertexFinder.VertexProducer_cff')

process.L1VertexFinder = process.VertexProducer.clone()
process.pPV = cms.Path(process.L1VertexFinder)
process.L1VertexFinderEmulator = process.VertexProducer.clone()
process.L1VertexFinderEmulator.VertexReconstruction.Algorithm = "fastHistoEmulation"
process.L1VertexFinderEmulator.l1TracksInputTag = cms.InputTag("L1GTTInputProducer", "Level1TTTracksConverted")
process.L1VertexFinderEmulator.VertexReconstruction.VxMinTrackPt = cms.double(0.0)
process.pPVemu = cms.Path(process.L1VertexFinderEmulator)

process.L1TrackerEmuEtMiss.L1VertexInputTag = cms.InputTag("L1VertexFinderEmulator", "l1verticesEmulation")

process.TTTracksEmu = cms.Path(process.L1PromptExtendedHybridTracks)
process.TTTracksEmuWithTruth = cms.Path(process.L1PromptExtendedHybridTracksWithAssociators)
process.pL1TrackSelection = cms.Path(process.L1TrackSelectionProducer*process.L1TrackSelectionProducerExtended)
process.pL1GTTInput = cms.Path(process.L1GTTInputProducer*process.L1GTTInputProducerExtended)
process.pL1TrackJetsEmu = cms.Path(process.L1TrackJetsEmulation*process.L1TrackJetsExtendedEmulation)
process.pTkMETEmu = cms.Path(process.L1TrackerEmuEtMiss)
process.pTkMHTEmulator = cms.Path(process.L1TrackerEmuHTMiss*process.L1TrackerEmuHTMissExtended)

############################################################
# L1 Global Trigger Emulation
############################################################

process.L1GTProducer = cms.EDProducer(
    "L1GTProducer",
    GTTPromptJets = cms.InputTag("L1TrackJetsEmulation", "L1TrackJets"),
    GTTDisplacedJets = cms.InputTag("L1TrackJetsExtendedEmulation", "L1TrackJetsExtended"),
    GTTPrimaryVert = cms.InputTag("L1VertexFinderEmulator", "l1verticesEmulation")
)
process.pL1GTProducer = cms.Path(process.L1GTProducer)

# Conditions
from L1Trigger.Phase2L1GT.l1GTSingleObjectCond_cfi import l1GTSingleObjectCond
from L1Trigger.Phase2L1GT.l1GTDoubleObjectCond_cfi import l1GTDoubleObjectCond
from L1Trigger.Phase2L1GT.l1GTTripleObjectCond_cfi import l1GTTripleObjectCond
from L1Trigger.Phase2L1GT.l1GTQuadObjectCond_cfi import l1GTQuadObjectCond


process.DoubleJetCondition = l1GTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GTTPromptJets"),
        minPt = cms.double(12)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GTTDisplacedJets"),
        minPt = cms.double(10)
    )
)

process.TripleJetCondition = l1GTTripleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GTTPromptJets"),
        minPt = cms.double(50)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GTTPromptJets"),
        minPt = cms.double(40)
    ),
    collection3 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GTTPromptJets"),
        minPt = cms.double(25)
    )
)

process.pDoubleJetCondition = cms.Path(process.DoubleJetCondition)
process.pTripleJetCondition = cms.Path(process.TripleJetCondition)

############################################################
# Analyzable output
############################################################

process.out = cms.OutputModule("PoolOutputModule",
outputCommands = cms.untracked.vstring('drop *',
        'keep *_*_*_L1TEmulation'
    ),
    fileName=cms.untracked.string("l1t_emulation.root")
)

process.pOut = cms.EndPath(process.out)
