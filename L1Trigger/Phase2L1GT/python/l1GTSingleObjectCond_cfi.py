import FWCore.ParameterSet.Config as cms
from L1Trigger.Phase2L1GT.l1GTScales import scale_parameter

l1GTSingleObjectCond = cms.EDFilter(
    "L1GTSingleObjectCond",
    scales=scale_parameter
)
