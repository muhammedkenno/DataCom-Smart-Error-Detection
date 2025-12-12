from flask import Flask, render_template, request
from utils import generate_parity, generate_crc, generate_hamming, check_parity, check_crc, check_hamming
import random

app = Flask(__name__)

# ---------------- ERROR INJECTION FUNCTIONS ----------------

def bit_flip(data):
    if len(data) == 0:
        return data
    bit_data = ''.join(format(ord(c), '08b') for c in data)
    pos = random.randint(0, len(bit_data)-1)
    flipped = list(bit_data)
    flipped[pos] = '0' if flipped[pos] == '1' else '1'
    return ''.join(chr(int(''.join(flipped[i:i+8]), 2)) for i in range(0, len(flipped), 8))

def char_substitution(data):
    if len(data) == 0:
        return data
    i = random.randint(0, len(data)-1)
    return data[:i] + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + data[i+1:]

def deletion(data):
    if len(data) == 0:
        return data
    i = random.randint(0, len(data)-1)
    return data[:i] + data[i+1:]

def insertion(data):
    i = random.randint(0, len(data))
    return data[:i] + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + data[i:]

def burst_error(data):
    if len(data) < 3:
        return data
    start = random.randint(0, len(data)-3)
    length = random.randint(2, 4)
    return data[:start] + ''.join(random.choice("XYZ") for _ in range(length)) + data[start+length:]


# ------------------- MAIN ROUTE -------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        data = request.form["data"]
        method = request.form["method"]
        error_type = request.form["error"]

        # ----- Generate Control Bits -----
        if method == "PARITY":
            control = generate_parity(data)
        elif method == "CRC":
            control = generate_crc(data)
        elif method == "HAMMING":
            control = generate_hamming(data)

        # ----- Apply selected error -----
        if error_type == "none":
            corrupted = data
        elif error_type == "bit_flip":
            corrupted = bit_flip(data)
        elif error_type == "substitution":
            corrupted = char_substitution(data)
        elif error_type == "deletion":
            corrupted = deletion(data)
        elif error_type == "insertion":
            corrupted = insertion(data)
        elif error_type == "burst":
            corrupted = burst_error(data)
        else:  # Random
            corrupted = random.choice([
                bit_flip, char_substitution, deletion, insertion, burst_error
            ])(data)

        # ----- Check / Correct -----
        if method == "PARITY":
            status = "CORRECT" if check_parity(corrupted, control) else "CORRUPTED"
            corrected = "-"

        elif method == "CRC":
            status = "CORRECT" if check_crc(corrupted, control) else "CORRUPTED"
            corrected = "-"

        elif method == "HAMMING":
            corrected = check_hamming(corrupted, control)
            status = "CORRECT" if corrected == data else "CORRUPTED"

        return render_template("index.html",
                               original=data,
                               corrupted=corrupted,
                               method=method,
                               control=control,
                               corrected=corrected,
                               status=status)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
