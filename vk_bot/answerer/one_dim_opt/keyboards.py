from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboards:
    """
    Набор готовых клавиатур.
    """

    def __init__(self):
        self.keyboard = VkKeyboard(inline=True)

    def for_opt_alg_selection(self) -> VkKeyboard:
        """
        Выбор алгоритма для оптимизации.

        Returns
        -------
        VkKeyboard
            Объект созданной клавиатуры.
        """

        self.keyboard.add_button('Алгоритм "Парабола"', VkKeyboardColor.PRIMARY)
        self.keyboard.add_button('Алгоритм "Золотое сечение"', VkKeyboardColor.SECONDARY)
        # TODO: добавить кнопки для остальных алгоритмов
        return self.keyboard
