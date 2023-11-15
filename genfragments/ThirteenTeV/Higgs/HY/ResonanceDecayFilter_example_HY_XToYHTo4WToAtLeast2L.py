import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/local/karl/gridpacks/NMSSM_XToYH_MX_1000_MY_500_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            '25:m0 = 125.0',
            '25:onMode = off', # disable all Higgs decay modes
            '25:oneChannel = 1 1 100 24 -24', # H->W+ W- only possible
            '25:onIfMatch = 24 -24', # enable H->W+ W-
            '35:onMode = off', # disable all Y decay modes
            '35:oneChannel = 1 1 100 24 -24', # Y->W+ W- only possible
            '35:onIfMatch = 24 -24', # enable Y->W+ W-
            '24:mMin = 0.05', # minimum mass of off-shell W
            'ResonanceDecayFilter:filter = on',
            'ResonanceDecayFilter:exclusive = off', # the daughters do not have to appear in the exact numbers as specified
            'ResonanceDecayFilter:mothers = 24', # only the descendants of W bosons are considered here
            'ResonanceDecayFilter:eMuTauAsEquivalent = on', # treat all leptons on equal footing in the list of daughters
            'ResonanceDecayFilter:daughters = 11,11', # W bosons must produce at least 2 leptons
          ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters')
    )
)
