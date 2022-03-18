from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboards:
    """
    Набор готовых клавиатур.
    """
    def __init__(self):
        self.keyboard = VkKeyboard(inline=True)
