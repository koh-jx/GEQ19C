# The User class contains the name of the user, as well as a messageList,
# with values of type Message. As the user makes/deletes offers, the messageList will be updated with his/her current messages.
from Message import Message


class User:
    def __init__(self, name):
        # Name to call the User
        self.name = name

        # List of active messages that the User has send/edited.
        self.messageList = []

        # Should User want to access a certain message in messageList (through Manage Posts), this will track the requested index
        self.requestedIndex = 0
    
    # Adds a new message to the end of the messageList
    def addMessage(self, type):
        self.messageList.append(Message(type))

    # Lists all active messages that the User has
    def listMessages(self):    
        self.clearUnsentMessages()
        text = ""
        for i in range(len(self.messageList)):
            message = self.messageList[i]
            status = message.getstatus()
            text += (str(i + 1) + ": " + message.title + " " + status + '\n')
        return text

    # Deletes all unused messages in the messageList (To reduce space used, and easier listMessages functionality)
    def clearUnsentMessages(self):
        i = 0
        while (i < len(self.messageList)):
            if(self.messageList[i].id == 0):
                del self.messageList[i]
                continue
            i += 1
    
    # MUTATOR
    def setRequestedIndex(self, index):
        self.requestedIndex = index