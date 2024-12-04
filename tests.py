from src import HuffmanEncoder


def testcase1():
    dict_to_encode = {
        'а': 0.18,
        'с': 0.132,
        'м': 0.12,
        'о': 0.168,
        'т': 0.09,
        'я': 0.01,
        'е': 0.032,
        'ь': 0.068,
        'н': 0.11,
        ' ': 0.09,
    }

    string = 'смотана мама мота'
    encoder = HuffmanEncoder(dict_to_encode)
    encoded_str = encoder.encode_message(string)
    decoded_str = encoder.decode_message(encoded_str)

    assert(encoded_str == '10110011011110001000111010000100001110100110111100')
    assert(decoded_str == string)


def testcase2():
    dict_to_encode = {
        'b': 0.3,
        'o': 0.15,
        't': 0.12,
        'w': 0.11,
        'r': 0.13,
        'k': 0.07,
        's': 0.1,
        ' ': 0.02,
    }

    string = 'bot works'
    encoder = HuffmanEncoder(dict_to_encode)
    encoded_str = encoder.encode_message(string)
    decoded_str = encoder.decode_message(encoded_str)

    assert(encoded_str == '1110101100000101011000001001')
    assert(decoded_str == string)


def testcase3():
    dict_to_encode = {
        'а': 0.12,
        'р': 0.1,
        'б': 0.08,
        'у': 0.2,
        'з': 0.06,
        ' ': 0.04,
        'в': 0.04,
        'к': 0.04,
        'с': 0.02,
        'н': 0.15,
        'й': 0.12,
        'ы': 0.03,
    }

    encoder = HuffmanEncoder('арбуз вкусный')

    encoded_str = encoder.encode_message('арбуз вкусный')
    decoded_str = encoder.decode_message(encoded_str)

    assert(encoded_str == '01011011100011111111101001100001110111010001000')
    assert(decoded_str == 'арбуз вкусный')


testcase1()
testcase2()
testcase3()
print('The tests were ran successfully')
