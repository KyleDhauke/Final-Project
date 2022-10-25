from spleeter.separator import Separator
from transcriber import transcribe
from argparse import ArgumentParser
import librosa


def song_to_drums():
    '''Takes any song as input, produces a MIDI transcription of the drums in it.'''

    # Parse command line input
    parser = ArgumentParser()
    parser.add_argument('-i', '--ifile')  # Input file
    parser.add_argument('-o', '--ofile')  # Output file
    parser.add_argument('-c', '--config')  # Config file for model (.json). Currently drum_config_new.json
    args = parser.parse_args()

    # filename = args.ifile
    # filename = (filename.replace('.mp3', ''))

    # Prepare spleeter's separator
    separator_song = Separator('spleeter:4stems')

    # Calculate BPM
    y, sr = librosa.load(args.ifile)
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    bpm = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)

    # Separate stems.
    separator_song.separate_to_file(args.ifile, 'stems')

    # Separate and transcribe the drums.
    separator_drums = Separator(args.config)
    separator_drums.separate_to_file('stems/' + filename + '/drums.wav', 'drumparts')
    transcribe('drumparts/HH.wav', 'drumparts/KD.wav', 'drumparts/SD.wav', args.ofile, bpm)


# The following is a script safeguard to prevent scripts from behaving strangely.
def main():
    song_to_drums()


if __name__ == '__main__':
    main()
