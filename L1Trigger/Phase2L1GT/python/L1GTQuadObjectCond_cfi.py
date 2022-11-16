import FWCore.ParameterSet.Config as cms
from L1Trigger.Phase2L1GT.L1GTScales import scale_parameter

L1GTQuadObjectCond = cms.EDFilter(
    "L1GTQuadObjectCond",
    scales=scale_parameter
)
