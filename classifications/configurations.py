import pathes 

header_size = 3
num_of_features = 8657
num_of_participants = 5 #pathes.num_of_subjects
cluster_size = [2,4,6,8]
k_list = [5,7,10,15,20,25]

k_validation = 10

random_seed = 42
np_seed = 42

class_threshold = {'cv': 15, 'lto': 10}

participants_range = range(1, num_of_participants + 1)
fake_participants_range = range(200, 225)

restrictions = [10, 6, 6, 6, 6, 6, 6]

tests_random_configurations = [{'name': 'all manipulation', 'filter' :(1, [0,1,2,3]), 'labeler': (1, {0:0, 1:1, 2:1, 3:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': 'all agency', 'filter' :(1, [0,1,2,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': 'all agency unconfounded', 'filter' :(1, [0,1,2,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': '100ms manipulation', 'filter' :(1, [0,1]), 'labeler': (1, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '200ms manipulation', 'filter' :(1, [0,2]), 'labeler': (1, {0:0, 2:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '300ms manipulation', 'filter' :(1, [0,3]), 'labeler': (1, {0:0, 3:1}), 'validation':'cv', 'unconfound' : False},]

test_random_names = ['id'] + [x['name'] for x in tests_random_configurations]


objective_tests = [{'name': 'all manipulation', 'filter' :(1, [0,1,2,3]), 'labeler': (1, {0:0, 1:1, 2:1, 3:1}), 'validation':'cv', 'unconfound' : False},
                    {'name': '50ms manipulation', 'filter' :(1, [0,1]), 'labeler': (1, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                    {'name': '100ms manipulation', 'filter' :(1, [0,2]), 'labeler': (1, {0:0, 2:1}), 'validation':'cv', 'unconfound' : False},
                    {'name': '150ms manipulation', 'filter' :(1, [0,3]), 'labeler': (1, {0:0, 3:1}), 'validation':'cv', 'unconfound' : False},
                    {'name': 'unconcious manipulation', 'filter' :([1,2], [(0,1), (1,1)]), 'labeler': (1, {0:0, 1:1}), 'validation':'lto' , 'unconfound': False},]

subjective_tests = [{'name': 'all agency', 'filter' :(1, [0,1,2,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                    {'name': '50ms agency', 'filter' :(1, [0,1]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                    {'name': '100ms agency', 'filter' :(1, [0,2]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                    {'name': '150ms agency', 'filter' :(1, [0,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},]


if pathes.dataset_mode == 'ophir':
    objective_tests[0]['filter'] = (1, [0,1,2,3,4])
    objective_tests[0]['labeler'] = (1, {0:0, 1:1, 2:1, 3:1, 4:1})         
    objective_tests.insert(4, {'name': '200ms manipulation', 'filter' :(1, [0,4]), 'labeler': (1, {0:0, 4:1}), 'validation':'cv', 'unconfound' : False} )
    
    subjective_tests[0]['filter'] = (1, [0,1,2,3,4])
    subjective_tests.insert(4, {'name': '200ms manipulation', 'filter' :(1, [0,4]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False})

tests_configurations = [{'name': 'all manipulation', 'filter' :(1, [0,1,2,3]), 'labeler': (1, {0:0, 1:1, 2:1, 3:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': 'all agency', 'filter' :(1, [0,1,2,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': 'all agency unconfounded', 'filter' :(1, [0,1,2,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': '100ms manipulation', 'filter' :(1, [0,1]), 'labeler': (1, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '100ms agency', 'filter' :(1, [0,1]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '100ms agency unconfounded', 'filter' :(1, [0,1]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': '200ms manipulation', 'filter' :(1, [0,2]), 'labeler': (1, {0:0, 2:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '200ms agency', 'filter' :(1, [0,2]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '200ms agency unconfounded', 'filter' :(1, [0,2]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': '300ms manipulation', 'filter' :(1, [0,3]), 'labeler': (1, {0:0, 3:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '300ms agency', 'filter' :(1, [0,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '300ms agency unconfounded', 'filter' :(1, [0,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': 'unconcious manipulation', 'filter' :([1,2], [(0,1), (1,1)]), 'labeler': (1, {0:0, 1:1}), 'validation':'lto' , 'unconfound': False},]

tests_configurations_s = [{'name': 'all manipulation', 'filter' :(1, [0,4,5,6]), 'labeler': (1, {0:0, 4:1, 5:1, 6:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': 'all agency', 'filter' :(1, [0,4,5,6]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': 'all agency unconfounded', 'filter' :(1, [0,4,5,6]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': '100ms manipulation', 'filter' :(1, [0,4]), 'labeler': (1, {0:0, 4:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '100ms agency', 'filter' :(1, [0,4]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '100ms agency unconfounded', 'filter' :(1, [0,4]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': '200ms manipulation', 'filter' :(1, [0,5]), 'labeler': (1, {0:0, 5:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '200ms agency', 'filter' :(1, [0,5]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '200ms agency unconfounded', 'filter' :(1, [0,5]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': '300ms manipulation', 'filter' :(1, [0,6]), 'labeler': (1, {0:0, 6:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '300ms agency', 'filter' :(1, [0,6]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '300ms agency unconfounded', 'filter' :(1, [0,6]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': 'unconcious manipulation', 'filter' :([1,2], [(0,1), (4,1)]), 'labeler': (1, {0:0, 4:1}), 'validation':'lto' , 'unconfound': False},]



test_names = ['id'] + [x['name'] for x in tests_configurations]





tests_configurations_v1 = [{'name': 'all manipulation', 'filter' :(1, [0,1,2,3]), 'labeler': (1, {0:0, 1:1, 2:1, 3:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': 'all agency', 'filter' :(1, [0,1,2,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': 'all agency unconfounded', 'filter' :(1, [0,1,2,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': '100ms manipulation', 'filter' :(1, [0,1]), 'labeler': (1, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '100ms agency', 'filter' :(1, [0,1]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '100ms agency unconfounded', 'filter' :(1, [0,1]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': '200ms manipulation', 'filter' :(1, [0,2]), 'labeler': (1, {0:0, 2:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '200ms agency', 'filter' :(1, [0,2]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '200ms agency unconfounded', 'filter' :(1, [0,2]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': '300ms manipulation', 'filter' :(1, [0,3]), 'labeler': (1, {0:0, 3:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '300ms agency', 'filter' :(1, [0,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : False},
                        {'name': '300ms agency unconfounded', 'filter' :(1, [0,3]), 'labeler': (2, {0:0, 1:1}), 'validation':'cv', 'unconfound' : True},
                        {'name': '0ms inside agency', 'filter' :(1, [0]), 'labeler': (2, {0:0, 1:1}), 'validation': 'lto', 'unconfound' : False},
                        {'name': '100ms inside agency', 'filter' :(1, [1]), 'labeler': (2, {0:0, 1:1}), 'validation': 'lto','unconfound' : False},
                        {'name': '200ms inside agency', 'filter' :(1, [2]), 'labeler': (2, {0:0, 1:1}), 'validation':'lto', 'unconfound' : False},
                        {'name': '300ms inside agency', 'filter' :(1, [3]), 'labeler': (2, {0:0, 1:1}), 'validation': 'lto', 'unconfound' : False},
                        {'name': 'unconcious manipulation', 'filter' :([1,2], [(0,1), (1,1)]), 'labeler': (1, {0:0, 1:1}), 'validation':'lto' , 'unconfound': False},]
