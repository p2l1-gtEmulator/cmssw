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
                                '/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/MinBias_TuneCP5_14TeV-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/110000/0016DCDC-FCE4-BC47-89AC-43EB1BB82D46.root',
                            ),
                            inputCommands = cms.untracked.vstring("keep *","drop l1tTkPrimaryVertexs_L1TkPrimaryVertex_*_*")
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
    process.l1tTTTracksFromTrackletEmulation,
    process.l1tTTTracksFromExtendedTrackletEmulation,
    process.SimL1EmulatorTask
)
 
process.pUpstreamEmulators = cms.Path(process.UpstreamEmulators)

############################################################
# L1 Global Trigger Emulation
############################################################

# Conditions
from L1Trigger.Phase2L1GT.l1tGTSingleObjectCond_cfi import l1tGTSingleObjectCond
from L1Trigger.Phase2L1GT.l1tGTDoubleObjectCond_cfi import l1tGTDoubleObjectCond
from L1Trigger.Phase2L1GT.l1tGTTripleObjectCond_cfi import l1tGTTripleObjectCond
from L1Trigger.Phase2L1GT.l1tGTQuadObjectCond_cfi import l1tGTQuadObjectCond

from L1Trigger.Phase2L1GT.l1tGTAlgoBlockProducer_cff import algorithms

####### SEED 1 ###########

process.SingleTkMuon22 = l1tGTSingleObjectCond.clone(
    tag =  cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    minPt = cms.double(22),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4)
)
process.pSingleTkMuon22 = cms.Path(process.SingleTkMuon22)
algorithms.append(cms.PSet(expression = cms.string("pSingleTkMuon22")))

####### SEED 2 ###########

process.DoubleTkMuon15x7 = l1tGTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(14),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(6),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    maxDz = cms.double(1),
)
process.pDoubleTkMuon15_7 = cms.Path(process.DoubleTkMuon15x7)
algorithms.append(cms.PSet(expression = cms.string("pDoubleTkMuon15_7")))

####### SEED 3 ###########

process.DoubleJet90x30 = l1tGTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt = cms.double(90)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt = cms.double(30)
    ),
)
process.pDoubleJet90_30 = cms.Path(process.DoubleJet90x30)

process.DoubleJet30MassMin620 = l1tGTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt = cms.double(30)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt = cms.double(30)
    ),
    minInvMass = cms.double(620)
)
process.pDoubleJet30_Mass_Min620 = cms.Path(process.DoubleJet30MassMin620)
algorithms.append(cms.PSet(name=cms.string("pDoubleJet_90_30_DoubleJet30_Mass_Min620"),
                       expression=cms.string("pDoubleJet90_30 and pDoubleJet30_Mass_Min620")))

############################################################
# Analyzable output
############################################################

process.out = cms.OutputModule("PoolOutputModule",
outputCommands = cms.untracked.vstring('drop *',
        'keep *_l1tGTProducer_*_L1TEmulation',
        'keep l1tP2GTCandidatesl1tP2GTCandidatel1tP2GTCandidatesl1tP2GTCandidateedmrefhelperFindUsingAdvanceedmRefs_*_*_L1TEmulation',
        'keep *_l1tGTAlgoBlockProducer_*_L1TEmulation',
        'keep *_TriggerResults_*_L1TEmulation'
    ),
    fileName=cms.untracked.string("l1t_emulation.root")
)

process.pOut = cms.EndPath(process.out)
