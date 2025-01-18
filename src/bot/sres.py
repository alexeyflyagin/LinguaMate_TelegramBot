class GENERAL:
    ACTION_CANCELED = "The current action has been cancelled 👌"


class AUTH:
    SEND_CONTACT_REQUEST = "*You're not authorized.* Please send me your contact info for authorization."
    SUCCESS = "🎉 *You have successfully logged in.* Hello {nickname}!"

    class BTN:
        SEND_CONTACT = "✅ Send my contact"


class PHRASE:
    class ADD_FAST:
        SUCCESS = "✅ The new phrase has been *successfully added*!"

        class ERROR:
            NO_ARGS = "🤨 A new phrase was expected after the command...\n e.g.: `/phrase new phrase::новая фраза::еще один перевод`"
            INCORRECT_ARGS = "🤨 There is an error in the format of the new phrase. Please check and try again...\ne.g.: `/phrase new phrase::новая фраза::еще один перевод`"
            NO_TRANSLATION = "🤨 At least one translation is required. Please try again...\ne.g.: `/phrase new phrase::новая фраза::еще один перевод`"
            ALREADY_EXIST = "🤨 Ops! This phrase *already exists in your phrasebook*."


class CHECK:
    class ERROR:
        CONTENT_TYPE = "🤨 Hmm... The message has unexpected content. Please try again..."
        EMPTY_COMMAND_ARGS = "🤨 The args were expected after the command..."


class ERROR:
    UNEXPECTED = "Ops! An unexpected error has occurred..."
