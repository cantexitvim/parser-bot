from aiogram.types import KeyboardButton, KeyboardButtonRequestChat, ReplyKeyboardMarkup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Connect", style="primary"),
            KeyboardButton(text="Run", style="danger"),
            KeyboardButton(text="Help", style="success"),
        ]
    ],
    resize_keyboard=True,
)

connect = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Choose the channel you want to connect",
                style="primary",
                request_chat=KeyboardButtonRequestChat(
                    request_id=1,
                    chat_is_channel=True,
                    can_manage_chat=True,
                    can_post_messages=True,
                    bot_is_member=True,
                ),
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
