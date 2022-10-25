import librosa
import os
import csv

path = 'validation_new'
with open('drum_' + path + '.csv', 'w', newline = '') as file:
    w = csv.writer(file)
    w.writerow(['mix_path', 'HH_path', 'SD_path', 'KD_path', 'duration'])
    current_row = ['', '', '', '', '']
    for filename in os.listdir('Training\\' + path):
        if "HH" in filename and "#train" not in filename:
            current_row[1] = path + '\\' + filename
        elif "KD" in filename and "#train" not in filename:
            current_row[3] = path + '\\' + filename
        elif "MIX" in filename and "#train" not in filename:
            current_row[0] = path + '\\' + filename
            current_row[4] = librosa.get_duration(filename='Training\\' + path + '\\' + filename)
        elif "SD" in filename and "#train" not in filename:
            current_row[2] = path + '\\' + filename
        else:
            print("Skipped " + filename)
        if current_row[0] and current_row[1] and current_row[2] and current_row[3]:
            print(current_row)
            w.writerow(current_row)
            current_row = ['', '', '', '', '']

    # for filename in os.listdir('Training\\' + path):
    #     if "HH#train" in filename:
    #         current_row[1] = path + '\\' + filename
    #     elif "KD#train" in filename:
    #         current_row[3] = path + '\\' + filename
    #     elif "MIX#train" in filename:
    #         current_row[0] = path + '\\' + filename
    #         current_row[4] = librosa.get_duration(filename='Training\\' + path + '\\' + filename)
    #     elif "SD#train" in filename:
    #         current_row[2] = path + '\\' + filename
    #     else:
    #         print("Skipped " + filename)
    #     if current_row[0] and current_row[1] and current_row[2] and current_row[3]:
    #         print(current_row)
    #         w.writerow(current_row)
    #         current_row = ['', '', '', '', '']
