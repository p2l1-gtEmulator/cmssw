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

#        regionsAbsEtaLowerBounds=cms.vdouble(0,1.2,3),
#        regionsMinPt=cms.vdouble(12,14,15)


SingleTkMuon22 = l1tGTSingleObjectCond.clone(
    tag =  cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    #minPt = cms.double(20.3),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4),
    regionsAbsEtaLowerBounds=cms.vdouble(0,0.83,1.24),
    regionsMinPt=cms.vdouble(20.3,20.2,20.4)
)
pSingleTkMuon22 = cms.Path(SingleTkMuon22)
algorithms.append(cms.PSet(expression = cms.string("pSingleTkMuon22")))

DoubleTkMuon157 = l1tGTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        #minPt = cms.double(13.6),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4),
        regionsAbsEtaLowerBounds=cms.vdouble(0,0.83,1.24),
        regionsMinPt=cms.vdouble(13.6,13.5,13.6)

    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        #minPt = cms.double(5.9),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4),
        regionsAbsEtaLowerBounds=cms.vdouble(0,0.83,1.24),
        regionsMinPt=cms.vdouble(5.9,5.8,6.0)
    ),
    maxDz = cms.double(1),
)
pDoubleTkMuon15_7 = cms.Path(DoubleTkMuon157)
algorithms.append(cms.PSet(expression = cms.string("pDoubleTkMuon15_7")))

TripleTkMuon533 = l1tGTTripleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        #minPt = cms.double(3.9),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4),
        regionsAbsEtaLowerBounds=cms.vdouble(0,0.83,1.24),
        regionsMinPt=cms.vdouble(3.9,3.9,4.0)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        #minPt = cms.double(2),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4),
        regionsAbsEtaLowerBounds=cms.vdouble(0,0.83,1.24),
        regionsMinPt=cms.vdouble(2.0,2.0,2.1)
    ),
    collection3 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        #minPt = cms.double(2),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4),
        regionsAbsEtaLowerBounds=cms.vdouble(0,0.83,1.24),
        regionsMinPt=cms.vdouble(2.0,2.0,2.1)
    ),
    delta12 = cms.PSet(
        maxDz = cms.double(1)
    ),
    delta13 = cms.PSet(
        maxDz = cms.double(1)
    ),
    #delta23 = cms.PSet(
    #    maxDz = cms.double(1)
    #)
)
pTripleTkMuon5_3_3 = cms.Path(TripleTkMuon533)
algorithms.append(cms.PSet(expression = cms.string("pTripleTkMuon5_3_3")))

####### TK EG and PHO seeds ###########

SingleTkEle36 = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    #minPt = cms.double(29.9),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4),
    regionsAbsEtaLowerBounds=cms.vdouble(0,1.479),
    regionsMinPt=cms.vdouble(29.9,28.0),
    regionsQual=cms.vuint32(0b0010,0b0010)
    #qual = cms.vuint32(0b0010)
)
pSingleTkEle36 = cms.Path(SingleTkEle36) 
algorithms.append(cms.PSet(expression = cms.string("pSingleTkEle36")))

SingleIsoTkEle28 = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    #minPt = cms.double(29.9),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4),
    regionsAbsEtaLowerBounds=cms.vdouble(0,1.479),
    regionsMinPt=cms.vdouble(23,21.9),
    regionsQual=cms.vuint32(0b0000,0b0010)
    #qual = cms.vuint32(0b0010)
)
pSingleIsoTkEle28 = cms.Path(SingleIsoTkEle28) 
algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28")))

#SingleIsoTkEle28Barrel = l1tGTSingleObjectCond.clone(
#    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
#    minPt = cms.double(23), 
#    minEta = cms.double(-1.479),
#    maxEta = cms.double(1.479),
    #maxIso = cms.double(0.13),
#)
#pSingleIsoTkEle28Barrel = cms.Path(SingleIsoTkEle28Barrel)
#algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28Barrel")))

#SingleIsoTkEle28BarrelQual = l1tGTSingleObjectCond.clone(
#    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
#    minPt = cms.double(23), 
#    minEta = cms.double(-1.479),
#    maxEta = cms.double(1.479),
#    qual = cms.vuint32(0b0000),
    #maxIso = cms.double(0.13),
#)
#pSingleIsoTkEle28BarrelQual = cms.Path(SingleIsoTkEle28BarrelQual)
#algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28BarrelQual")))

#SingleIsoTkEle28Endcap = l1tGTSingleObjectCond.clone(
#    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
#    minPt = cms.double(21.9),
#    minEtaAbs = cms.double(1.479),
#    maxEtaAbs = cms.double(2.4),
#    qual = cms.vuint32(0b0010,0b0011,0b0110,0b1010,0b0111,0b1011,0b1110,0b1111),
    #maxIso = cms.double(0.28)
#)
#pSingleIsoTkEle28Endcap = cms.Path(SingleIsoTkEle28Endcap) 
#algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28Endcap")))

#algorithms.append(cms.PSet(name=cms.string("pSingleIsoTkEle28OLD"),
#                       expression=cms.string("pSingleIsoTkEle28Barrel or pSingleIsoTkEle28Endcap")))


SingleIsoTkPho36 = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
    #minPt = cms.double(30.8),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4),
    regionsAbsEtaLowerBounds=cms.vdouble(0,1.479),
    regionsMinPt=cms.vdouble(30.8,29.2),
    regionsQual=cms.vuint32(0b0010,0b0100)
    #qual = cms.vuint32(0b0100),
    #maxIso = cms.double(0.205)
)
pSingleIsoTkPho36 = cms.Path(SingleIsoTkPho36) 

algorithms.append(cms.PSet(expression=cms.string("pSingleIsoTkPho36")))

#SingleIsoTkPho36Barrel = l1tGTSingleObjectCond.clone(
#    tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
#    minPt = cms.double(30.8),
#    minEta = cms.double(-1.479), 
#    maxEta = cms.double(1.479),
#    qual = cms.vuint32(0b0010),
#    maxIso = cms.double(0.25)
#)
#pSingleIsoTkPho36Barrel = cms.Path(SingleIsoTkPho36Barrel) 

#SingleIsoTkPho36Endcap = l1tGTSingleObjectCond.clone(
#    tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
#    minPt = cms.double(30.8),
#    minEtaAbs = cms.double(1.479),
#    maxEtaAbs = cms.double(2.4),
#    qual = cms.vuint32(0b0100),
#    maxIso = cms.double(0.205)
#)
#pSingleIsoTkPho36Endcap = cms.Path(SingleIsoTkPho36Endcap) 
#
#algorithms.append(cms.PSet(name=cms.string("pSingleIsoTkPho36"),
#                       expression=cms.string("pSingleIsoTkPho36Barrel or pSingleIsoTkPho36Endcap")))

DoubleTkEle2512 = l1tGTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
        #minPt = cms.double(20.6),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4),
        regionsAbsEtaLowerBounds=cms.vdouble(0,1.479),
        regionsMinPt=cms.vdouble(20.6,19.3),
        regionsQual=cms.vuint32(0b0010,0b0010)
        #qual = cms.vuint32(0b0010)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
        #minPt = cms.double(9.6),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4),
        regionsAbsEtaLowerBounds=cms.vdouble(0,1.479),
        regionsMinPt=cms.vdouble(9.6,9.1),
        regionsQual=cms.vuint32(0b0010,0b0010)
        #qual = cms.vuint32(0b0010)
    ),
    maxDz = cms.double(1),
)
pDoubleTkEle25_12 = cms.Path(DoubleTkEle2512)
algorithms.append(cms.PSet(expression = cms.string("pDoubleTkEle25_12")))

DoubleIsoTkPho2212 = l1tGTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
        #minPt = cms.double(20.6),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4),
        regionsAbsEtaLowerBounds=cms.vdouble(0,1.479),
        regionsMinPt=cms.vdouble(18.0,16.2),
        regionsQual=cms.vuint32(0b0010,0b0100)
        #qual = cms.vuint32(0b0010)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
        #minPt = cms.double(9.6),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4),
        regionsAbsEtaLowerBounds=cms.vdouble(0,1.479),
        regionsMinPt=cms.vdouble(8.8,6.9),
        regionsQual=cms.vuint32(0b0010,0b0100)
        #qual = cms.vuint32(0b0010)
    ),
)
pDoubleIsoTkPho22_12 = cms.Path(DoubleIsoTkPho2212)
algorithms.append(cms.PSet(expression = cms.string("pDoubleIsoTkPho22_12")))



#SingleIsoTkPho36 = l1tGTSingleObjectCond.clone(
#    tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
#    #minPt = cms.double(30.8),
#    minEta = cms.double(-2.4),
#    maxEta = cms.double(2.4),
#    regionsAbsEtaLowerBounds=cms.vdouble(0,1.479),
#    regionsMinPt=cms.vdouble(30.8,29.2),
#    regionsQual=cms.vuint32(0b0010,0b0100)
    #qual = cms.vuint32(0b0100),
    #maxIso = cms.double(0.205)
#)
#pSingleIsoTkPho36 = cms.Path(SingleIsoTkPho36) 

#algorithms.append(cms.PSet(expression=cms.string("pSingleIsoTkPho36")))





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
