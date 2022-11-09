import FWCore.ParameterSet.Config as cms

l1GTProducer = cms.EDProducer(
    "L1GTProducer",
    CL2Electrons = cms.VInputTag(
        cms.InputTag("l1ctLayer1EG", "L1TkEleEB"),
        cms.InputTag("l1ctLayer1EG", "L1TkEleEE")
    ),
    CL2Photons = cms.VInputTag(
        cms.InputTag("l1ctLayer1EG","L1TkEmEB"),
        cms.InputTag("l1ctLayer1EG","L1TkEmEE")
    )
)
