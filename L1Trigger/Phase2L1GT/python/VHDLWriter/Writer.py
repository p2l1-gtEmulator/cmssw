import jinja2
import L1Trigger.Phase2L1GT.VHDLWriter.Conditions
import os

def conditionwriter(filter, path):
    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))    # this has to be changed there seems to be a version of this thats called packageloader instead of filesystemloader
    templateEnv = jinja2.Environment(loader=templateLoader,trim_blocks=True,lstrip_blocks=True)
    template = templateEnv.get_template(filter.Template,)
    if(filter.Label == 'L1GTDoubleObjectCond'):
        outputText = template.render(condition_name = filter.Name, dict_item = filter.Cuts,objects_first = filter.InputObjects.get(1),objects_second = filter.InputObjects.get(2), algo_bit_name = path) 
    elif(filter.Label == 'L1GTSingleObjectCond'):
        outputText = template.render(condition_name = filter.Name, dict_item = filter.Cuts,object = filter.InputObjects.get(1), algo_bit_name = path) 
    return outputText

def algounitWriter(obj,conditions):
    templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))    # this has to be changed there seems to be a version of this thats called packageloader instead of filesystemloader
    templateEnv = jinja2.Environment(loader=templateLoader,trim_blocks=True,lstrip_blocks=True)
    template = templateEnv.get_template("algounit.template",)
    outputText = template.render(algobits = obj.Assignment, Conditions = conditions)
    return outputText

def writeAlgounitToFile(filename,contents):
    f = open(filename,"w")
    f.write(contents)
    f.close()

    