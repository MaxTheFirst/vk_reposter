from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    menu = State()
    main_group = State()
    add_groups = State()
    del_groups = State()
    read_url = State()
    read_text = State()
