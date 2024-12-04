class HuffmanEncoder:
    """Ключевой класс для кодировки Хаффмана.
    При инициализации объекта необходимо передать либо dict[str, float] с символами и вероятностями их появления в
    тексте, либо str - строку с символами, которые надо закодировать.
    Объект класса HuffmanEncoder может кодировать сообщения согласно полученному при инициализации словарю, либо
    декодировать сообщение двоичного кода, исходя из предположения, что оно было получено согласно кодировке, которую
    определил экземпляр этого же класса (разные экземпляры могут по-разному решить кодировать один и тот же текст,
    потому что возможны ситуации неопределенности, когда узлы будут равновероятны, и выбор нуля или единицы для
    того или иного узла - арбитрарный выбор, который алгоритмом отдан случайности).
    """

    def __init__(self, input_data=None):
        """
        :param input_data: Принимает либо dict[str, float], либо str.
        Если передан словарь, в нем должны содержаться все необходимые символы как ключи и
        вероятности их появления в тексте как значения.
        Если передана строка, объект сам рассчитает вероятности появления всех символов и получит нужный словарь.
        """

        if type(input_data) == dict:
            self._input_dict = input_data
        elif type(input_data) == str:
            self._input_dict = self.count_dict(input_data)
        else:
            raise TypeError('input_data must be a dict or str')

        self.encoding_dict, self.decoding_dict = self.encode_dict()
        self.total_bytes = self.count_total_used_encoding_symbols()

    class EncodedSymbol:
        def __init__(self, symbol: str, probability: float):
            self.symbol = symbol
            self.probability = probability
            self.code = ''

        def __repr__(self):
            return f'EncodedSymbol obj with symbol "{self.symbol}" and probability of {self.probability}. ' \
                   f'Currently encoded by "{self.code}"'

    class Node:
        def __init__(self, symbols: list = None):
            if not symbols:
                self.symbols = []
            else:
                if type(symbols) != list:
                    raise TypeError('symbols arg must be a list')
                self.symbols = symbols

            # Автоматический расчет суммарной вероятности в узле, складывая вероятности каждого входящего символа
            total_prob = 0
            for symb in self.symbols:
                total_prob += symb.probability

            self.total_prob = total_prob

        def add_symbol(self, symbol_obj):
            """
            Принимает аргументом объект класса EncodedSymbol, добавляет его в список символов узла,
            а его вероятность появления добавляет в суммарную вероятность узла.
            :type symbol_obj: EncodedSymbol
            :rtype: None
            """

            self.symbols.append(symbol_obj)
            self.total_prob = self.total_prob + symbol_obj.probability

        def __repr__(self):
            return f'Node obj with symbols: {self.symbols} and total prob of {self.total_prob}'

    def get_input_dict(self):
        return self._input_dict

    def set_input_dict(self, value):
        self._input_dict = value

    def encode_dict(self):
        """
        Обрабатывает словарь, переданный при инициализации объекта HuffmanEncoder и кодирует
        его согласно алгоритму Хаффмана. Эта функция используется в функции инициализации объекта HuffmanEncoder,
        добавляя поле кодированного словаря.
        :return: Два словаря: с ключом-символом и значением-кодом и с ключом-кодом и значением-символом.
        Два словаря нужно для удобного кодирования и декодирования.
        :rtype: tuple[dict[str, str], dict[str, str]].
        """
        symbols_list = [self.EncodedSymbol(symbol=sym, probability=prob) for sym, prob in self.get_input_dict().items()]
        nodes_list = [self.Node() for i in range(len(symbols_list))]

        # Добавляем каждому начальному узлу соответствующий символ
        for i in range(len(nodes_list)):
            nodes_list[i].add_symbol(symbols_list[i])

        # Основной цикл кодировки
        while len(nodes_list) > 1:

            # Сортируем по убыванию вероятности узлов, чтобы доставать самые невероятные
            nodes_list.sort(key=lambda x: x.total_prob, reverse=True)

            # Достаем два самых невероятных узла, даем символам в одном из них ноль, в другом - 1
            last_node = nodes_list.pop(-1)
            for encoded_symbol in last_node.symbols:
                encoded_symbol.code = f'0{encoded_symbol.code}'

            second_last_node = nodes_list.pop(-1)
            for encoded_symbol in second_last_node.symbols:
                encoded_symbol.code = f'1{encoded_symbol.code}'

            # Создаем новый узел из убранных двух
            new_node = self.Node(symbols=last_node.symbols + second_last_node.symbols,)

            nodes_list.append(new_node)

        output_encoding_dict = {}
        output_decoding_dict = {}

        for symb in symbols_list:
            output_encoding_dict[symb.symbol] = symb.code
            output_decoding_dict[symb.code] = symb.symbol

        return output_encoding_dict, output_decoding_dict

    def encode_message(self, message: str):
        """
        Кодирует сообщение согласно полученному полю кодированного словаря.
        :param message: Сообщение для кодировки.
        :return: Закодированное сообщение.
        :rtype: str.
        """
        output_str = ''
        for char in message:
            try:
                output_str = output_str + self.encoding_dict[char]
            except KeyError:
                raise KeyError(f'Unknown symbol "{char}" in message "{message}"')
        return output_str

    def decode_message(self, message: str):
        """
        Декодирует сообщение согласно полученному полю кодированного словаря.
        :param message: Сообщение для декодировки.
        :return: Декодированное сообщение.
        :rtype: str.
        """
        output_str = ''
        current_char = ''

        for char in message:
            current_char += char
            if current_char in self.encoding_dict.values():
                output_str = output_str + self.decoding_dict[current_char]
                current_char = ''
            else:
                continue

        return output_str

    def count_total_used_encoding_symbols(self):
        """
        Считает, сколько символов потребуется для кодировки всех символов в словаре.
        :return: Количество необходимых символов.
        :rtype: int.
        """
        output = 0
        for v in self.encoding_dict.values():
            output += len(v)

        return output

    @staticmethod
    def count_dict(input_str: str) -> dict:
        """
        Получает строку на вход и возвращает dict[str, float] с символами и вероятностями их появления в строке.
        Словарь такого вида используется как "сырой" для дальнейшего кодирования.
        :param input_str: строка, символы которой надо закодировать.
        :return: dict[str, float] с символами и вероятностями их появления в строке.
        :rtype: dict[str, float].
        """

        output_dict = {}

        for char in input_str:
            chars_appearance = input_str.count(char)
            char_probability = round(chars_appearance / len(input_str), 2)

            output_dict[char] = char_probability

        return output_dict

    def __repr__(self):
        return f'Huffman encoder object with encoded dict: {self.encoding_dict}'

