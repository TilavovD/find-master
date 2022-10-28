import datetime
from io import BytesIO
import numpy as np
from django.utils import timezone
from telegram import ParseMode, Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from master.models import Master
from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_start_command, make_keyboard_for_number_sharing, \
    make_keyboard_for_remain_anonymous


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_start_command())


def need_master(update: Update, context: CallbackContext) -> int:
    text = static_text.name
    update.message.reply_text(text=text, reply_markup=ReplyKeyboardRemove())
    return 0


def name_handler(update: Update, context: CallbackContext) -> int:
    user = User.get_user(update, context)
    name = update.message.text
    Master.objects.create(name=name, user=user)

    update.message.reply_text(static_text.year_of_experience)

    return 1


def exp_handler(update: Update, context: CallbackContext) -> int:
    user = User.get_user(update, context)
    master = Master.objects.filter(user=user).last()
    exp_year = update.message.text
    try:
        exp_year = int(exp_year)
    except ValueError:
        update.message.reply_text(static_text.year_of_experience_error_text)
        update.message.reply_text(static_text.year_of_experience)
        return 1
    master.experience_year = exp_year
    master.save()
    update.message.reply_text(static_text.phone_number, reply_markup=make_keyboard_for_number_sharing())
    return 2


def phone_number_handler(update: Update, context: CallbackContext):
    user = User.get_user(update, context)
    master = Master.objects.filter(user=user).last()
    num_prefixes = ['99', '98', '97', '95', '94', '93', '91', '90', '88', '77', '33']
    if update.message.text:
        number = update.message.text
        text = static_text.phone_number_error_text
        if number[:4] == "+998" and number[4:6] in num_prefixes and len(number) == 13:
            try:
                _ = int(number[1:])
                master.phone_number = number
            except ValueError:
                update.message.reply_text(text, reply_markup=make_keyboard_for_remain_anonymous())
                return 2
        else:
            update.message.reply_text(text, reply_markup=make_keyboard_for_remain_anonymous())
            return 2

    elif update.message.contact:
        number = update.message.contact.phone_number
        master.phone_number = number
    master.save()
    update.message.reply_text(static_text.share_image_text, reply_markup=make_keyboard_for_remain_anonymous())
    return 3


def image_handler(update: Update, context: CallbackContext):
    print(update)
    user = User.get_user(update, context)
    master = Master.objects.filter(user=user).last()
    master.image = update.message.photo[-1].file_id

    master.save()
    context.bot.send_photo(chat_id=user.user_id, photo=master.image)


def secret_level(update: Update, context: CallbackContext) -> None:
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )
