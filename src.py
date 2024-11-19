class HuffmanEncoder:

    def __init__(self, input_dict: dict):
        self.input_dict = input_dict
        self.encoded_dict, self.encoded_object_list = self.encode_dict()
        self.total_bytes = self.count_total_used_encoding_symbols()

    class EncodedSymbol:
        def __init__(self, symbol: str, probability: float):
            self.symbol = symbol
            self.probability = probability
            self.code = ''

        def __str__(self):
            return f'EncodedSymbol obj with symbol: {self.symbol} and probability of {self.probability}. ' \
                   f'Currently encoded by {self.code}'

        def __repr__(self):
            return f'EncodedSymbol obj with symbol "{self.symbol}" and probability of {self.probability}. ' \
                   f'Currently encoded by "{self.code}"'

    class Node:
        def __init__(self, symbols=None, total_prob=0):
            if not symbols:
                self.symbols = []
            else:
                self.symbols = symbols

            self.total_prob = total_prob

        def add_symbol(self, symbol_obj):
            """Takes an EncodedSymbol instance and adds it to self.symbols. Also increasing self.total_prob"""
            # Prolly quite useless but convenient

            self.symbols.append(symbol_obj)
            self.total_prob = self.total_prob + symbol_obj.probability

        def __str__(self):
            return f'Node obj with symbols: {self.symbols} and total prob of {self.total_prob}'

        def __repr__(self):
            return f'Node obj with symbols: {self.symbols} and total prob of {self.total_prob}'

    def encode_dict(self):
        symbols_list = [self.EncodedSymbol(symbol=sym, probability=prob) for sym, prob in self.input_dict.items()]
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

            new_node = self.Node(symbols=last_node.symbols + second_last_node.symbols,
                                 total_prob=last_node.total_prob + second_last_node.total_prob)

            nodes_list.append(new_node)

        output_dict = {}
        output_objects_list = []

        for symb in sorted(symbols_list, key=lambda x: x.probability, reverse=True):
            output_objects_list.append(symb)
            output_dict[symb.symbol] = symb.code

        return output_dict, output_objects_list

    def encode_message(self, message: str):
        output_str = ''
        for char in message:
            try:
                output_str = output_str + self.encoded_dict[char]
            except KeyError:
                raise KeyError(f'Unknown symbol "{char}" in message "{message}"')
        return output_str

    def decode_message(self, message: str):
        output_str = ''
        current_char = ''
        for char in message:
            current_char += char
            if current_char in self.encoded_dict.values():
                output_str = output_str + list(self.encoded_dict.keys())[list(self.encoded_dict.values()).index(current_char)]
                current_char = ''
            else:
                continue

        return output_str

    def count_total_used_encoding_symbols(self):
        output = 0
        for v in self.encoded_dict.values():
            output += len(v)

        return output

    def __str__(self):
        return f'Huffman encoder object with encoded dict: {self.encoded_dict}'

    def __repr__(self):
        return f'Huffman encoder object with encoded dict: {self.encoded_dict}'

