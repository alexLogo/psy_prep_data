from random import randint, seed
def create_labeler(idx=0, class_dict=False):
  
    # define the classifier function
    def labeler(trial_header):
        # if idx is -1, we will create random labeler
        if idx == -1:
            return randint(0, 1)
        if isinstance(idx, int):
            key = trial_header[idx]
        else:
            key = tuple(trial_header[idx])
        return class_dict.get(key, 2)
    
    return labeler