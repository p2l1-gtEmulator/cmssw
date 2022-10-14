import FWCore.ParameterSet.Config as cms
from test_algounitwriter import Algobits as algosdict
process = cms.Process('L1Test2')

# Input source
process.source = cms.Source("PoolSource", fileNames=cms.untracked.vstring(("file:new_output.root")))


# Algo bits
from L1Trigger.Phase2L1GT.l1GTAlgoChannelConfig import generate_channel_config
print(algosdict)
process.BoardData = cms.EDAnalyzer("L1GTBoardWriter",
  outputFilename = cms.string("new_patterns"),
  maxLines = cms.uint32(1024),
  processName = cms.string("L1Test"),
  channelConfig = generate_channel_config(
        algosdict
    )
)
process.l1t_BoardData = cms.Path(process.BoardData)
