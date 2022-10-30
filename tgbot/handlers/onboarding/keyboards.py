from telegram import ReplyKeyboardMarkup, KeyboardButton

from master.models import Region, District
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
        [static_text.remain_anonym],
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_regions() -> ReplyKeyboardMarkup:
    regions = Region.objects.all()
    buttons = []
    row = []
    for region in regions:
        row.append(region.name)

        if len(row) == 2:
            buttons.append(row)
            row = []
    if len(row) == 1:
        buttons.append(row)
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_districts(region) -> ReplyKeyboardMarkup:
    districts = District.objects.filter(region=region)
    buttons = []
    row = []
    for district in districts:
        row.append(district.name)

        if len(row) == 2:
            buttons.append(row)
            row = []
    if len(row) == 1:
        buttons.append(row)
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
