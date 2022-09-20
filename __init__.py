from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message

class ParrotSkill(MycroftSkill):

    def __init__(self):
        super(ParrotSkill, self).__init__()

    @intent_handler("Parrot.intent")
    def talkback(self, message):
        phrase = message.data.get('phrase')
        self.speak_dialog(phrase)

def create_skill():
    return ParrotSkill()
