import L1Trigger.Phase2L1GT.VHDLWriter.Conditions as cond




def checkFilter(obj):
    knownConditions = [cond.SingleObjCond, cond.DoubleObjCond]
    Condit = None
    for Condition in knownConditions:
        try:
            if obj.type_() == Condition.Label:
                Condit = Condition()
        except Exception as ex:
            print(ex)
            pass
    

    if Condit == None:
        return 0

    for idx, col in Condit.getCollections(obj).items():
        knowncuts = Condit._cut_aliases.keys()
        for knowncut in knowncuts:
            if col.hasParameter(knowncut):
                Condit.setCut(knowncut,col.getParameter(knowncut).value(), idx)
    
    knowncuts = Condit._cut_aliases.keys()
    for knowncut in knowncuts:
        if obj.hasParameter(knowncut):
            Condit.setCut(knowncut, obj.getParameter(knowncut).value())

    for idx, tag in enumerate(Condit._InputTags):
        Condit._setInputObject(idx + 1, tag.productInstanceLabel)

    return Condit



def assignAlgoBits(obj):
    Algobitlist = obj.channelConfig.value().pop().getParameter('algoBits')
    algos = cond.DefineAlgoBits()
    for Bititem in Algobitlist:
        name = Bititem.bitPos.value()
        value = Bititem.path.value()
        algos.SetBit(value,name)
    return algos


def getConditionsfromConfig(obj):
    filterlist = []
    for key,value in  obj.filters.items():
        x = checkFilter(value)
        if x != 0:
            x.setName(key)
            filterlist.append(x)
    return filterlist
