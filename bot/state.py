from aiogram.fsm.state import State, StatesGroup

class xabar(StatesGroup):
  text = State()

class zakaz(StatesGroup):
  telefon = State()
  tolov = State()
  tasdiq = State()
  joylashuv = State()
  screenshot = State()