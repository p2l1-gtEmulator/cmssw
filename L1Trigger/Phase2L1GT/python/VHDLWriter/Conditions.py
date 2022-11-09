from L1Trigger.Phase2L1GT.l1GTScales import l1GTScales

class Condition:
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

    def _setInputObject(self,condition,value):
        self.InputObjects[condition] = self._ObjectNameConversions.get(value)

    def setCuts(self, **cutsdict):
        for key , value in cutsdict.items():
            if key in self._PossibleCuts:
                if key in self._HWConversionFunctions:
                    self.Cuts[key] = self._HWConversionFunctions[key](value)
                else:
                    self.Cuts[key] = value

    def setCut(self,key,value, collection = ""):
        if key in self._HWConversionFunctions:
            self.Cuts[self.getHWCut(key, collection)] = self._HWConversionFunctions[key](value)
        else:
            self.Cuts[self.getHWCut(key, collection)] = value

    def setName(self,name):
        self.Name = name

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

    def getCollections(self, object):
        collections = {1: object.getParameter('collection1'), 2: object.getParameter('collection2')}
        for col in collections.values():
            self._InputTags += [col.getParameter("tag")]

        return collections


class SingleObjCond(Condition):
    Label = "L1GTSingleObjectCond"
    Template = "single.template"

    def getCollections(self, object):
        self._InputTags += [object.getParameter("tag")]
        return {}

class DefineAlgoBits:
    def __init__(self):
        self.Assignment = {}
    def SetBit(self,Name,Algobit):
        self.Assignment[Name] = Algobit


    

