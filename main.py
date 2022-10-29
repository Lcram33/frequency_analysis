import sys
import unidecode

file_path = sys.argv[1]
data = ""

charset = "abcdefghijklmnopqrstuvwxyz"
coincidence_rates = {
    'french': 0.0778,
    'german': 0.0762,
    'italian': 0.0738,
    'english': 0.0667,
    'random': 0.0385
}

with open(file_path, 'r') as f:
    data = unidecode.unidecode(f.read()).lower()

chars_list = list(set(list(data)))

chars_data = {}
total_chars = 0
for char in chars_list:
    if char in charset:
        char_count = len([x for x in data if x == char])
        total_chars += char_count
        chars_data[char] = char_count

chars_data_sorted = sorted(chars_data.items(), key=lambda x:x[1])
chars_data = dict(chars_data_sorted)

print(chars_data)


n = len([x for x in data if x in charset])
coincidence_rate = sum((x*(x-1))/(n*(n-1)) for x in chars_data.values())


delta = 0.02
print(f"Coincidence rate : {coincidence_rate}")
for lang,rate in coincidence_rates.items():
    if (1 - delta) * rate < coincidence_rate < (1 + delta) * rate:
        print("Probable lang : " + lang)