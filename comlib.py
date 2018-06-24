import speech
import comtypes.client  # Importing comtypes.client will make the gen subpackage
import os


try:
    assert(os.name == 'nt') # Checks for Windows
except:
    raise RuntimeError("Windows is required.")


try:
    from comtypes.gen import SpeechLib  # comtypes
except ImportError:
    # Generate the SpeechLib lib and any associated files
    engine = comtypes.client.CreateObject("SAPI.SpVoice")
    stream = comtypes.client.CreateObject("SAPI.SpFileStream")
    from comtypes.gen import SpeechLib
