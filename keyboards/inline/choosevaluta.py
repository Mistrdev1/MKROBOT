from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




clearWallets = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = "♨️Tozalash", callback_data = "clear_wallets")   
        ]
    ]
)


class ChooseValuta:
    def __init__(self, l_valuta1="🔼 UZCARD", l_valuta2="🔼 HUMO", l_valuta3="🔼 USDT",
                 r_valuta1="▫️", r_valuta2="▫️", r_valuta3="▫️",
                 callback1="none", callback2="none", callback3="none"):
        self.l_valuta1 = l_valuta1
        self.l_valuta2 = l_valuta2
        self.l_valuta3 = l_valuta3

        self.r_valuta1 = r_valuta1
        self.r_valuta2 = r_valuta2
        self.r_valuta3 = r_valuta3

        self.callback1 = callback1
        self.callback2 = callback2
        self.callback3 = callback3

    def makeValuta(self):
        chooseValuta = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=self.l_valuta1, callback_data='from_uzcard'),
                    InlineKeyboardButton(
                        text=self.r_valuta1, callback_data=self.callback1)
                ],
                [
                    InlineKeyboardButton(
                        text=self.l_valuta2, callback_data='from_humo'),
                    InlineKeyboardButton(
                        text=self.r_valuta2, callback_data=self.callback2)
                ],
                [
                    InlineKeyboardButton(
                        text=self.l_valuta3, callback_data='from_usdt'),
                    InlineKeyboardButton(
                        text=self.r_valuta3, callback_data=self.callback3)
                ],
            ])

        return chooseValuta


choose_menu = ChooseValuta()
chooseValuta = choose_menu.makeValuta()

choose_uzcard = ChooseValuta(l_valuta1='✅UZCARD', r_valuta1='🔽 USDT', r_valuta2="▫️",r_valuta3="▫️",
                                                    callback1="to_usdt", callback2="none", callback3='none')

chooseUzcard = choose_uzcard.makeValuta()

choose_humo = ChooseValuta(l_valuta2='✅HUMO', r_valuta1='🔽 USDT', r_valuta2="▫️",r_valuta3="▫️",
                                                callback1="to_usdt", callback2="none", callback3='none',
                           )
chooseHumo = choose_humo.makeValuta()

choose_usdt = ChooseValuta(
    l_valuta3='✅ USDT', r_valuta1='🔽UZCARD', r_valuta2="🔽HUMO",
    r_valuta3="▫️",
    callback1="to_uzcard", callback2="to_humo", callback3='none',
)
chooseUSDT = choose_usdt.makeValuta()








