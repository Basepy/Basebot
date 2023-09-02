from telebot import types


def menu_01():
    teclado_01 = types.InlineKeyboardMarkup()
    bt_menu_01 = types.InlineKeyboardButton("BTC", callback_data='btn_btc')
    bt_menu_02 = types.InlineKeyboardButton("Taxa Rede", callback_data='btn_fees')
    bt_menu_03 = types.InlineKeyboardButton("Informações", callback_data='btn_info')
    bt_menu_04 = types.InlineKeyboardButton("Empréstimo", callback_data='btn_btccred')
    teclado_01.add(bt_menu_01, bt_menu_02, bt_menu_03, bt_menu_04)
    return teclado_01

