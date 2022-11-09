import argparse

import ROOT
from L1Trigger.Phase2L1GT.l1GTScales import scale_parameter

from DataFormats.FWLite import Events, Handle


def get_pathfilters(event, procname):

    if not hasattr(ROOT, "getPathNames"):
        ROOT.gInterpreter.Declare("""
#include "FWCore/ParameterSet/interface/ParameterSet.h"
std::vector<std::string> getPathNames(edm::ParameterSet& pset){
   const auto& pathPSet = pset.getParameterSet("@trigger_paths");
   if(pathPSet.exists("@trigger_paths")){
     return pathPSet.getParameter<std::vector<std::string>>("@trigger_paths");
   }else{
     return std::vector<std::string>();
   }
}
                """)

    if not hasattr(ROOT, "getFiltModules"):
        ROOT.gInterpreter.Declare("""
#include "FWCore/ParameterSet/interface/ParameterSet.h"
std::vector<std::string> getFiltModules(edm::ParameterSet& pset,const std::string& pathName){
   std::vector<std::string> filtMods;
   const auto& pathPSet = pset.getParameterSet("@trigger_paths");
   if(pset.existsAs<std::vector<std::string> >(pathName,true)){
     const auto& modules = pset.getParameter<std::vector<std::string>>(pathName);
     for(const auto& mod : modules){
        //ignored modules will start with - and this needs to be removed if present            
        if(pset.exists(mod.front()!=std::string("-") ? mod : mod.substr(1))){
           const auto& modPSet = pset.getParameterSet(mod.front()!=std::string("-") ? mod : mod.substr(1));
           if(modPSet.getParameter<std::string>("@module_edm_type")=="EDFilter") {
             if (modPSet.getParameter<std::string>("@module_type") == "L1GTDoubleObjectCond") {
               filtMods.push_back(mod + "::" + modPSet.getParameterSet("collection1").getParameter<edm::InputTag>("tag").instance());
               if (modPSet.getParameterSet("collection1").getParameter<edm::InputTag>("tag").instance() != 
                   modPSet.getParameterSet("collection2").getParameter<edm::InputTag>("tag").instance()) {
                 filtMods.push_back(mod + "::" + modPSet.getParameterSet("collection2").getParameter<edm::InputTag>("tag").instance());
               }
             }
             else if (modPSet.getParameter<std::string>("@module_type") == "L1GTSingleObjectCond"){
               filtMods.push_back(mod + "::" + modPSet.getParameter<edm::InputTag>("tag").instance());
             }
           }
        }
     }
   }
   return filtMods;
}
                """)

    cfg = ROOT.edm.ProcessConfiguration()
    proc_hist = event.object().processHistory()
    proc_hist.getConfigurationForProcess(procname, cfg)
    cfg_pset = event.object().parameterSet(cfg.parameterSetID())
    pathnames = ROOT.getPathNames(cfg_pset)
    path_filters = {}
    for path in pathnames:
        path_filters[str(path)] = [str(filt) for filt in ROOT.getFiltModules(cfg_pset, path)]

    return {path: modules for path, modules in path_filters.items() if len(modules) > 0}, pathnames


class TrigResults:
    """
    class acts as a name cache to allow the trigger results to be accessed
    by trigger name

    it takes as input the list of specific triggers to look for rather than 
    reading all possible triggers
    """

    def __init__(self, trigs, process, pathnames):
        self.process = process
        self.trig_indices = {x: [] for x in trigs}
        self.trig_res = {x: False for x in trigs}
        self._set_trig_indices(pathnames)

    def _set_trig_indices(self, pathNames):
        for name in self.trig_indices:
            self.trig_indices[name] = []

        for idx, trig_name in enumerate(pathNames):
            if str(trig_name) in self.trig_indices:
                self.trig_indices[str(trig_name)].append(idx)

    def _fill_trig_res(self, trig_res):
        for trig in self.trig_res:
            self.trig_res[str(trig)] = False  # resetting it
            for idx in self.trig_indices[str(trig)]:
                if trig_res[idx].accept():
                    self.trig_res[str(trig)] = True
                    break

    def fill(self, event):
        handle = Handle("edm::TriggerResults")
        event.getByLabel("TriggerResults", "", self.process, handle)
        self._fill_trig_res(handle.product())

    def result(self, trig):
        if trig in self.trig_res:
            return self.trig_res[trig]
        else:
            return False


def get_objs_passing_filter(event, filter_name, process):
    trig_res = Handle("l1t::P2GTCandidateVectorRef")
    event.getByLabel(*filter_name.split('::'), process, trig_res)

    passing_objs = {}
    for obj in trig_res.product():
        passing_objs[obj.key()] = obj.get()

    return passing_objs


def print_l1(event, l1_res, l1_name, l1_filtnames, process):

    if l1_res.result(l1_name) == True:
        passed_objs = {}
        for filter in l1_filtnames:
            l1_objs = get_objs_passing_filter(event, filter, process)
            tag = filter.split('::')[1]
            if tag in passed_objs:
                passed_objs[tag] = dict(l1_objs.items() & passed_objs[tag].items())
            else:
                passed_objs[tag] = l1_objs

        print("{} : {}, nr objs pass {}".format(
            l1_name, l1_res.result(l1_name), sum(len(v) for v in passed_objs.values())))
        for tag, objs in passed_objs.items():
            for key, obj in sorted(objs.items()):
                print(" {}: {} pt {:3.1f} eta {:3.2f} phi {:3.2f}".format(
                    tag, key, obj.hwPT() * scale_parameter.pT_lsb.value(),
                    obj.hwEta() * scale_parameter.eta_lsb.value(), obj.hwPhi() * scale_parameter.phi_lsb.value()))
    else:
        print("{} : {}, nr objs pass {}".format(l1_name, l1_res.result(l1_name), 0))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='L1GT analyzer')
    parser.add_argument('in_filename', nargs="+", help='input filename')
    parser.add_argument('--prefix', '-p', default='file:', help='file prefix')
    parser.add_argument('--process', '-P', default='L1', help='Process to analyze')

    args = parser.parse_args()

    in_filenames_with_prefix = ['{}{}'.format(args.prefix, x) for x in args.in_filename]
    events = Events(in_filenames_with_prefix)

    print("number of events", events.size())
    print('*' * 80)

    l1_res = None
    for idx, event in enumerate(events):
        print('Event:', idx)

        if l1_res == None:
            path_filters, pathnames = get_pathfilters(event, args.process)
            l1_res = TrigResults(path_filters.keys(), args.process, pathnames)

        l1_res.fill(event)

        for path, filters in path_filters.items():
            print_l1(event, l1_res, path, filters, args.process)

        print('*' * 80)
