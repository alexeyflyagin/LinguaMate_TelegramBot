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
            ALREADY_EXISTS = "🤨 Ops! This phrase *already exists in your phrasebook*."

    class ADD_MODE:
        ENTER_PHRASE = "✏️ *The phrase-adding mode is activated.* Enter the phrases one by one...\n/exit — leave the phrase-adding mode."
        SUCCESS = "✅ *Successfull*! Added {added_count} phrase(s)\n/exit — leave the phrase-adding mode."
        EXIT = "You exited the phrase-adding mode 👌"

        class ERROR:
            INCORRECT_CONTENT = "🤨 There is an error in the format of the new phrase. Please check and try again...\ne.g.:\n`/phrase new phrase::новая фраза::еще один перевод\n/let's start!::давай начнём!\n/exit — leave the phrase-adding mode."
            NO_TRANSLATION = "🤨 At least one translation is required. Please try again...\ne.g.: `/phrase new phrase::новая фраза::еще один перевод`\n/exit — leave the phrase-adding mode."
            ALREADY_EXIST = "🤨 Ops! These phrases *already exist in your phrasebook*.\n/exit — leave the phrase-adding mode."


class CHECK:
    class ERROR:
        CONTENT_TYPE = "🤨 Hmm... The message has unexpected content. Please try again..."
        EMPTY_COMMAND_ARGS = "🤨 The args were expected after the command..."


class ERROR:
    UNEXPECTED = "Ops! An unexpected error has occurred..."
