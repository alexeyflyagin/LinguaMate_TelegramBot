from aiogram.fsm.state import StatesGroup, State


class AuthStates(StatesGroup):
    SendContact = State()

class MainStates(StatesGroup):
    Main = State()

class AddPhraseModeStates(StatesGroup):
    EnterPhrase = State()
