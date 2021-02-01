# Message class contains the title and text of the message, so they can be retrieved from the database.
# Each message also has a type: 1 - Donation/Exchange, 2 - Sharing, 3 - Looking for
# Message has 3 mutators, to change the id, title and text as the user sees fit (For creation and editing purposes)
class Message:
    def __init__(self, type):
        # Type of post. Not much difference at all between the 3 posts, hence not separate classes.
        # 1 - Offering items, 2 - Sharing items, 3 - Looking for items
        self.type = type

        # Title and Text of post; To be set using the mutators
        self.title = ""
        self.text = ""

        #Status of post: id is 0 if it remains unsent; 1 or more otherwise
        self.id = 0           

        # Telegram has to know when to send a photo post or text post. photoid is the id of the photo file to pass to Telegram
        self.photoid = 0
        self.hasphoto = False

    # MUTATORS
    def set_title(self, title):
        self.title = title
    
    def set_text(self, text):
        self.text = text

    def set_id(self, id):
        self.id = id

    def set_photoid(self, photoid):
        self.photoid = photoid

    # Sets hasphoto to True if False, False if True
    def set_hasphoto(self):
        if self.hasphoto:
            self.hasphoto = False
        else:
            self.hasphoto = True

    #Generate the template message based on Message contents
    def generateMessage(self):
        type = ""
        if (self.type == 1):
            type = "OFFERING"
        elif (self.type == 2):
            type = "UP FOR SHARING"
        elif (self.type == 3):
            type = "LOOKING FOR"
        else:
            type = "???"    #Should not happen
        
        title = self.title
        text = self.text
        return '<b>' + type + '</b>\n<b>' + title + '</b>\n' + "====================\n" + text + '\n====================\n'