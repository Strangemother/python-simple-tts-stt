# Sample code for speech recognition using the MS Speech API
# Inigo Surguy (inigosurguy@hotmail.com)
from win32com.client import constants
import win32com.client
import pythoncom

"""Sample code for using the Microsoft Speech SDK 5.1 via COM in Python.
    Requires that the SDK be installed (it's a free download from
            http://www.microsoft.com/speech
    and that MakePy has been used on it (in PythonWin,
    select Tools | COM MakePy Utility | Microsoft Speech Object Library 5.1).

    After running this, then saying "One", "Two", "Three" or "Four" should
    display "You said One" etc on the console. The recognition can be a bit
    shaky at first until you've trained it (via the Speech entry in the Windows
    Control Panel."""
class SpeechRecognition:
    """ Initialize the speech recognition with the passed in list of words """
    def __init__(self, wordsToAdd):
        # For text-to-speech
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        # For speech recognition - first create a listener
        self.listener = win32com.client.Dispatch("SAPI.SpSharedRecognizer")
        # Then a recognition context
        self.context = self.listener.CreateRecoContext()
        # which has an associated grammar
        self.grammar = self.context.CreateGrammar()
        # Do not allow free word recognition - only command and control
        # recognizing the words in the grammar only
        self.grammar.DictationSetState(0)
        # Create a new rule for the grammar, that is top level (so it begins
        # a recognition) and dynamic (ie we can change it at runtime)
        self.wordsRule = self.grammar.Rules.Add("wordsRule",
                        constants.SRATopLevel + constants.SRADynamic, 0)
        
        # Clear the rule (not necessary first time, but if we're changing it
        # dynamically then it's useful)
        self.wordsRule.Clear()
        # And go through the list of words, adding each to the rule
        [ self.wordsRule.InitialState.AddWordTransition(None, word) for word in wordsToAdd ]
        # Set the wordsRule to be active
        self.grammar.Rules.Commit()
        self.grammar.CmdSetRuleState("wordsRule", 1)
        # Commit the changes to the grammar
        self.grammar.Rules.Commit()
        # And add an event handler that's called back when recognition occurs
        self.eventHandler = ContextEvents(self.context)
        # Announce we've started
        self.say("Speech recognition tool started.")
    """Speak a word or phrase"""
    def say(self, phrase):
        self.speaker.Speak(phrase)


class GrammarState(object):

    def __init__(self):
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        self.listener = win32com.client.Dispatch("SAPI.SpSharedRecognizer")
        self.context = self.listener.CreateRecoContext()
        self.grammar = self.new_grammar()
        self.eventHandler = self.ContextEvents(self.context)
        self.eventHandler.parent = self
        # A list of created grammar lists of which have 
        # been added as a wordlist to
        # call upon
        self.grammars = []

    def say(self, phrase):
        self.speaker.Speak(phrase)

    def new_grammar(self):
        # which has an associated grammar
        grammar = self.context.CreateGrammar()
        # Do not allow free word recognition - only command and control
        # recognizing the words in the grammar only
        grammar.DictationSetState(0)

        return grammar

    def set_grammar(self, grammar_name):
        # set the name of the grammar list into the engine
        # if the grammar list has not been created, an error
        # will be thrown.
        if grammar_name in self.grammars:
            #for gram in self.grammars:
            #    self.grammar.CmdSetRuleState(gram, 0)
            self.grammar.CmdSetRuleState(grammar_name, 1)
            # Commit the changes to the grammar
            self.grammar.Rules.Commit()
            # And add an event handler that's called back when recognition occurs
            print("%s rules have been set. " % grammar_name)

    def lights(self):
        self.say('define lights.')
        self.set_grammar('lights')

    def add_diction(self, name, *args):

        wordsRule = self.grammar.Rules.Add(name,
                        constants.SRATopLevel + constants.SRADynamic, 0)
        
        # Clear the rule (not necessary first time, but if we're changing it
        # dynamically then it's useful)
        wordsRule.Clear()

        transit_rule = wordsRule.InitialState.AddWordTransition

        # And go through the list of words, adding each to the rule
        for word in args:
            transit_rule(None, word)
            transit_rule(None, '%s %s' % (name, word ) )
            transit_rule(None, '%s %s' % (word, name) )

        # Set the wordsRule to be active
        self.grammar.Rules.Commit()
        
        self.grammars.append(name)
        
        # Announce we've started
        print("New diction of '" + name  + "'' has been applied.")

    """The callback class that handles the events raised by the speech object.
        See "Automation | SpSharedRecoContext (Events)" in the MS Speech SDK
        online help for documentation of the other events supported. """
    class ContextEvents(win32com.client.getevents("SAPI.SpSharedRecoContext")):
        """Called when a word/phrase is successfully recognized  -
            ie it is found in a currently open grammar with a sufficiently high
            confidence"""
        def OnRecognition(self, StreamNumber, StreamPosition, RecognitionType, Result):
            newResult = win32com.client.Dispatch(Result)
            said = newResult.PhraseInfo.GetText()
            print "You said: ", self.parent,  said
            if hasattr(self.parent, said):
                print('%s command' % said)
                getattr(self.parent, said)()

if __name__=='__main__':
    wordsToAdd = [ "lights", "emails", "music", "door", "exit" ]
    # speechReco = SpeechRecognition(wordsToAdd)
    gs = GrammarState()
    gs.add_diction('lights', *['off', 'more', 'less', '10%', '20%', '30%', '40%', '50%', '60%' '70%', '80%', '90%', '100%' 'full']) 
    gs.add_diction('house', *wordsToAdd) 
    gs.set_grammar('house')
    while 1:
        pythoncom.PumpWaitingMessages()



