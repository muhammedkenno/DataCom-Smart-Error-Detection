def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

# -------- PARITY --------

def even_parity(bit_string):
    count = bit_string.count("1")
    return "0" if count % 2 == 0 else "1"

def generate_parity(data):
    bits = text_to_bits(data)
    return even_parity(bits)

def check_parity(data, received_parity):
    bits = text_to_bits(data)
    new_parity = even_parity(bits)
    return new_parity == received_parity


# -------- CRC --------

def xor(a, b):
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))

def crc_remainder(data_bits, polynomial):
    poly_len = len(polynomial)
    temp = data_bits[:poly_len]

    for i in range(poly_len, len(data_bits)):
        if temp[0] == '1':
            temp = xor(temp, polynomial)
        temp = temp[1:] + data_bits[i]

    if temp[0] == '1':
        temp = xor(temp, polynomial)

    return temp[1:]

def generate_crc(data):
    polynomial = "1101"
    data_bits = text_to_bits(data) + "0" * (len(polynomial) - 1)
    return crc_remainder(data_bits, polynomial)

def check_crc(data, received_crc):
    polynomial = "1101"
    data_bits = text_to_bits(data) + "0" * (len(polynomial) - 1)
    computed = crc_remainder(data_bits, polynomial)
    return computed == received_crc

# -------- Hamming (7,4) --------

def hamming_encode_4bits(data):
    # data is 4 bits string
    d1, d2, d3, d4 = map(int, data)

    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4

    # ترتيب: p1 p2 d1 p3 d2 d3 d4
    return f"{p1}{p2}{d1}{p3}{d2}{d3}{d4}"


def hamming_decode_7bits(code):
    b = list(map(int, code))

    p1 = b[0] ^ b[2] ^ b[4] ^ b[6]
    p2 = b[1] ^ b[2] ^ b[5] ^ b[6]
    p3 = b[3] ^ b[4] ^ b[5] ^ b[6]

    error_pos = p1 * 1 + p2 * 2 + p3 * 4

    if error_pos != 0:
        b[error_pos - 1] ^= 1   # تصحيح الخطأ

    # استخراج data bits
    return f"{b[2]}{b[4]}{b[5]}{b[6]}"


def generate_hamming(data):
    bits = text_to_bits(data)
    chunks = [bits[i:i+4] for i in range(0, len(bits), 4)]
    encoded = ""

    for chunk in chunks:
        if len(chunk) < 4:
            chunk = chunk.ljust(4, '0')
        encoded += hamming_encode_4bits(chunk)

    return encoded


def decode_hamming_full(encoded):
    corrected_bits = ""
    original_bits = ""

    chunks = [encoded[i:i+7] for i in range(0, len(encoded), 7)]

    for chunk in chunks:
        if len(chunk) < 7:
            continue

        b = list(map(int, chunk))

        p1 = b[0] ^ b[2] ^ b[4] ^ b[6]
        p2 = b[1] ^ b[2] ^ b[5] ^ b[6]
        p3 = b[3] ^ b[4] ^ b[5] ^ b[6]

        error_pos = p1 * 1 + p2 * 2 + p3 * 4

        if error_pos != 0:
            b[error_pos - 1] ^= 1   # تصحيح الخطأ

        corrected_bits += ''.join(map(str, b))
        original_bits += f"{b[2]}{b[4]}{b[5]}{b[6]}"

    return original_bits, corrected_bits


def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)


def check_hamming(data, received_code):
    decoded_bits, _ = decode_hamming_full(received_code)
    recovered_text = bits_to_text(decoded_bits)
    return recovered_text.strip('\x00')
