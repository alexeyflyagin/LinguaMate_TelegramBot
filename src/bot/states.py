from aiogram.fsm.state import StatesGroup, State


class AuthStates(StatesGroup):
    SendContact = State()


class MainStates(StatesGroup):
    Main = State()
    MyPhrases = State()


class AddPhraseModeStates(StatesGroup):
    EnterPhrase = State()


class AddWordModeStates(StatesGroup):
    EnterWord = State()
