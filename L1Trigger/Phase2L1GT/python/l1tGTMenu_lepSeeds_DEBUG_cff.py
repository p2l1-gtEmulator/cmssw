import FWCore.ParameterSet.Config as cms

############################################################
# L1 Global Trigger Emulation
############################################################

# Conditions

from L1Trigger.Phase2L1GT.l1tGTProducer_cff import l1tGTProducer

from L1Trigger.Phase2L1GT.l1tGTSingleObjectCond_cfi import l1tGTSingleObjectCond
from L1Trigger.Phase2L1GT.l1tGTDoubleObjectCond_cfi import l1tGTDoubleObjectCond
from L1Trigger.Phase2L1GT.l1tGTTripleObjectCond_cfi import l1tGTTripleObjectCond
from L1Trigger.Phase2L1GT.l1tGTQuadObjectCond_cfi import l1tGTQuadObjectCond

from L1Trigger.Phase2L1GT.l1tGTAlgoBlockProducer_cff import algorithms

####### TK EG and PHO seeds ###########

SingleIsoTkEle28Barrel = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(12), 
    minEta = cms.double(-1.479),
    maxEta = cms.double(1.479),
    #maxIso = cms.double(0.13),
)
pSingleIsoTkEle28Barrel = cms.Path(SingleIsoTkEle28Barrel)
#algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28Barrel")))

SingleIsoTkEle28EndcapAbs = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(12),
    minEtaAbs = cms.double(1.479),
    maxEtaAbs = cms.double(2.4),
    #qual = cms.vuint32(0b0010),
    #maxIso = cms.double(0.28)
)
pSingleIsoTkEle28EndcapAbs = cms.Path(SingleIsoTkEle28EndcapAbs) 
algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28EndcapAbs")))

algorithms.append(cms.PSet(name=cms.string("pSingleIsoTkEle28"),
                       expression=cms.string("pSingleIsoTkEle28Barrel or pSingleIsoTkEle28EndcapAbs")))

SingleIsoTkEle28EndcapPos = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(12),
    minEta = cms.double(1.479),
    maxEta = cms.double(2.4),
    #qual = cms.vuint32(0b0010),
    #maxIso = cms.double(0.28)
)
pSingleIsoTkEle28EndcapPos = cms.Path(SingleIsoTkEle28EndcapPos) 

SingleIsoTkEle28EndcapNeg = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(12),
    maxEta = cms.double(-1.479),
    minEta = cms.double(-2.4),
    #qual = cms.vuint32(0b0010),
    #maxIso = cms.double(0.28)
)
pSingleIsoTkEle28EndcapNeg = cms.Path(SingleIsoTkEle28EndcapNeg) 

algorithms.append(cms.PSet(name=cms.string("pSingleIsoTkEle28EndcapOR"),
                       expression=cms.string("pSingleIsoTkEle28EndcapPos or pSingleIsoTkEle28EndcapNeg")))

algorithms.append(cms.PSet(name=cms.string("pSingleIsoTkEle28OR"),
                       expression=cms.string("pSingleIsoTkEle28Barrel or pSingleIsoTkEle28EndcapPos or pSingleIsoTkEle28EndcapNeg")))

