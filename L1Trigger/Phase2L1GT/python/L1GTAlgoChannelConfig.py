import FWCore.ParameterSet.Config as cms

def generate_channel_config(algosDict: 'dict[int, dict[int, str]]') -> cms.VPSet:
    config = []
    for channel, algos in algosDict.items():
        algoBits = []
        for bitPos, path in algos.items():
            algoBits += [
                cms.PSet(
                    bitPos=cms.uint32(bitPos),
                    path=cms.string(path)
                )]
                
        config += [cms.PSet(
            channel=cms.uint32(channel),
            algoBits=cms.VPSet(*algoBits)
        )]

    return cms.VPSet(*config)
