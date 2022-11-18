import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Phase2_cff import Phase2

process = cms.Process('L1TEmulation', Phase2)

############################################################
# import standard configurations
############################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
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
                                '/store/mc/Phase2HLTTDRWinter20DIGI/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/PU200_110X_mcRun4_realistic_v3-v2/110000/005E74D6-B50E-674E-89E6-EAA9A617B476.root',
                            )
)

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(20))

############################################################
# Raw to Digi
############################################################

process.load('Configuration.StandardSequences.RawToDigi_cff')

process.pRawToDigi = cms.Path(process.RawToDigi)

############################################################
# Upstream Emulators
############################################################

process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff') # needed to read HCal TPs

process.load('L1Trigger.TrackTrigger.TrackTrigger_cff')
process.load("L1Trigger.TrackFindingTracklet.L1HybridEmulationTracks_cff") 
process.load("L1Trigger.TrackerDTC.ProducerES_cff") 
process.load("L1Trigger.TrackerDTC.ProducerED_cff")

process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')

process.UpstreamEmulators = cms.Task(
    process.TrackerDTCProducer,
    process.TTClustersFromPhase2TrackerDigis,
    process.TTStubsFromPhase2TrackerDigis,
    process.offlineBeamSpot,
    process.TTTracksFromTrackletEmulation,
    process.TTTracksFromExtendedTrackletEmulation,
    process.SimL1EmulatorTask
)
 
process.pUpstreamEmulators = cms.Path(process.UpstreamEmulators)

############################################################
# L1 Global Trigger Emulation
############################################################

# Conditions
from L1Trigger.Phase2L1GT.L1GTSingleObjectCond_cfi import L1GTSingleObjectCond
from L1Trigger.Phase2L1GT.L1GTDoubleObjectCond_cfi import L1GTDoubleObjectCond
from L1Trigger.Phase2L1GT.L1GTTripleObjectCond_cfi import L1GTTripleObjectCond
from L1Trigger.Phase2L1GT.L1GTQuadObjectCond_cfi import L1GTQuadObjectCond

# Some dummy seed to test tracker interface
process.DoubleJetCondition = L1GTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GTTPromptJets"),
        minPt = cms.double(12)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GTTDisplacedJets"),
        minPt = cms.double(10)
    )
)

process.TripleJetCondition = L1GTTripleObjectCond.clone(
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


# B-physics seeds from https://twiki.cern.ch/twiki/pub/CMS/PhaseIIL1TriggerMenuTools/L1Menu_L1TDR_270121.pdf
process.doubleTkMuon1 = L1GTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(2),
        minEta = cms.double(-1.5),
        maxEta = cms.double(1.5)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(2),
        minEta = cms.double(-1.5),
        maxEta = cms.double(1.5)
    ),
    maxDR = cms.double(1.4),
    maxDz = cms.double(1),
    os = cms.bool(True)
)
process.pDoubleTkMuon1 = cms.Path(process.doubleTkMuon1)

process.doubleTkMuon2 = L1GTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(4),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(4),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    maxDR = cms.double(1.2),
    maxDz = cms.double(1),
    os = cms.bool(True)
)
process.pDoubleTkMuon2 = cms.Path(process.doubleTkMuon2)

process.doubleTkMuon3 = L1GTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(4.5),
        minEta = cms.double(-2.0),
        maxEta = cms.double(2.0)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(4.5),
        minEta = cms.double(-2.0),
        maxEta = cms.double(2.0)
    ),
    minInvMass = cms.double(7),
    maxInvMass = cms.double(18),
    maxDz = cms.double(1),
    os = cms.bool(True)
)
process.pDoubleTkMuon3 = cms.Path(process.doubleTkMuon3)


process.tripleTkMuon1 = L1GTTripleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(5),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(3),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection3 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(2),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    delta12 = cms.PSet(
        os = cms.bool(True),
        minInvMass = cms.double(0),
        maxInvMass = cms.double(9),
        maxDz = cms.double(1)
    ),
    delta13 = cms.PSet(
        maxDz = cms.double(1)
    ),
    delta23 = cms.PSet(
        maxDz = cms.double(1)
    )
)
process.pTripleTkMuon1 = cms.Path(process.tripleTkMuon1)


process.tripleTkMuon2 = L1GTTripleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(5),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(3),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection3 = cms.PSet(
        tag = cms.InputTag("L1GTProducer", "GMTTkMuons"),
        minPt = cms.double(2),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    delta12 = cms.PSet(
        os = cms.bool(True),
        maxDz = cms.double(1)
    ),
    delta13 = cms.PSet(
        minInvMass = cms.double(5),
        maxInvMass = cms.double(17),
        maxDz = cms.double(1)
    ),
    delta23 = cms.PSet(
        maxDz = cms.double(1)
    )
)
process.pTripleTkMuon2 = cms.Path(process.tripleTkMuon2)


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
