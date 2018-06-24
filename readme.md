Simple Text to Speech with fancy effects using ffmpeg on Windows

http://sox.sourceforge.net/sox.html#EFFECTS

# getting started

python 3 with requirements.txt

    env3/Scripts/activate
    py say.py

It will read the 'words.txt' into an mp3 file and apply effects using ffmpeg.
Using the internal TTS lib (Windows in this case).

I also purchased _amazon polly_ voice - but I prefer IVONA Salli.

## API

In working progress the main API essentially creates strings to apply ffmpeg cli. All the given classes wrap a string generator for complex filters.
