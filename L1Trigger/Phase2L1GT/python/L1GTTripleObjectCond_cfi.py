import FWCore.ParameterSet.Config as cms
from L1Trigger.Phase2L1GT.L1GTScales import scale_parameter

L1GTTripleObjectCond = cms.EDFilter(
    "L1GTTripleObjectCond",
    scales=scale_parameter
)
