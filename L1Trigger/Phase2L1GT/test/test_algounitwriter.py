import L1Trigger.Phase2L1GT.VHDLWriter.Conversions as conversions
import L1Trigger.Phase2L1GT.VHDLWriter.Writer as writer
from cmssw_test_sequence_gt_only import process as gt

module_path_map = { list(mod.moduleNames())[0] : path for path, mod in gt.paths.items() }

knownfilters = []
condtext = ""
knownfilters = conversions.getConditionsfromConfig(gt)
algobits = conversions.assignAlgoBits(gt.BoardData)

for filt in knownfilters:
    condtext += writer.conditionwriter(filt, module_path_map[filt.Name])

algounittext = writer.algounitWriter(algobits,condtext)
writer.writeAlgounitToFile("algos.vhdl",algounittext)