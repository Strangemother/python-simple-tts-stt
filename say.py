import time
import os
import subprocess
import audio
import os
from comlib import *

import to_string

BASEPATH = os.path.abspath(os.path.dirname(__file__))
EXE_PATH = os.path.join(BASEPATH, "./lib/ffmpeg-20180310-950170b-win64-static\\bin\\ffmpeg.exe")


class VOICE:
    AMY = "IVONA 2 Amy OEM"
    CARLA = "IVONA 2 Carla OEM"
    ERIC = "IVONA 2 Eric - US English male voice [22kHz]"
    JENNIFER = "IVONA 2 Jennifer - US English female voice [22kHz]"
    JOEY = "IVONA 2 Joey - US English male voice [22kHz]"
    SALLI = "IVONA 2 Salli - US English female voice [22kHz]"

    KIMBERLY = "IVONA 2 Kimberly - US English female voice [22kHz]"
    MS_ANNA = "Microsoft Anna - English (United States)"
    FIONA = "Vocalizer Expressive Fiona Harpo 22kHz"
    TESSA = "Vocalizer Expressive Tessa Harpo 22kHz"


# voice_set = ("IVONA 2 Joey - US English male voice [22kHz]", 0)

SETTINGS = dict(
    word_file='./words.txt',
    covert_output_dir='static/output',
    persona=dict(
        voice=VOICE.SALLI,
        speed=0,
    ),
    effects=dict(
        chorus_standard=('chorus', (
                (10, 0.4, 0.7, 2),
                (140, 0.4, 0.8, 0.8),
            ), )
    )
)

import re, unicodedata
import string, random


def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


def rand(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def main(conf=None, **kw):
    # response = speech.input("Say something, please.")
    # speech.say("Simple speech")
    print('Running Speech conversion')
    config = conf or SETTINGS
    config.update(kw)
    words = extract_words(config)
    persona = config['persona']
    voice_set = [persona['voice'], persona['speed']]
    r_name = "{}-{}".format(slugify(words), rand())
    r_name = "{}".format(rand())

    create_say_effect(voice_set, words,
        raw_filename=r_name,
        out_filename=r_name,
        output_dir=config['covert_output_dir'])
    time.sleep(.5)

    r_name = "{}.mp3".format(r_name)
    to_string.main(
        dirpath=config['covert_output_dir'],
        input_filename=r_name,
        )
    config['created_file'] = r_name
    return config


def extract_words(config):
    config = config or {}
    words = config.get('text', None)

    if words is None:
        with open(config.get('filepath', './words.txt'), 'r') as stream:
            s = stream.readlines()
            words = ''.join(s)

    return words


def create_speech_file(voice_set, filepath, string):

    if os.path.isfile(filepath):
        print('deleting old "{}"'.format(filepath))
        os.unlink(filepath)

    sapi = text_to_mp3(voice_set, string, filepath)
    count = 0

    while os.path.isfile(filepath) is False:
        time.sleep(.3)
        if count > 10:
            print('File not created "{}"'.format(filepath))
            return False
        count += 1

    time.sleep(.1)
    print("File Created", filepath)
    return sapi


def create_effect_file(in_filepath, out_filename):
    apply_effect(in_filepath, out_filename)
    #audio.play_file(out_filename)


def create_say_effect(voice_set, string,
            raw_filename='raw_output',
            out_filename='output',
            ext='mp3',
            output_dir=None):
    output_dir = output_dir or ''
    raw_fn = os.path.abspath('{}.{}'.format(os.path.join(output_dir, raw_filename), ext))
    outfile = os.path.abspath('{}.{}'.format(os.path.join(output_dir, out_filename), ext))

    sapi = create_speech_file(voice_set, raw_fn, string)
    create_effect_file(raw_fn, outfile)


def create_say(voice_set, string,
            raw_filename='raw_output',
            out_filename='output',
            ext='mp3',
            output_dir=None):
    """Convert the given string to a text to speech file.

    Arguments:
        string {Str} -- The text work to convert

    Returns:
        bool -- False for faailure
    """

    sapi = Sapi()

    output_dir = output_dir or ''
    raw_fn = os.path.abspath('{}.{}'.format(os.path.join(output_dir, raw_filename), ext))
    outfile = os.path.abspath('{}.{}'.format(os.path.join(output_dir, out_filename), ext))

    if(os.path.isfile(raw_fn)):
        print('deleting old "{}"'.format(raw_fn))
        os.unlink(raw_fn)

    # for name in sapi.get_voice_sets():
    #     print(name)

    sapi.set_voice(voice_set[0])
    sapi.set_rate(voice_set[1])
    sapi.create_recording(raw_fn, string)

    print("File Created", raw_fn)

    count = 0
    while os.path.isfile(raw_fn) is False:
        time.sleep(.5)
        print('Deleting', raw_fn)
        if count > 10:
            print('File not created "{}"'.format(raw_fn))
            return False
        count += 1
    time.sleep(.5)

    # apply_effect(raw_fn, outfile)
    # audio.play_file(outfile)


def text_to_mp3(voice_set, string, filename):
    sapi = Sapi()
    sapi.set_voice(voice_set[0])
    sapi.set_rate(voice_set[1])
    sapi.create_recording(filename, string)
    return sapi
    # for name in sapi.get_voice_sets():
    #     print(name)


def create_call_string(in_file, out_file, filter_string=''):
    # https://ffmpeg.org/ffmpeg.html#Main-options
    in_str = "-i {} -y".format(in_file)
    out_str = '{}'.format(out_file)
    rp = ' '.join(['"{}"'.format(EXE_PATH), in_str, filter_string, out_str])
    return rp

def apply_effect(in_file, out_file):

    filter_str = audio.create_filter_string()
    run_str = create_call_string(in_file, out_file, filter_string=filter_str)
    print("Running", run_str)
    subprocess.call(run_str)
    return run_str


def listen():
    def callback(phrase, listener):
        if phrase == "goodbye":
            listener.stoplistening()
        speech.say(phrase)

    listener = speech.listenforanything(callback)
    while listener.islistening():
        time.sleep(.5)

import win32com
from win32com.client import DispatchWithEvents, Dispatch

# Pointer = win32com.client.getevents("SAPI.SpSharedRecoContext")

class E:
  def OnWord(self, *a):
    print('word', a)

e = DispatchWithEvents('SAPI.SpVoice', E)

class Sapi(object):
    """A speech API using the Microsoft SAPI through COM"""

    def __init__(self):
        self.voice = comtypes.client.CreateObject('Sapi.SpVoice')
        self.voice.EventInterests = 16

    def get_voices(self, name=''):
        """Get a list of voices, search by name optional"""
        voice_list = []
        voices = self.voice.GetVoices()

        if name is not '':
            for voice in voices:
                if name in voice.GetDescription():
                    voice_list.append(voice)
                    break
            else:
                print('Voice not found')
        else:
            for voice in voices:
                voice_list.append(voice)

        return voice_list

    def get_voice_sets(self):
        """Get the names of all the voices"""
        return [voice.GetDescription() for voice in self.get_voices()]

    def set_voice(self, voice):
        """Set the voice to the given voice"""
        if type(voice) is str:
            self.voice.Voice = self.get_voices(voice)[0]
        else:
            self.voice.Voice = voice
        return

    def get_audio_outputs(self, name=''):
        """Get the audio outputs, search for the one with the name if given"""
        output_list = []
        outputs = self.voice.GetAudioOutputs()

        if name is not '':
            for output in outputs:
                if name in output.GetDescription():
                    output_list.append(output)
                    break
            else:
                print('Audio output not found')
        else:
            for output in outputs:
                output_list.append(output)

        return output_list

    def get_audio_output_names(self):
        """Get the names of all the audio outpus"""
        return [output.GetDescription() for output in self.get_audio_outputs()]

    def set_audio_output(self, output):
        if type(output) is str:
            self.voice.AudioOutput = self.get_audio_outputs(output)[0]
        else:
            self.voice.AudioOutput = output
        return

    def say(self, message):
        self.voice.Speak(message)
        return

    def set_rate(self, rate):
        """Set the speed of the speaker
        -10 is slowest, 10 is fastest"""
        self.voice.Rate = rate

    def _create_stream(self, filename):
        """Create a file stream handler"""
        stream = comtypes.client.CreateObject('Sapi.SpFileStream')
        stream.Open(filename, SpeechLib.SSFMCreateForWrite, True)
        return stream

    def create_recording(self, filename, message):
        """Make a recording of the given message to the file
        The file should be a .wav as the output is
        PCM 22050 Hz 16 bit, Little endianness, Signed"""
        stream = self._create_stream(filename)
        temp_stream = self.voice.AudioOutputStream
        self.voice.AudioOutputStream = stream
        self.say(message)
        self.voice.AudioOutputStream = temp_stream


if __name__ == '__main__':
    main()
