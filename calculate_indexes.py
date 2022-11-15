from main import calculate_all
from os import listdir
from os.path import join


print("""
 _____       _            _       _   _                               
/  __ \     | |          | |     | | (_)            
| /  \/ __ _| | ___ _   _| | __ _| |_ _ _ __   __ _ 
| |    / _` | |/ __| | | | |/ _` | __| | '_ \ / _` |      
| \__/\ (_| | | (__| |_| | | (_| | |_| | | | | (_| | 
 \____/\__,_|_|\___|\__,_|_|\__,_|\__|_|_| |_|\__, |
                                               __/ |                               
                                              |___/                                

Depending on the quantity of data, consider having a coffee
                            ( (
                            ) )
                        ........
                        |      |]
                        \      /
                         `----'
   """)


languages = listdir("samples")
for lang in languages:
    rate = 0
    samples = listdir(join("samples", lang))
    for sample in samples:
        _, _, _, s_rate = calculate_all(join(join("samples", lang), sample), True)
        rate += s_rate
    
    rate /= len(samples)

    print(f"* {lang} :    {rate} -> {round(rate, 3)} (rounded)")