import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import math


def sensitivity(tp, fn):
    return tp/(tp + fn)


def precision(tp, fp):
    return tp/(tp + fp)


def accuracy(tp, tn, fp, fn):
    return (tp + tn)/(tp + tn + fp + fn)


def f_measure(tp, fp, fn):
    return 2*tp/(2*tp + fp + fn)


# Rounds x to the nearest a, used as a tolerance window.
def round_nearest(x, a):
    return round(round(x / a) * a, -int(math.floor(math.log10(a))))


tp = 0      # Is the note there in the ground truth and there in the prediction?
tn = 0      # Is a note correctly not bleeding in from a different instrument when it could be?
fp = 0      # Is a note detected when it shouldn't be here?
fn = 0      # Is a note supposed to be detected here, but isn't?

pred_files = "../Results_new"
truth_files = "../Training/test_new"

for file in os.listdir(pred_files):

    # Store all onsets so that true negatives can be calculated by seeing if onsets that could cause bleeding don't

    hh_pred = []
    hh_truth = []
    kd_pred = []
    kd_truth = []
    sd_pred = []
    sd_truth = []

    for subfile in os.listdir(os.path.join(pred_files, file)):

        print("Calculating " + subfile + "...")

        # Find onsets
        x, sr = librosa.load(os.path.join(pred_files, file, subfile))
        y, sr2 = librosa.load(os.path.join(truth_files, file, subfile))

        onset_frames_x = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
        onset_times_x = librosa.frames_to_time(onset_frames_x)

        onset_frames_y = librosa.onset.onset_detect(y, sr=sr2, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
        onset_times_y = librosa.frames_to_time(onset_frames_y)

        # Tolerance window
        round_to = 0.02

        # Store predictions and ground truth for each instrument.
        if "HH" in subfile:
            hh_pred = [round_nearest(num, round_to) for num in onset_times_x]
            hh_truth = [round_nearest(num, round_to) for num in onset_times_y]
        elif "KD" in subfile:
            kd_pred = [round_nearest(num, round_to) for num in onset_times_x]
            kd_truth = [round_nearest(num, round_to) for num in onset_times_y]
        elif "SD" in subfile:
            sd_pred = [round_nearest(num, round_to) for num in onset_times_x]
            sd_truth = [round_nearest(num, round_to) for num in onset_times_y]
        else:
            print("Whoops, seems like something was neither HH, KD nor SD!")
            break

    # Calculate true positive rate, false positive rate
    def positives(predictions, truth):
        global tp
        global fp
        for num in predictions:
            if num in truth:
                tp += 1

            elif num not in truth:
                fp += 1

            else:
                print("Ooopsie there's some kinda error here")
                break

    positives(hh_pred, hh_truth)
    positives(kd_pred, kd_truth)
    positives(sd_pred, sd_truth)

    # Calculate false negative rate
    def f_negatives(predictions, truth):
        global fn
        for num in truth:
            if num not in predictions:
                fn += 1

    f_negatives(hh_pred, hh_truth)
    f_negatives(kd_pred, kd_truth)
    f_negatives(sd_pred, sd_truth)

    # Calculate true negative rate
    def t_negatives(predictions, truth, bleed1, bleed2):
        # If an onset is in bleed, but not in predictions nor truth, then it can be considered a true negative
        # That'd mean the source separation was successful enough here
        global tn

        # First, combine bleed onsets into one list
        # Adapted from https://stackoverflow.com/questions/1319338/combining-two-lists-and-removing-duplicates-without-removing-duplicates-in-orig
        bleed = list(bleed1)
        bleed.extend(b for b in bleed2 if b not in bleed)

        # If something is in bleed but not in truth nor predictions, then it has been correctly filtered out and is a true negative
        for onset in bleed:
            if (onset not in truth) and (onset not in predictions):
                tn += 1

    t_negatives(hh_pred, hh_truth, sd_truth, kd_truth)
    t_negatives(sd_pred, sd_truth, hh_truth, kd_truth)
    t_negatives(kd_pred, kd_truth, hh_truth, sd_truth)

# Print results
print("Total (sans TN): " + str(tp + fp + fn))
print("TP: " + str(tp))
print("TN: " + str(tn))
print("FP: " + str(fp))
print("FN: " + str(fn))

print("Sensitivity: " + str(sensitivity(tp, fn)))
print("Precision: " + str(precision(tp, fp)))
print("Accuracy: " + str(accuracy(tp, tn, fp, fn)))
print("F-measure: " + str(f_measure(tp, fp, fn)))

# Plot onsets on a graph
'''plt.subplot(2, 1, 1)
librosa.display.waveplot(x)
plt.vlines(onset_times_x, 0, 0.2, color='r', alpha=0.9, linestyle='--', label='Onsets')

plt.subplot(2, 1, 2)
librosa.display.waveplot(y)
plt.vlines(onset_times_y, 0, 0.2, color='r', alpha=0.9, linestyle='--', label='Onsets')
plt.show()'''
