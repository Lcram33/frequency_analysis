import sys
import unidecode
import json
import os
import hashlib


USE_CACHE = True
FILE_SIZE_THRESHOLD = 5000000 #5 MB

charset = "abcdefghijklmnopqrstuvwxyz"
index_coincidences = {
    "German": 0.072,
    "English":  0.065,
    "Spanish": 0.074,
    "Esperanto": 0.069,
    "French": 0.078,    #calculated using calculate_rates.py
    "Italian": 0.075,
    "Norwegian": 0.073,
    "Swedish": 0.071
}


def convert_size(size_in_bytes):
    units = ['TB', 'GB', 'MB', 'KB']
    size_range = list(range(1,len(units)+1))[::-1]

    for i in size_range:
        converted = size_in_bytes // (10**(3*i))
        if converted > 0:
            return str(round(size_in_bytes / (10**(3*i)), 1)) + ' ' + units[::-1][i-1]

    return str(size_in_bytes) + ' B'

def md5(path):
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()

def load_cache():
    if os.path.exists("cache.json"):
        with open("cache.json", 'r') as f:
            return json.load(f)
    else:
        return {}

def save_cache(cache):
    with open("cache.json", 'w+') as f:
        json.dump(cache, f)

def count_chars(data, only_letters):
    chars_data = {}
    for char in data:
        if char in charset or not only_letters:
            if char in chars_data:
                chars_data[char] += 1
            else:
                chars_data[char] = 1

    chars_data_sorted = sorted(chars_data.items(), key=lambda x:x[1])
    chars_data = dict(chars_data_sorted)

    return chars_data

def calculate_frequencies(n, chars_data):
    return {k:round(100*v/n,2) for k,v in chars_data.items()}

def calculate_index_coincidence(n, chars_data):
    index_coincidence = sum((x*(x-1))/(n*(n-1)) for x in chars_data.values())

    return index_coincidence

def guess_language(index_coincidence, delta):
    for lang,rate in index_coincidences.items():
        if abs(index_coincidence - rate) < delta:
            print("Probable lang : " + lang)

def calculate_all(file_path, only_letters):
    with open(file_path, 'r') as f:
        data = "".join(x for x in unidecode.unidecode(f.read()).lower() if x in charset) if only_letters else f.read()

    n = len(data)
    chars_data = count_chars(data, only_letters)
    index_coincidence = calculate_index_coincidence(n, chars_data)
    frequencies = calculate_frequencies(n, chars_data)

    return n, chars_data, frequencies, index_coincidence


def main():
    args = sys.argv[1:]

    if len(args) not in [1, 2]:
        print("Please provide a path, and optionnaly 1 if only letters should be included.")
        return
    
    print("""▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█ ▄▄█ ▄▄▀█ ▄▄█ ▄▄ █ ██ █ ▄▄█ ▄▄▀█▀▄▀█ ██ ███ ▄▄▀█ ▄▄▀█ ▄▄▀█ ██ ██ █ ▄▄██▄██ ▄▄
█ ▄██ ▀▀▄█ ▄▄█ ▀▀ █ ██ █ ▄▄█ ██ █ █▀█ ▀▀ ███ ▀▀ █ ██ █ ▀▀ █ ██ ▀▀ █▄▄▀██ ▄█▄▄▀
█▄███▄█▄▄█▄▄▄████ ██▄▄▄█▄▄▄█▄██▄██▄██▀▀▀▄███▄██▄█▄██▄█▄██▄█▄▄█▀▀▀▄█▄▄▄█▄▄▄█▄▄▄
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    """)

    file_path = args[0]
    only_letters = True if (len(args) == 2 and args[1] == '1') else False

    if only_letters:
        print("Counting only letters [A-Za-z]")
    else:
        print("Counting all chars")

    file_size = os.path.getsize(file_path)
    if USE_CACHE and file_size > FILE_SIZE_THRESHOLD:
        print(f"File size : {convert_size(file_size)} > {convert_size(FILE_SIZE_THRESHOLD)}. Using cache.")

        cache = load_cache()
        md5sum = md5(file_path)
        md5sum += "_only_letters" if only_letters else "_full"
        if md5sum in cache:
            print("Cache found !")
            print()

            n = cache[md5sum]["n"]
            chars_data = cache[md5sum]["data"]
            frequencies = calculate_frequencies(n, chars_data)
            index_coincidence = calculate_index_coincidence(n, chars_data)
        else:
            print("No cache, calculating and saving.")

            n, chars_data, frequencies, index_coincidence = calculate_all(file_path, only_letters)

            cache[md5sum] = {}
            cache[md5sum]["n"] = n
            cache[md5sum]["data"] = chars_data
            save_cache(cache)
    else:
        n, chars_data, frequencies, index_coincidence = calculate_all(file_path, only_letters)

    print(f"I counted {n} chars :")
    print(chars_data)
    print()
    print("Frequencies (%) :")
    print(frequencies)
    print()
    print(f"Index of coincidence (probability of two randomly selected letters being equal) :\n{index_coincidence}")
    
    delta = 0.002
    guess_language(index_coincidence, delta)

if __name__ == "__main__":
    main()