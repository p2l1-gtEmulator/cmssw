import FWCore.ParameterSet.Config as cms
from L1Trigger.Phase2L1GT.l1GTScales import scale_parameter

l1GTTripleObjectCond = cms.EDFilter(
    "L1GTTripleObjectCond",
    scales=scale_parameter
)
