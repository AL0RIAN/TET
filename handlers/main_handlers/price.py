from telebot import types
from datetime import datetime
from utils.utils import get_days
from config_data.constants import *


@bot.message_handler(commands=["lowprice", "highprice", "bestdeal"])
def price(message: types.Message) -> None:
    """
    This function sets functions route to find hotels

    If user entered lowprice: function sets sortOrder properties to 'PRICE' (from cheap to expensive)
    If user entered highprice: function sets sortOrder properties to 'PRICE_HIGHEST_FIRST' (from expensive to cheap)
    If user entered bestdeal: function sets sortOrder properties to 'DISTANCE_FROM_LANDMARK'

    And waits for a message from user with city name. Then it transmits control to Function get_name.

    :param message: Message instance with text '/lowprice'
    :return: None
    """

    to_data_base.append(f"{message.from_user.id}")
    to_data_base.append(f"{message.text}")
    to_data_base.append(f"{datetime.today().strftime('%d/%m/%Y %H:%M')}")

    # Each new call to this function response_properties updates its values
    response_properties["priceRange"] = float("inf")
    response_properties["distance"] = float("inf")

    # Search will be done by price (from cheap to expensive)
    if message.text == "/lowprice":
        response_properties["sortOrder"] = "PRICE"
    elif message.text == "/highprice":
        # Search will be done by price (from expensive to cheap)
        response_properties["sortOrder"] = "PRICE_HIGHEST_FIRST"
    else:
        # Search will be done by distance from landmark
        response_properties["sortOrder"] = "DISTANCE_FROM_LANDMARK"

    msg = bot.send_message(chat_id=message.chat.id, text="🌙 Enter number of days:", disable_notification=False)
    bot.register_next_step_handler(msg, get_days)
