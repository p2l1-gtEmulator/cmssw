import L1Trigger.Phase2L1GT.VHDLWriter.Conditions as cond
import L1Trigger.Phase2L1GT.VHDLWriter.Writer as writer




def checkFilter(filt):
    """
    takes in a cmssw process object and
    checks if filter is a known gt condition
    converts it to corresponding Condition object defined in 
    Conditions.py
    """
    knownConditions = [cond.SingleObjCond, cond.DoubleObjCond]
    Condit = None
    for Condition in knownConditions:
        try:
            if filt.type_() == Condition.Label:
                Condit = Condition()
        except Exception as ex:
            print(ex)
            pass

    if Condit == None:
        return 0
    collectionlength = Condit.getCollections(filt)
    print(len(collectionlength))
    for idx, col in Condit.getCollections(filt).items():
        print(idx)
        knowncuts = Condit._cut_aliases.keys()
        for knowncut in knowncuts:
            if col.hasParameter(knowncut):
                Condit.setCut(knowncut,col.getParameter(knowncut).value(), idx,collectionlength)
                Condit.addResources(knowncut)
    
    knowncuts = Condit._cut_aliases.keys()
    for knowncut in knowncuts:
        if filt.hasParameter(knowncut):
            Condit.setCut(knowncut, filt.getParameter(knowncut).value())
            Condit.addResources(knowncut)
    for idx, tag in enumerate(Condit._InputTags):
        Condit._setInputObject(idx + 1, tag.productInstanceLabel)

    return Condit
def assignAlgoBits(obj):
    """
    takes in 
    """
    Algobitlist = obj.channelConfig.value().pop().getParameter('algoBits')
    algos = cond.defineAlgoBits()
    for Bititem in Algobitlist:
        name = Bititem.bitPos.value()
        value = Bititem.path.value()
        algos.SetBit(value,name)
    return algos


def getConditionsfromConfig(obj):
    filterdict = {}
    for key,value in  obj.filters.items():
        x = checkFilter(value)
        if x != 0:
            filterdict[key] = x 
            addPathsToModule(obj,key,filterdict[key])
    return filterdict

def findPaths(obj,modulename):
    pathlist = []
    for path in obj.paths.values():
        if modulename in path.moduleNames():
            pathlist.append(path.label())
    return pathlist


def getModulesfromPath(gt,algobits):
    modules = {}
    for key,value in algobits.Assignment.items():
        modules[key] = gt.paths[key].moduleNames()
    return modules


def checkiflogicalcombination(filterlist,algobits):
    filterpaths =  [path for filt in filterlist for path in filt.Path]
    combinatorialpath = []
    for algopath in algobits.keys():     
        if algopath not in filterpaths:
            combinatorialpath.append(algopath)
    return combinatorialpath



def getLogicalFilters(gt,knownfilters):
    combinatorialfilters = {} 
    for path in gt.paths:
        pathmodules = gt.paths[path].moduleNames()
        for module in pathmodules:
            if (module in gt.filterNames().split())  :
                if gt.filters[module].type_() == "PathStatusFilter":
                    expression = gt.filters[module].getParameter("logicalExpression").value()
                    containsmodules = getModules(gt,expression)
                    for mod in containsmodules:
                         if mod in knownfilters.keys():
                                combinatorialfilters[path] = cond.LogicalFilter(module,expression,containsmodules)
                                break

    return combinatorialfilters
def getModules(obj,expression):
    words = expression.split()
    modulelist = []
    moduleset = {}
    for word in words:
        try:
            moduleset = (obj.paths[word].moduleNames())
        except:
            pass
        if moduleset != set():
            modulelist.append(moduleset.pop())
        if moduleset != set():
            print("warning %s is part of a combinatorial logic and its path contains more than 1 modules, this will lead to undefined behaviour".format(word))
    return modulelist



def associatePathAndModules(gt,knownfilters):
    pathswithmodules = {}    
    for path in gt.paths:
           x = gt.paths[path].moduleNames()
           for module in x:
               for filt in knownfilters.keys():
                   if filt == module:
                        pathswithmodules.setdefault(filt,[]).append(path)
    return pathswithmodules


def addPathsToModule(gt,filtername,filtervalue):    
    for path in gt.paths:
           modules = gt.paths[path].moduleNames()
           for module in modules:
                if filtername == module:
                    filtervalue.addPath(path)



def writeAlgoblocks(conditions,logfilt):
    algodict = cond.Algorithmsdict()
    algodict.addLogicalFilters(logfilt)
    algodict.addConditions(conditions)
    return algodict

def distributeAlgos(algodict,numslrs):
    algounits = []
    for i in range(numslrs):
        algounits.append(cond.AlgorithmBlock())
    flip = (numslrs -1) * -1
    count = 0

    addmax = algodict.popMaxalgoblock()
    if(numslrs == 1):
        while(addmax != 0):
            algounits[count].Combineblocks(addmax)
            addmax = algodict.popMaxalgoblock()
        return algounits
    else:
        algounits[numslrs-1 - abs(flip)].Combineblocks(addmax)
        flip += 1

        while(addmax != 0):
            addmax = algodict.popMaxalgoblock()
            algounits[numslrs-1 - abs(flip)].Combineblocks(addmax)
            if (numslrs-1 - abs(flip) == 0) or (numslrs-1 - abs(flip) == 2):
                if addmax != 0:
                    addmax = algodict.popMaxalgoblock()
                    if addmax != 0:
                        algounits[numslrs-1 - abs(flip)].Combineblocks(addmax)
            flip += 1
            if flip == (numslrs -1):
                flip = (numslrs -1) * -1
        return algounits



def minconditionsperslr(algodict, numslrs, boarddata = []):
    return 0



def assignAlgostoSlrs(knownfilters,logicalcombinations,numslrs):
    algoblocks = WriteAlgoDict(knownfilters,logicalcombinations)
    distributedAlgos = distributealgos(algoblocks,numslrs)
    return distributedAlgos



def writeAlgounits(distributedAlgos,algomap,knownfilters,logcomb):
    for index,value in enumerate(distributedAlgos):
        modules = dict()
        paths = dict()
        condtext = ""
        algounittext = ""
        bits = {}
        tdistributedAlgos = {}
        logicalcombinations = dict()
        for mod in value.Modules:
            condtext += writer.conditionwriter(mod,knownfilters[mod])
            tdistributedAlgos[mod] = knownfilters[mod]
        if(value.LogicalPath != set()):
            for log in value.LogicalPath:
                logicalcombinations[log] = logcomb[log]
        algounittext = writer.algounitWriter(algomap,condtext,tdistributedAlgos,logicalcombinations,index)
        writer.writeAlgounitToFile("algos_slr{}.vhdl".format(index),algounittext)


def getAlgobits(algomap,distributedalgos,Outputchans):
    chans = Outputchans
    algosdict = {}
    for block in distributedalgos: 
        algochan = chans.pop(0)
        algodict = {}
        for key,conf in algomap.items():
            if(conf in block.Paths or conf in block.LogicalPath):
                algodict[key] = conf
        algosdict[algochan] = algodict
    return algosdict

