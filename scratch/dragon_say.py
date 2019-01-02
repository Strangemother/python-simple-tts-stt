import pythoncom
from time import sleep
from dragonfly.all import Grammar, CompoundRule

# Voice command rule combining spoken form and recognition processing.
class ExampleRule(CompoundRule):
    spec = "Sadie"                  # Spoken form of command.
    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        print "Voice command spoken."

# Create a grammar which contains and loads the command rule.
grammar = Grammar("example grammar")                # Create a grammar to contain the command rule.
grammar.add_rule(ExampleRule())                     # Add the command rule to the grammar.
grammar.load()

while True:
    try:
        pythoncom.PumpWaitingMessages()
    except e:
        print e
    sleep(.1)