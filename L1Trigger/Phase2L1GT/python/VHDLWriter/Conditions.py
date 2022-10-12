from ast import Mod
from asyncio.windows_events import NULL
from modulefinder import Module
from queue import Empty
from turtle import update
from L1Trigger.Phase2L1GT.l1GTScales import l1GTScales

class Condition:
    """
    Base Class for all EDFilters that correspond to an P2GT condition
    Contains: Cuts, The VHDL Resource usage, Paths corresponding to the Modules in the config
    """
    _ObjectNameConversions = {
        "GTT PromptJets" : "GTT_PROMPT_JETS_SLOT",
        "GTT DisplacedJets" : "GTT_DISPLACED_JETS_SLOT",
        "GTT PromptHtSum" : "GTT_HT_MISS_PROMPT_SLOT",
        "GTT DisplacedHtSum" : "GTT_HT_MISS_DISPLACED_SLOT",
        "GTT EtSum" : "GTT_ET_MISS_SLOT",
        "GTT Taus" : "GTT_TAUS_SLOT",
        "GTT PhiCandidates" : "GTT_PHI_CANDIDATE_SLOT",
        "GTT RhoCandidates" : "GTT_RHO_CANDIDATE_SLOT",
        "GTT BsCandidates" : "GTT_BS_CANDIDATE_SLOT",
        "GTT Prim Vert" : "GTT_PRIM_VERT_SLOT",
        "CL2 Jets" : "CL2_JET_SLOT",
        "CL2 HtSum" : "CL2_HT_MISS_SLOT",
        "CL2 EtSum" : "CL2_ET_MISS_SLOT",
        "CL2 Taus" : "CL2_TAU_SLOT",
        "CL2 Electrons" : "CL2_ELECTRON_SLOT",
        "CL2 Photons" : "CL2_PHOTON_SLOT",
        "GCT NonIsoEg" : "GCT_NON_ISO_EG_SLOT",
        "GCT IsoEg" : "GCT_ISO_EG_SLOT",
        "GCT Jets" : "GCT_JETS_SLOT",
        "GCT Taus" : "GCT_TAUS_SLOT",
        "GCT HtSum" : "GCT_HT_MISS_SLOT",
        "GCT EtSum" : "GCT_ET_MISS_SLOT",
        "GMT SaPromptMuons" : "GMT_SA_PROMPT_SLOT", 
        "GMT SaDisplacedMuons" : "GMT_SA_DISPLACED_SLOT", 
        "GMT TkMuons" : "GMT_TK_MUON_SLOT", 
        "GMT Topo" : "GMT_TOPO_SLOT"
        }


    def __init__(self):
        self.Cuts = {}
        self.InputObjects = {}
        self._InputTags = []
        self.Paths = []
        self.ResourceUseage = CutResources()
        self.ResourcesperCut = {
            ('minPt') : CutResources(bram = 0 , dsp = 0, lut = 110),
            ('minEta','maxEta') : CutResources(bram = 0 , dsp = 0, lut = 120),
            ('minPhi','maxPhi') : CutResources(bram = 0 , dsp = 0, lut = 123),
            ('minDz','maxDz') : CutResources(bram = 0 , dsp = 0, lut = 123),
            ('qual') : CutResources(bram = 0 , dsp = 0, lut = 40),
            ('iso') : CutResources(bram = 0 , dsp = 0, lut = 40)

        }
        self._HWConversionFunctions = {
            'minPt': l1GTScales.to_hw_pT,
            'minEta': l1GTScales.to_hw_eta,
            'maxEta': l1GTScales.to_hw_eta,
            'minPhi': l1GTScales.to_hw_phi,
            'maxPhi': l1GTScales.to_hw_phi,
            'minDz': l1GTScales.to_hw_dZ,
            'maxDz': l1GTScales.to_hw_dZ,
        }

        self._cut_aliases = {
            'minPt' : 'pT{}_cut',
            'minEta' : 'minEta{}_cut',
            'maxEta' : 'maxEta{}_cut',
            'minPhi' : 'minPhi{}_cut',
            'maxPhi' : 'maxPhi{}_cut',
            'minDz' : 'minDz{}_cut',
            'maxDz' : 'maxDz{}_cut',
            'qual' : 'qual{}_cut',
            'iso' : 'iso{}_cut'
        }

    def addResources(self,knowncut):
        for k in list(self.ResourcesperCut.keys()):
            if knowncut in k:
                if k in self.ResourcesperCut.keys():
                    self.ResourceUseage.addCutResources(self.ResourcesperCut.pop(k))




    def _setInputObject(self,condition,value):
        self.InputObjects[condition] = self._ObjectNameConversions.get(value)

    def setCut(self,key,physvalue, collection = "",collectionlength = 0):
        if collection != "":
            if self.getHWCut(key, collection) not in self.Cuts.keys():
                self.Cuts[self.getHWCut(key, collection)] = [0] * (collectionlength - 1)
                self.Cuts[self.getHWCut(key, collection)][collection] = 
 
        if key in self._HWConversionFunctions:
            self.Cuts[self.getHWCut(key, collection)] =  _Cut(self._HWConversionFunctions[key](physvalue),physvalue)
        else:
            self.Cuts[self.getHWCut(key, collection)] = _Cut(physvalue,physvalue)

    def setName(self,name):
        self.Name = name
    def addPath(self,path):
        self.Paths.append(path)

    def getHWCut(self, cut, collection = ""):
        if cut in self._cut_aliases:
            return self._cut_aliases[cut].format(collection)
        return cut

    def getCollections(self, object):
        return {}

    def setInputObjects(self, **inobjs):
        for name, value in inobjs.items():
            if name in self._InputTags:
                self.InputObjects[name] = value
    def _setHWConversionFunctions(self,indict):
           self._HWConversionFunctions = indict


class DoubleObjCond(Condition):
    """
    Class for to the L1GTDoubleObjectCond 
    """
    Label = "L1GTDoubleObjectCond"
    Template = "double.template"
    def __init__(self):
        Condition.__init__(self)
        
        self._HWConversionFunctions.update({
            'minDEta': l1GTScales.to_hw_eta,
            'maxDEta': l1GTScales.to_hw_eta,
            'minDPhi': l1GTScales.to_hw_phi,
            'maxDPhi': l1GTScales.to_hw_phi,
            'minDR': l1GTScales.to_hw_dRSquared,
            'maxDR': l1GTScales.to_hw_dRSquared,
            'minInvMass': l1GTScales.to_hw_InvMassSqrDiv2,
            'maxInvMass': l1GTScales.to_hw_InvMassSqrDiv2,
            'minTransMass': l1GTScales.to_hw_TransMassSqrDiv2,
            'maxTransMass': l1GTScales.to_hw_TransMassSqrDiv2,
        })

        self._cut_aliases.update({ 
            'minDEta' : 'dEtaMin_cut',
            'maxDEta' : 'dEtaMax_cut',
            'minDPhi' : 'dPhiMin_cut',
            'maxDPhi' : 'dPhiMax_cut',
            'minDR' : 'dRSquaredMin_cut',
            'maxDR' : 'dRSquaredMax_cut',
            'minInvMass' : 'invMassSqrDiv2Min_cut',
            'maxInvMass' : 'invMassSqrDiv2Max_cut',
            'minTransMass' : 'transMassSqrDiv2Min_cut',
            'maxTransMass' : 'transMassSqrDiv2Max_cut',
            'os' : 'os_cut',
            'ss' : 'ss_cut'
        })
        self.ResourcesperCut.update({
            ('minDEta','maxDEta') : CutResources(bram = 0 , dsp = 0, lut = 800),
            ('minDPhi','maxDPhi') : CutResources(bram = 0 , dsp = 0, lut = 800),
            ('minDR','maxDR') : CutResources(bram = 0 , dsp = 24, lut = 1800),
            ('minInvMass','maxInvMass') : CutResources(bram = 24 , dsp = 36, lut = 2000),
            ('minTransMass','maxTransMass') : CutResources(bram = 24 , dsp = 36, lut = 2000)
        })


    def getCollections(self, object):
        collections = {1: object.getParameter('collection1'), 2: object.getParameter('collection2')}
        for col in collections.values():
            self._InputTags += [col.getParameter("tag")]

        return collections


class SingleObjCond(Condition):

    """
    Class for to the L1GTSingleObjectCond 
    """
    Label = "L1GTSingleObjectCond"
    Template = "single.template"

    def getCollections(self, object):
        self._InputTags += [object.getParameter("tag")]
        return {}


class CutResources:
    def __init__(self,bram = 0,dsp = 0,lut = 0):
        self.bram = bram
        self.dsp = dsp
        self.lut = lut
    def addCutResources(self,cutResources):
        self.bram = self.bram + cutResources.bram
        self.dsp = self.dsp + cutResources.dsp
        self.lut = self.lut + cutResources.lut
    def printResources(self):
        print("bram:{}".format(self.bram))
        print("dsp:{}".format(self.dsp))
        print("lut:{}".format(self.lut))
        return 0

class DefineAlgoBits:
    def __init__(self):
        self.Assignment = {}
    def SetBit(self,Name,Algobit):
        self.Assignment[Name] = Algobit
    
    


class _Cut:
    def __init__(self,hwcut,physcut):
        self.hwcut = hwcut
        self.physcut = physcut 


class LogicalFilter:
    def __init__(self,pathname,expression,modulenames):
        self.pathname = pathname 
        self.expression = expression
        self.modulenames = modulenames


class AlgorithmBlock:
    """
    Class that groupes the algorithms in a way that all codependent conditions are grouped  are 
    """
    def __init__(self):
        self.ResourceUseage = CutResources(0,0,0)
        self.Modules = set()
        self.Paths  = set()
        self.Collections = set()
        self.LogicalPath = set()

    def addlogical(self,paths,modules):
        self.Modules.update(modules.modulenames)
        self.LogicalPath.add(paths)
    def checklogical(self,modules):
        """
        checks if a module in a logical combination is already present in modules
        """
        if(self.Modules.intersection(modules.modulenames) == set()):
            return 0
        else:
            return 1
    def Combineblocks(self,algoblock):
        self.ResourceUseage.addCutResources(algoblock.ResourceUseage) 
        self.Modules.update(algoblock.Modules) 
        self.Paths.update(algoblock.Paths)  
        self.LogicalPath.update(algoblock.LogicalPath)
    def addCondition(self,knownfilterkey,knownfiltervalue):
        self.Modules.add(knownfilterkey)
        self.Paths.update(knownfiltervalue.Paths)
        self.ResourceUseage.addCutResources(knownfiltervalue.ResourceUseage)
        self.Collections.update(set(knownfiltervalue.InputObjects.values()))
    def checkCondition(self,knownfilterkey):
        """
        checks if module is already present in modules, needed to combine logical filters and conditions
        """
        if  knownfilterkey in self.Modules:
            return 1
        else:
            return 0 

class Algorithmsdict:
    def __init__(self):
        self.algoblocks = []

    def addLogicalFilters(self,logicalcombinations):

        for key, value in logicalcombinations.items():
            for algoblock in self.algoblocks:
                if algoblock.checklogical(key, value):
                    break
            else:
                newblock  = AlgorithmBlock()
                newblock.addlogical(key, value)
                self.algoblocks.append(newblock)
    def addConditions(self,conditions):
        for key in conditions.keys():
            for algoblock in self.algoblocks:
                if algoblock.checkCondition(key) == 1:
                    algoblock.addCondition(key,conditions[key])
                    break
            else:
                newblock  = AlgorithmBlock()
                newblock.addCondition(key,conditions[key])
                self.algoblocks.append(newblock)





    def popMaxalgoblock(self):

        if self.algoblocks == []:
            return 0
        else:
           brammax = max(item.ResourceUseage.bram for item in self.algoblocks)

           if brammax!=0 :
                for item, value in enumerate(self.algoblocks):
                    if value.ResourceUseage.bram == brammax:
                        return self.algoblocks.pop(item)

           dspmax = max(item.ResourceUseage.dsp for item in self.algoblocks)
           if dspmax!=0 :
                for item, value in enumerate(self.algoblocks):
                    if value.ResourceUseage.dsp == dspmax:
                        return self.algoblocks.pop(item)
           lutmax = max(item.ResourceUseage.lut for item in self.algoblocks)
           for item, value in enumerate(self.algoblocks):
                if value.ResourceUseage.lut == lutmax:
                    return self.algoblocks.pop(item)

            


