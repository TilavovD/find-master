from telegram import ReplyKeyboardMarkup, KeyboardButton
from tgbot.handlers.onboarding import static_text

from tgbot.handlers.onboarding.static_text import need_master, i_am_master


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    buttons = [
        [need_master, i_am_master],
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_number_sharing() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton(text="Raqamni ulashish", request_contact=True)]],
        resize_keyboard=True
    )


def make_keyboard_for_remain_anonymous() -> ReplyKeyboardMarkup:
    buttons = [
        ["Anonim qoldirish"],
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)