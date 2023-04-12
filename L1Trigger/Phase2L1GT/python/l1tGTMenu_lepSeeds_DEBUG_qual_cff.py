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

SingleIsoTkEle28Endcap = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(12),
    minEtaAbs = cms.double(1.479),
    maxEtaAbs = cms.double(2.4),
    qual = cms.vuint32(0b0010,0b0011,0b0110,0b1010,0b0111,0b1011,0b1110,0b1111), #cms.vuint32(0b0010),
    maxIso = cms.double(0.28)
)
pSingleIsoTkEle28Endcap = cms.Path(SingleIsoTkEle28Endcap) 
algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28Endcap")))

SingleIsoTkEle28Pt = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(12),
    #minEtaAbs = cms.double(1.479),
    #maxEtaAbs = cms.double(2.4),
    #qual = cms.vuint32(0b0010,0b0011,0b0110,0b1010,0b0111,0b1011,0b1110,0b1111),
    #maxIso = cms.double(0.28)
)
pSingleIsoTkEle28Pt = cms.Path(SingleIsoTkEle28Pt) 
algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28Pt")))

SingleIsoTkEle28EndcapBare = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(12),
    minEtaAbs = cms.double(1.479),
    maxEtaAbs = cms.double(2.4),
    #qual = cms.vuint32(0b0010,0b0011,0b0110,0b1010,0b0111,0b1011,0b1110,0b1111),
    #maxIso = cms.double(0.28)
)
pSingleIsoTkEle28EndcapBare = cms.Path(SingleIsoTkEle28EndcapBare) 
algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28EndcapBare")))


SingleIsoTkEle28EndcapIso = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(12),
    minEtaAbs = cms.double(1.479),
    maxEtaAbs = cms.double(2.4),
    #qual = cms.vuint32(0b0010,0b0011,0b0110,0b1010,0b0111,0b1011,0b1110,0b1111),
    maxIso = cms.double(0.28)
)
pSingleIsoTkEle28EndcapIso = cms.Path(SingleIsoTkEle28EndcapIso) 
algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28EndcapIso")))

SingleIsoTkEle28EndcapQual = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(12),
    minEtaAbs = cms.double(1.479),
    maxEtaAbs = cms.double(2.4),
    qual = cms.vuint32(0b0010,0b0011,0b0110,0b1010,0b0111,0b1011,0b1110,0b1111),
    #maxIso = cms.double(0.28)
)
pSingleIsoTkEle28EndcapQual = cms.Path(SingleIsoTkEle28EndcapQual) 
algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28EndcapQual")))


#algorithms.append(cms.PSet(name=cms.string("pSingleIsoTkEle28"),
#                       expression=cms.string("pSingleIsoTkEle28Barrel or pSingleIsoTkEle28Endcap")))

