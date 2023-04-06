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

####### MUON SEEDS ###########

SingleTkMuon22 = l1tGTSingleObjectCond.clone(
    tag =  cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    minPt = cms.double(20.3),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4)
)
pSingleTkMuon22 = cms.Path(SingleTkMuon22)
algorithms.append(cms.PSet(expression = cms.string("pSingleTkMuon22")))

DoubleTkMuon157 = l1tGTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(13.6),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(5.9),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    maxDz = cms.double(1),
)
pDoubleTkMuon15_7 = cms.Path(DoubleTkMuon157)
algorithms.append(cms.PSet(expression = cms.string("pDoubleTkMuon15_7")))

TripleTkMuon533 = l1tGTTripleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(3.9),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(2),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection3 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(2),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    delta12 = cms.PSet(
        maxDz = cms.double(1)
    ),
    delta13 = cms.PSet(
        maxDz = cms.double(1)
    ),
    delta23 = cms.PSet(
        maxDz = cms.double(1)
    )
)
pTripleTkMuon5_3_3 = cms.Path(TripleTkMuon533)
algorithms.append(cms.PSet(expression = cms.string("pTripleTkMuon5_3_3")))

####### TK EG and PHO seeds ###########

SingleTkEle36 = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(29.9),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4),
    qual = cms.vuint32(0b0010)
)
pSingleTkEle36 = cms.Path(SingleTkEle36) 
algorithms.append(cms.PSet(expression = cms.string("pSingleTkEle36")))

SingleIsoTkEle28Barrel = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(23), 
    minEta = cms.double(-1.479),
    maxEta = cms.double(1.479),
    maxIso = cms.double(0.13),
)
pSingleIsoTkEle28Barrel = cms.Path(SingleIsoTkEle28Barrel)
algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28Barrel")))

SingleIsoTkEle28Endcap = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(23),
    minEtaAbs = cms.double(1.479),
    maxEtaAbs = cms.double(2.4),
    qual = cms.vuint32(0b0010),
    maxIso = cms.double(0.28)
)
pSingleIsoTkEle28Endcap = cms.Path(SingleIsoTkEle28Endcap) 
algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28Endcap")))

algorithms.append(cms.PSet(name=cms.string("pSingleIsoTkEle28"),
                       expression=cms.string("pSingleIsoTkEle28Barrel or pSingleIsoTkEle28Endcap")))


SingleIsoTkPho36Barrel = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
    minPt = cms.double(30.8),
    minEta = cms.double(-1.479), 
    maxEta = cms.double(1.479),
    qual = cms.vuint32(0b0010),
    maxIso = cms.double(0.25)
)
pSingleIsoTkPho36Barrel = cms.Path(SingleIsoTkPho36Barrel) 

SingleIsoTkPho36Endcap = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
    minPt = cms.double(30.8),
    minEtaAbs = cms.double(1.479),
    maxEtaAbs = cms.double(2.4),
    qual = cms.vuint32(0b0100),
    maxIso = cms.double(0.205)
)
pSingleIsoTkPho36Endcap = cms.Path(SingleIsoTkPho36Endcap) 

algorithms.append(cms.PSet(name=cms.string("pSingleIsoTkPho36"),
                       expression=cms.string("pSingleIsoTkPho36Barrel or pSingleIsoTkPho36Endcap")))

DoubleTkEle2512 = l1tGTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt = cms.double(20.6),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4),
        qual = cms.vuint32(0b0010)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt = cms.double(9.6),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4),
        qual = cms.vuint32(0b0010)
    ),
    maxDz = cms.double(1),
)
pDoubleTkEle25_12 = cms.Path(DoubleTkEle2512)
algorithms.append(cms.PSet(expression = cms.string("pDoubleTkEle25_12")))


#SingleIsoTkPho22Barrel = l1tGTSingleObjectCond.clone(
#    tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
#    minPt = cms.double(17.1),
#    minEta = cms.double(-1.479), 
#    maxEta = cms.double(1.479),
#    qual = cms.vuint32(0b0010),
#    maxIso = cms.double(0.25)
#)
#pSingleIsoTkPho22Barrel = cms.Path(SingleIsoTkPho22Barrel) 

#SingleIsoTkPho22Endcap = l1tGTSingleObjectCond.clone(
#    tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
#    minPt = cms.double(17.1),
#    minEtaAbs = cms.double(1.479),
#    maxEtaAbs = cms.double(2.4),
#    qual = cms.vuint32(0b0100),
#    maxIso = cms.double(0.205)
#)
#pSingleIsoTkPho22Endcap = cms.Path(SingleIsoTkPho22Endcap) 

#SingleIsoTkPho12Barrel = l1tGTSingleObjectCond.clone(
#    tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
#    minPt = cms.double(8.8),
#    minEta = cms.double(-1.479), 
#    maxEta = cms.double(1.479),
#    qual = cms.vuint32(0b0010),
#    maxIso = cms.double(0.25)
#)
#pSingleIsoTkPho12Barrel = cms.Path(SingleIsoTkPho12Barrel) 

#SingleIsoTkPho12EndcapPos = l1tGTSingleObjectCond.clone(
#    tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
#    minPt = cms.double(8.8),
#    minEtaAbs = cms.double(1.479),
#    maxEtaAbs = cms.double(2.4),
#    qual = cms.vuint32(0b0100),
#    maxIso = cms.double(0.205)
#)
#pSingleIsoTkPho12EndcapPos = cms.Path(SingleIsoTkPho12EndcapPos) 

#algorithms.append(cms.PSet(name=cms.string("pDoubleTkIsoPho22_12"),
#                       expression=cms.string("(pSingleIsoTkPho22Barrel or pSingleIsoTkPho22EndcapPos or pSingleIsoTkPho22EndcapNeg) and (pSingleIsoTkPho12Barrel or pSingleIsoTkPho12EndcapPos or pSingleIsoTkPho12EndcapNeg)")))
