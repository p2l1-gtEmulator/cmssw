import L1Trigger.Phase2L1GT.VHDLWriter.Conversions as conversions
import L1Trigger.Phase2L1GT.VHDLWriter.Writer as writer
from gt_firmware_evaluation import process as gt
from gt_firmware_evaluation import channel_conf as algobitmap

knownfilters = dict()
logicalcombinations = dict()
distributedalgos = dict()
knownfilters = conversions.getConditionsfromConfig(gt)
logicalcombinations = conversions.getLogicalFilters(gt,knownfilters)
algoblocks = conversions.writeAlgoblocks(knownfilters,logicalcombinations)

distributedalgos = conversions.distributeAlgos(algoblocks,1)
conversions.writeAlgounits(distributedalgos,algobitmap,knownfilters,logicalcombinations)