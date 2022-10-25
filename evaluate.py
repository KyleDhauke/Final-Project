""" Evaluate a directory using museval, given a ground truth directory and an estimate directory.
    Files in both directories must have matching names. """

import museval
import os

reference_path = "../Training/test_new"
results_path = "../Results_new"

results = museval.EvalStore(frames_agg='median', tracks_agg='median')

for file in os.listdir(reference_path):
    print("Evaluating " + file)
    ref_dir = os.path.join(reference_path, file)
    res_dir = os.path.join(results_path, file)
    results.add_track(museval.eval_dir(ref_dir, res_dir))

print(results)
results.save('train.pandas')
