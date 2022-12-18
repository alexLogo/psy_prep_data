from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from copy import deepcopy
import time 

import classifications.configurations as cfg
from classifications.experiment_analysis import analysis
from classifications.utils import util
from classifications.one_model_analysis import subjects_iterations


if __name__ == "__main__":
    start = time.time()
    print(cfg.pathes.base_dir)
    name = 'gaze_wtb2'
    mode = 'clean'
    # new_model = RandomForestClassifier(n_estimators=1000, max_depth=5)
    new_model = LogisticRegression()
    
    
    # run AUC tailored
    print('AUC tailored')
    model =  deepcopy(new_model)
    res, models, matrices = analysis(model, test_set=cfg.objective_tests[1:2], feature_mode=mode)
    
    util.save_results(res, name)
    util.save_matrices(matrices, name)
    util.save_models(models, name)
    
    # run one_subject AUC
    # model =  deepcopy(new_model)
    # res, matrices = subjects_iterations(mode, model)
    # util.save_results(res, name+"_one")
    # util.save_matrices(matrices, name+"_one")
    
    
    
    # # run tailoerd subjective AUC
    # print('tailoerd subjective AUC')
    # model =  deepcopy(new_model)
    # res, models, matrices = analysis(model, test_set=cfg.subjective_tests, feature_mode=mode)
    # util.save_results(res, name+"_sub_model")
    
    # # shuffled AUC
    # print('shuffled subjective AUC')
    # model =  deepcopy(new_model)
    # res, models, matrices = analysis(model, test_set=cfg.subjective_tests[:1], feature_mode=mode, iterations=30)
    # util.save_results(res, name+"_sub_shuffle")
    
    # # shuffled AUC
    # print('shuffled objective AUC')
    # model =  deepcopy(new_model)
    # res, models, matrices = analysis(model, test_set=cfg.objective_tests[:1], feature_mode=mode, iterations=30)
    # util.save_results(res, name+"_obj_shuffle")
    
    end = time.time()
    print(f"Time: {end-start:.3f} sec")

    
    
    
