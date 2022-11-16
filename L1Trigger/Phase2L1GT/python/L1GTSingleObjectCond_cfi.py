import FWCore.ParameterSet.Config as cms
from L1Trigger.Phase2L1GT.L1GTScales import scale_parameter

L1GTSingleObjectCond = cms.EDFilter(
    "L1GTSingleObjectCond",
    scales=scale_parameter
)
