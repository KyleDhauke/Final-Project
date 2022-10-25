# Transcribes a set of HH, KD and SD into a midi file.
from onsets import get_onsets, get_delta_times
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
import operator


def calculate_ticks(note_time_ms, bpm, ppq):
    return int(note_time_ms/60000*ppq*bpm)


def onsets_to_tuples(note, onsets, bpm, ppq):
    r_onsets = [calculate_ticks(round(num*1000), bpm, ppq) for num in onsets]
    return [(note, onset) for onset in r_onsets]


def transcribe(hh, kd, sd, output, bpm, ppq=96):
    '''
    Transcribes a set of hh, kd, sd wav files into a midi file.
    '''
    # Initialise midi file
    mid = MidiFile()
    track = MidiTrack()
    tempo_track = MidiTrack()
    mid.tracks.append(tempo_track)
    mid.tracks.append(track)

    # FL Studio uses 96 ticks per beat, hence the default ppq is 96.
    mid.ticks_per_beat = ppq

    # Generate an index of what instrument plays at what time.
    timeline = []

    # HH = 42, KD = 35, SD = 38
    # get_onsets() is a simple function which returns the onsets of a file using librosa.
    timeline += onsets_to_tuples(42, get_onsets(hh), bpm, ppq)
    timeline += onsets_to_tuples(35, get_onsets(kd), bpm, ppq)
    timeline += onsets_to_tuples(38, get_onsets(sd), bpm, ppq)

    # We now have a list of tuples, describing what not plays at what time.
    # However, these are not ordered.
    # Since MIDI messages proceed linearly through time, we must first sort them
    timeline.sort(key=operator.itemgetter(1))

    # Since MIDI is based on delta time (time since last message, we must convert the timeline to one of delta times.
    delta_timeline = [timeline[0]]
    delta_timeline += [(timeline[n][0], timeline[n][1]-timeline[n-1][1]) for n in range(1, len(timeline))]

    # Set the tempo
    tempo_track.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm)))

    # Add the MIDI messages in sequence
    for n in delta_timeline:
        track.append(Message('note_off', note=n[0], channel=10, time=n[1]))
        track.append(Message('note_on', note=n[0], channel=10, time=0))

    mid.save(output)


def main():
    path = "midi_groove/rock_groove"
    transcribe(path + '/HH.wav', path + '/KD.wav', path + '/SD.wav', 'trial.mid', 130)


if __name__ == "__main__":
    main()
