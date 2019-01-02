import numpy as np
import subprocess as sp
import sys
import os


def main(dirpath=None, filepath=None, input_filename='raw_output.mp3'):
    print("\n\n-- Creating waveform\n")
    pp=sp.Popen(['ffmpeg', '-i', os.path.join(dirpath or '', input_filename),
        '-ar', '22050', # 22050 Hz, produces, 88200 pairs
        '-f', 's16le',
        '-ac','2',
        '-acodec', 'pcm_s16le',
        '-'], stdout=sp.PIPE, bufsize=10**8)
    v = b''
    while True:
        chunk = pp.stdout.read(88200)
        v += chunk
        if len(chunk) == 0:
            break

    aa=np.fromstring(v, dtype='int16')
    #aa = norm_raw(aa, .7, -.5)
    filepath =  filepath or 'ss.js'
    if dirpath is not None:
        filepath = os.path.join(dirpath, filepath)

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    print('Saving to', filepath)
    js_file(filepath, aa)

def norm_raw(rawpoints, high=100.0, low=0.0):
    mins = np.min(rawpoints)
    maxs = np.max(rawpoints)
    rng = maxs - mins
    return high - (((high - low) * (maxs - rawpoints)) / rng)

def norm_numpy(aa, ma, m):
    return (aa-m)/(ma-m)

def with_flip(aa):
    with open('foo.txt', 'w') as stream:
        flip = True
        _max = 0
        _min = 0
        started = False
        for v in aa:

            flip = not flip
            _min = min(_min, v)
            _max = max(_max, v)
            if (v == 0) and (started is False):
                continue
            started=True

            stream.write('{}{}'.format(v, ',\n' if flip else ','))

        print('min', _min)
        print('max', _max)

# def make_peaks(bottom, upper, list):


def js_file(filepath, aa):
    # aa= make_peaks(-1, 1, aa)
    print('Writing {}'.format(filepath))
    with open(filepath, 'w') as stream:

        stream.write('{}'.format('var wordString = ['))
        _max = 0
        _min = 0
        started = False
        limit=20
        i=0
        for v in aa:
            _min = min(_min, v)
            _max = max(_max, v)
            i+=1
            if (v == 0) and (started is False):
                continue
            started=True
            stream.write('{}{}'.format(v, ',{}'.format('\n' if i == limit else '')))
            if i > limit:
                i =0

        stream.write('{}'.format(']'))
        print('min', _min)
        print('max', _max)

    # p=sp.Popen(['ffmpeg','-i','output.mp3','-'], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)

#main()
