import FWCore.ParameterSet.Config as cms

process = cms.Process('L1Test2')

# Input source
process.source = cms.Source("PoolSource", fileNames=cms.untracked.vstring(("file:test_output.root")))


# Algo bits
from L1Trigger.Phase2L1GT.l1GTAlgoChannelConfig import generate_channel_config

process.BoardData = cms.EDAnalyzer("L1GTBoardWriter",
  outputFilename = cms.string("outputPattern"),
  maxLines = cms.uint32(1024),
  processName = cms.string("L1Test"),
  channelConfig = generate_channel_config({
        0 : {0: "l1t_singleTkMu_14_er2p3"}
    })
)
process.l1t_BoardData = cms.Path(process.BoardData)
