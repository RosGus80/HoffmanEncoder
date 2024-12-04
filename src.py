class HuffmanEncoder:

    def __init__(self, input_dict: dict[str, float]):
        self._input_dict = input_dict
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

    # TODO: сделать ф-цию, принимающую строку и возвращающую словарь с символами и вероятностями их появления
    @staticmethod
    def count_dict(input_str: str) -> tuple[dict[str, float], dict[float, str]]:
        pass

    def __repr__(self):
        return f'Huffman encoder object with encoded dict: {self.encoding_dict}'

