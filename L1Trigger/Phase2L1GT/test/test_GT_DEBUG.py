# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step1 --conditions 125X_mcRun4_realistic_v2 -n 2 --era Phase2C17I13M9 --eventcontent FEVTDEBUGHLT -s RAW2DIGI,L1TrackTrigger,L1 --datatier GEN-SIM-DIGI-RAW-MINIAOD --fileout file:test.root --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring,L1Trigger/Configuration/customisePhase2.addHcalTriggerPrimitives,L1Trigger/Configuration/customisePhase2FEVTDEBUGHLT.customisePhase2FEVTDEBUGHLT,L1Trigger/Configuration/customisePhase2TTNoMC.customisePhase2TTNoMC --geometry Extended2026D88 --nThreads 8 --filein /store/mc/Phase2Fall22DRMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2_ext1-v1/30000/000c5e5f-78f7-44ee-95fe-7b2f2c2e2312.root --mc --customise_commands=process.source.inputCommands = cms.untracked.vstring("keep *", "drop l1tPFJets_*_*_*")
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Phase2C17I13M9_cff import Phase2C17I13M9

process = cms.Process('L1TEmulation',Phase2C17I13M9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D88Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring(
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30006/6fbb57e0-65e1-48e8-860a-4d6b546929da.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30006/d5c63c2b-0297-4bc3-abc6-56c72cfdff9c.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30006/411d336c-f647-4648-9a7d-f1efd054ad0e.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30006/2267fc28-ef8a-4802-a25d-b40a152228c1.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/ef7bebd4-f24d-49bb-b590-aa4227410e23.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/e14052b2-fcaa-4e39-bea7-e5033f34b099.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30007/326aff9f-ebab-4c74-9cb5-3e715ff2c83e.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/96855af8-26be-4acf-a82b-91d828e6948d.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/8ab28e29-a620-40fa-9f61-1f4a251b2463.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/1195dfcc-6da3-43a5-9aba-ed0e54d0d226.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/f4cd47bc-d3c7-4cf6-b2df-01eeabd66585.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/9c047cb3-3ae8-476b-9d9c-f5dcece00c58.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/af171202-330f-4aca-93da-1246931d7abb.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/2b3ddc48-093c-4e15-b5d0-d6379511098e.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/284b077a-5211-4d50-9830-4c6eb90cb85f.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/14b3e36e-9111-43c7-8ced-427b5a3828fb.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/ba827a49-1a1e-4968-99fc-9c826a746876.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30007/d9cf568d-9874-4fbe-b62f-57a4fe5dacba.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30006/c9bb7137-be3d-431a-8216-7e3c29ee5c45.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/418014d8-778c-42ab-a91d-f3ac27012ff7.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/6f8409d1-fbef-4a50-a76b-0a66e3ed07f1.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/e3db3902-3290-4425-a774-d3f50ee7dd8e.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/18e7e3dc-99be-40ac-ad45-c940fcf9f66f.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/23bb86a3-3ba6-4fb7-9788-b4db0d2d0063.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/e4e3d9c4-8b32-49dc-bbfc-a77cc6ff5ecd.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/a22f816b-f2a4-4056-a8d4-473a73f043d7.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/a3f69f92-5367-4599-bd71-dd146bcdd9e3.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/1b018cdb-05ca-4dfa-a239-f9484d21695e.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/001e9c24-1e25-4781-a408-824e17e91ce4.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30007/06048d70-fb9b-486d-8d0c-4a4d5b6a7406.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/72979cf5-1800-4166-aa6d-9736e9ecd09f.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/2a53b1d6-edfa-4b57-991e-71db4a8b8df8.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/df085247-0397-44ee-ae0a-c84723853c7c.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/4fb3ffa1-5dde-47bc-b8b4-743e6db28247.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/fc6fc028-55e1-4ef0-a686-32c33cde817b.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30007/6052934f-e72f-423c-a4a0-d644a76bc5e6.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/e4d8cc1c-3798-4beb-b7fb-c067ceba73d7.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/2d7ba091-d94a-41b8-82d9-c62771fd12a7.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/8b324e30-c19e-4709-9ad7-9950d8ecb360.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/06641ca3-b01a-4bfe-af72-15123929239a.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/875224ed-22c5-485b-97d1-56509b86d6b3.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30007/f667c20c-1b6e-4b4c-bade-7552b0e65f72.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/4cbb206e-80f2-4f7e-82d5-46b3bb2d48ac.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/a6e05081-60b0-4fec-bd57-c06c3efcaf88.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/ff2f0f40-6ff0-4876-b476-95fe87acacef.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/1f066607-4c3c-44ac-a9a5-45ea418539b5.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/028e57da-3e6e-4a2f-b857-b08e28d3fded.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30005/53a72c26-f50a-46df-b5e2-c1e590800869.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/f851ec44-73aa-4c89-9c72-3652c01ccaf9.root',
'/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30008/485f7283-c0c7-45fe-a950-592a5f071d95.root',
                            ),
)

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(200))


process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step1 nevts:2'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW-MINIAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:test.root'),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '125X_mcRun4_realistic_v2', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1TrackTrigger_step = cms.Path(process.L1TrackTrigger)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

#GT emulator
process.load('L1Trigger.Configuration.GTemulator_cff')
process.GTemulation_step = cms.Path(process.GTemulator)

process.load('L1Trigger.Phase2L1GT.l1tGTMenu_lepSeeds_DEBUG_qual_cff')
from L1Trigger.Phase2L1GT.l1tGTAlgoBlockProducer_cff import collectAlgorithmPaths


process.GToutput = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('drop *',
       'keep *P2GT*_*_*_L1TEmulation',
    ),
    fileName=cms.untracked.string("l1t_emulation.root")
    )

process.pGToutput = cms.EndPath(process.GToutput) 


# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1simulation_step,process.GTemulation_step, *collectAlgorithmPaths(process), process.pGToutput, process.endjob_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads = 8
process.options.numberOfStreams = 0

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.aging
from SLHCUpgradeSimulations.Configuration.aging import customise_aging_1000 

#call to customisation function customise_aging_1000 imported from SLHCUpgradeSimulations.Configuration.aging
process = customise_aging_1000(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customisePhase2
from L1Trigger.Configuration.customisePhase2 import addHcalTriggerPrimitives 

#call to customisation function addHcalTriggerPrimitives imported from L1Trigger.Configuration.customisePhase2
process = addHcalTriggerPrimitives(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customisePhase2FEVTDEBUGHLT
from L1Trigger.Configuration.customisePhase2FEVTDEBUGHLT import customisePhase2FEVTDEBUGHLT 

#call to customisation function customisePhase2FEVTDEBUGHLT imported from L1Trigger.Configuration.customisePhase2FEVTDEBUGHLT
process = customisePhase2FEVTDEBUGHLT(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customisePhase2TTNoMC
from L1Trigger.Configuration.customisePhase2TTNoMC import customisePhase2TTNoMC 

#call to customisation function customisePhase2TTNoMC imported from L1Trigger.Configuration.customisePhase2TTNoMC
process = customisePhase2TTNoMC(process)

# End of customisation functions


# Customisation from command line

process.source.inputCommands = cms.untracked.vstring("keep *", "drop l1tPFJets_*_*_*", "drop l1tTkPrimaryVertexs_L1TkPrimaryVertex_*_*")
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
