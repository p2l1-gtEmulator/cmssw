import FWCore.ParameterSet.Config as cms
from L1Trigger.Phase2L1GT.l1GTScales import scale_parameter

l1GTQuadObjectCond = cms.EDFilter(
    "L1GTQuadObjectCond",
    scales=scale_parameter
)
