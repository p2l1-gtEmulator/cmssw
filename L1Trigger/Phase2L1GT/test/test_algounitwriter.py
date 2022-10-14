import L1Trigger.Phase2L1GT.VHDLWriter.Conversions as conversions
import L1Trigger.Phase2L1GT.VHDLWriter.Writer as writer
from cmssw_test_sequence_gt_only import process as gt
from cmssw_test_sequence_gt_only import channel_conf as algobitmap

knownfilters = dict()
logicalcombinations = dict()
distributedalgos = dict()
knownfilters = conversions.getConditionsfromConfig(gt)
logicalcombinations = conversions.getLogicalFilters(gt,knownfilters)
algoblocks = conversions.writeAlgoblocks(knownfilters,logicalcombinations)
distributedalgos = conversions.distributeAlgos(algoblocks,1)
conversions.writeAlgounits(distributedalgos,algobitmap,knownfilters,logicalcombinations)
Algobits = conversions.getAlgobits(algobitmap,distributedalgos,[0])
