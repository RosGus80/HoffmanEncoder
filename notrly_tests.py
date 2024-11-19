from src import HoffmanEncoder

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

str1 = 'смотана мама мота'
encoder = HoffmanEncoder(dict_to_encode)

encoded_str = encoder.encode_message(str1)
print(f'Not-a-test1')
print(encoded_str)
print(len(encoded_str))

decoded_str = encoder.decode_message(encoded_str)
print(decoded_str)

print(encoder.total_bytes)
print(encoder.encoded_dict)

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

str1 = 'bot works'
encoder1 = HoffmanEncoder(dict_to_encode)

encoded_str = encoder1.encode_message(str1)
print('Not-a-test2')
print(encoded_str)
print(len(encoded_str))

decoded_str = encoder1.decode_message(encoded_str)
print(decoded_str)

print(encoder1.total_bytes)
print(encoder1.encoded_dict)
