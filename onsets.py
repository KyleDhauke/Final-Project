import librosa
import librosa.display
from matplotlib import pyplot as plt
import numpy as np


def get_onsets(file):
    # Gets onsets and bpm from a file
    x, sr = librosa.load(file)

    onset_frames_x = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
    onset_times_x = librosa.frames_to_time(onset_frames_x)

    return onset_times_x


def get_delta_times(onsets):
    # Returns a list of delta times given a list of onsets
    onsets = [int(round(num * 100, 0)) for num in onsets]
    dt = [0]
    for n, i in enumerate(onsets):
        if n == 0:
            prev = 0
        else:
            prev = onsets[n - 1]
        dt.append(i-prev)
    return dt


def display_onsets(file, title):
    x, sr = librosa.load(file)

    onset_frames_x = librosa.onset.onset_detect(x, sr=sr, wait=3, pre_avg=3, post_avg=3, pre_max=3, post_max=3)
    onset_times_x = librosa.frames_to_time(onset_frames_x)

    D = np.abs(librosa.stft(x))
    fig, ax = plt.subplots(nrows=2, sharex=True)
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                             x_axis='time', y_axis='log', ax=ax[0])
    ax[0].set(title=title)
    ax[0].label_outer()

    librosa.display.waveplot(x, ax=ax[1])
    plt.vlines(onset_times_x, 0 - x.max(), x.max(), color='r', alpha=0.9, linestyle='--', label='Onsets')
    plt.show()


def display_onsets_strength(file):
    x, sr = librosa.load(file)

    o_env = librosa.onset.onset_strength(x, sr=sr)
    times = librosa.times_like(o_env, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)

    D = np.abs(librosa.stft(x))
    fig, ax = plt.subplots(nrows=2, sharex=True)
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                             x_axis='time', y_axis='log', ax=ax[0])
    ax[0].set(title='Power spectrogram')
    ax[0].label_outer()
    ax[1].plot(times, o_env, label='Onset strength')
    ax[1].vlines(times[onset_frames], 0, o_env.max(), color='r', alpha=0.9,
                 linestyle='--', label='Onsets')
    ax[1].legend()
    plt.show()


if __name__ == "__main__":
    print(get_onsets('rock_groove.wav'))
    #display_onsets('rock_groove.wav', 'Basic Rock Groove')
