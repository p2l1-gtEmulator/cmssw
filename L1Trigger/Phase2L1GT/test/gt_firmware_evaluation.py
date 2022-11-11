import FWCore.ParameterSet.Config as cms

process = cms.Process('L1Test')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')


# Input source
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(72))


process.GTProducer = cms.EDProducer(
    "L1GTEvaluationProducer",
    outputFilename=cms.string("inputPattern"),
    random_seed=cms.uint32(0),
    maxLines=cms.uint32(1024),
    platform=cms.string("VU9P")
)

process.l1t_GTProducer = cms.Path(process.GTProducer)

from L1Trigger.Phase2L1GT.l1GTSingleInOutLUT import COSH_ETA_LUT, COSH_ETA_LUT_2, COS_PHI_LUT

COSH_ETA_LUT.export("coshEtaLUT.mem")
COSH_ETA_LUT_2.export("coshEtaLUT2.mem")
COS_PHI_LUT.export("cosPhiLUT.mem")

from L1Trigger.Phase2L1GT.l1GTSingleObjectCond_cfi import l1GTSingleObjectCond
from L1Trigger.Phase2L1GT.l1GTDoubleObjectCond_cfi import l1GTDoubleObjectCond
from L1Trigger.Phase2L1GT.l1GTTripleObjectCond_cfi import l1GTTripleObjectCond
from L1Trigger.Phase2L1GT.l1GTQuadObjectCond_cfi import l1GTQuadObjectCond

l1GTDoubleObjectCond.sanity_checks = cms.untracked.bool(True)
l1GTDoubleObjectCond.inv_mass_checks = cms.untracked.bool(True)

# Conditions

process._singleTkMu_14_er2p3 = l1GTSingleObjectCond.clone(
    tag=cms.InputTag("GTProducer", "GMTTkMuons"),
    minPt=cms.double(14),
    minEta=cms.double(-2.3),
    maxEta=cms.double(2.3),
)

process._doubleJet_3_9_dEta_Max1p6_OS = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTJets"),
        minPt=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTJets"),
        minPt=cms.double(9),
    ),
    maxDEta=cms.double(1.6),
)

process._doubleTau_5_9_q2_4_SS = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(5),
        # qual=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(9),
        # qual=cms.double(4),
    ),
    ss=cms.bool(True),
)

process._doubleMu_11_9_q2_4 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(11),
        # qual_cut=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(9),
        # qual_cut=cms.double(4),
    ),
)

process._doubleMuEl_11_9_q2_4_OS = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(11),
        # qual_cut=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(9),
        # qual_cut=cms.double(4),
    ),
    os=cms.bool(True),
)

process._doubleMu_11_9_combPt_19 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(9),
    ),
    minPt=cms.double(19)
)

process._doubleMuEl_11_9_SS = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(9),
    ),
    ss=cms.bool(True),
)

process._doubleJetGamma_11_9_pr_0p2to1p8_1to3 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTIsoEg"),
        minPt=cms.double(11),
        minPhi=cms.double(0.2),
        maxPhi=cms.double(1.8),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTJets"),
        minPt=cms.double(9),
        minPhi=cms.double(1),
        maxPhi=cms.double(3),
    ),
)

process._doubleMuTau_2_9_er_1to3_3to3p3 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(2),
        minEta=cms.double(1),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(9),
        minEta=cms.double(3),
        maxEta=cms.double(3.3),
    ),
)

process._doubleMuEl_2_9_dEtaMin2 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(9),
    ),
    minDEta=cms.double(2),
)

process._doubleElGamma_2_9_dPhiMin2 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTIsoEg"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(9),
    ),
    minDPhi=cms.double(2),
)

process._doubleMuEl_2_9_dRMin2 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(9),
    ),
    minDR=cms.double(2),
)

process._doubleElTau_2_9_dEta0p2to2 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTTaus"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(9),
    ),
    minDEta=cms.double(0.2),
    maxDEta=cms.double(2),
)

process._doubleMuJet_2_9_dPhi2to4 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTJets"),
        minPt=cms.double(9),
    ),
    minDPhi=cms.double(2),
    maxDPhi=cms.double(4),
)

process._doubleMuEl_2_9_dR1to3 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Photons"),
        minPt=cms.double(9),
    ),
    minDR=cms.double(1),
    maxDR=cms.double(3),
)

process._doubleMuGamma_11_9_massMax10 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(11),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Photons"),
        minPt=cms.double(9),
    ),
    maxInvMass=cms.double(10),
)

process._doubleElMu_11_9_mass10to600 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(11),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(9),
    ),
    minInvMass=cms.double(10),
    maxInvMass=cms.double(600),
)

process._doubleTkMu_15_7_er2p4_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(15),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxDz=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxDz=cms.double(1.0),
    ),
)

process._tkIsoEleStaEG_22_12_er2p4 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTIsoEg"),
        minPt=cms.double(22),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTNonIsoEg"),
        minPt=cms.double(12),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkEle_25_12_er2p4 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTNonIsoEg"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTNonIsoEg"),
        minPt=cms.double(12),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleStaEG_37_24_er2p4 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GTTBsCandidates"),
        minPt=cms.double(37),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GTTBsCandidates"),
        minPt=cms.double(24),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkIsoPhoton_22_12_er2p4 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTIsoEg"),
        minPt=cms.double(22),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTIsoEg"),
        minPt=cms.double(12),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleCaloTau_69_69_er2p1_drMin0p5 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTTaus"),
        minPt=cms.double(69),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTTaus"),
        minPt=cms.double(69),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doubleCaloTau_90_90_er2p1_drMin0p5 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTTaus"),
        minPt=cms.double(90),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTTaus"),
        minPt=cms.double(90),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPITau_36_36_er2p1_drMin0p5 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(36),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(36),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPITau_52_52_er2p1_drMin0p5 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(52),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(52),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPIJet_112_112_er2p4_dEtaMax1p6 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Jets"),
        minPt=cms.double(112),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Jets"),
        minPt=cms.double(112),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    maxDEta=cms.double(1.6),
)

process._tkMuonTkIsoEle_7_20_er2p4_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxDz=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(20),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxDz=cms.double(1.0),
    ),
)

process._tkMuonTkEle_7_23_er2p4_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxDz=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(23),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxDz=cms.double(1.0),
    ),
)

process._tkEleTkMuon_10_20_er2p4_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxDz=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(20),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxDz=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_27_18_er2p1_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(27),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(18),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minDz=cms.double(-1.0),
        maxDz=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_36_18_er2p1_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(36),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(18),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minDz=cms.double(-1.0),
        maxDz=cms.double(1.0),
    ),
)

process._tkIsoElePUPPItau_22_29_er2p1_drMin0p3_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(22),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minDz=cms.double(-1.0),
        maxDz=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(29),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(22),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minDz=cms.double(-1.0),
        maxDz=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(39),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(28),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        maxDz=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GTTPromptJets"),
        minPt=cms.double(40),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxDz=cms.double(1.0),
    ),
    minDR=cms.double(0.3),
)

process._doublePuppiJet_160_35_er5p0_massMin620 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Jets"),
        minPt=cms.double(160),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Jets"),
        minPt=cms.double(35),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    minInvMass=cms.double(620),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(2),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxDz=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(2),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxDz=cms.double(1.0),
    ),
    maxDR=cms.double(1.4),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p4_drMax1p2_OS_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxDz=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxDz=cms.double(1.0),
    ),
    maxDR=cms.double(1.2),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p0_massMin7_massMax18_OS_dzMax1p0 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxDz=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxDz=cms.double(1.0),
    ),
    minInvMass=cms.double(7),
    maxInvMass=cms.double(18),
    os=cms.bool(True),
)

process._doubleEG_32_32_er2p5_Mt40 = l1GTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTIsoEg"),
        minPt=cms.double(32),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GCTIsoEg"),
        minPt=cms.double(32),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    minTransMass=cms.double(40),
)


process._triplePuppiJet_70_50_35 = l1GTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Jets"),
        minPt=cms.double(70)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Jets"),
        minPt=cms.double(50)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Jets"),
        minPt=cms.double(35)
    )
)

process._tripleTkEleTkMuPUPPIJet_30_40_25_er2p4 = l1GTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(30),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(40),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Jets"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)

process._tripleTkMuTkEle_7_5_5_er3p4_SS = l1GTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(5),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    ss=cms.bool(True)
)

process._quadTkMuTkEle_5_5_5_7_er3p4_SS = l1GTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    ss=cms.bool(True)
)

process._quadTkEleTkMuPUPPIJet_30_40_25_25_er2p4 = l1GTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Electrons"),
        minPt=cms.double(30),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("GTProducer", "GMTTkMuons"),
        minPt=cms.double(40),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Jets"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("GTProducer", "CL2Taus"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)

channel_conf = {}
idx = 0
# remove '_', since it are not allowed for module names
for filt_name in process.filters:
    if filt_name[:1] != '_':
        continue
    new_name = filt_name.replace('_', '')
    setattr(process, new_name, getattr(process, filt_name).clone())
    delattr(process, filt_name)
    channel_conf[idx] = 'l1t' + filt_name
    setattr(process, 'l1t' + filt_name, cms.Path(getattr(process, new_name)))
    idx += 1


# Algo bits
from L1Trigger.Phase2L1GT.l1GTAlgoChannelConfig import generate_channel_config


process.BoardData = cms.EDAnalyzer("L1GTBoardWriter",
  outputFilename = cms.string("outputPattern"),
  maxLines = cms.uint32(1024),
  channelConfig = generate_channel_config({
        0 : channel_conf
    })
)

process.l1t_BoardData = cms.EndPath(process.BoardData)

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('file:test_output.root'),
    outputCommands = cms.untracked.vstring('keep *'),
    splitLevel = cms.untracked.int32(0)
)

process.output_step = cms.EndPath(process.output)
