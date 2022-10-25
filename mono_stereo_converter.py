import wave
import array
from pydub import AudioSegment


def make_stereo(file1):
    """ Converts a file from mono to stereo."""

    ifile = wave.open(file1)
    # print(ifile.getparams())
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = ifile.getparams()
    assert comptype == 'NONE'
    array_type = {1:'B', 2: 'h', 4: 'l'}[sampwidth]
    left_channel = array.array(array_type, ifile.readframes(nframes))[::nchannels]
    ifile.close()

    stereo = 2 * left_channel
    stereo[0::2] = stereo[1::2] = left_channel

    ofile = wave.open(file1, 'w')
    ofile.setparams((2, sampwidth, framerate, nframes, comptype, compname))
    ofile.writeframes(stereo.tostring())
    ofile.close()


def make_mono(ifile):
    """ Converts a file from stereo to mono. """

    sound = AudioSegment.from_wav(ifile)
    sound = sound.set_channels(1)
    sound.export(ifile, format="wav")
