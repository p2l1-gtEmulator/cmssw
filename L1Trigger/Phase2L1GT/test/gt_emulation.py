import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Phase2_cff import Phase2

process = cms.Process('L1TEmulation', Phase2)

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

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

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

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(100))

############################################################
# Upstream Emulators
############################################################

process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')

process.pUpstreamEmulators = cms.Path(process.SimL1Emulator)

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

# The menu
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
        'keep *_L1GTProducer_*_L1TEmulation',
        'keep l1tP2GTCandidatesl1tP2GTCandidatel1tP2GTCandidatesl1tP2GTCandidateedmrefhelperFindUsingAdvanceedmRefs_*_*_L1TEmulation',
        'keep *_TriggerResults_*_L1TEmulation'
    ),
    fileName=cms.untracked.string("l1t_emulation.root")
)

process.pOut = cms.EndPath(process.out)
