from spleeter.separator import Separator
from transcriber import transcribe
from argparse import ArgumentParser
import librosa
from os import path


def wav_to_midi():
    ''' Takes a drum wav as input, produces a MIDI transcription as output.'''

    # Parse command line input
    parser = ArgumentParser()
    parser.add_argument('-i', '--ifile')  # Input file
    parser.add_argument('-o', '--ofile')  # Output file
    parser.add_argument('-c', '--config')  # Config file for model (.json). Currently drum_config_new.json
    args = parser.parse_args()

    # Prepare separator
    separator = Separator(args.config)

    # Calculate BPM
    y, sr = librosa.load(args.ifile)
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    bpm = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)

    # Separate and transcribe
    separator.separate_to_file(args.ifile, 'drumparts')
    transcribe('drumparts/HH.wav', 'drumparts/KD.wav', 'drumparts/SD.wav', args.ofile, bpm)


def main():
    wav_to_midi()


if __name__ == '__main__':
    main()
