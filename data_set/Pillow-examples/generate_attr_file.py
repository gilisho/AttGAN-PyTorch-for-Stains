IMAGES_NUMBER = 1000

string = f'{IMAGES_NUMBER}\nClean Stain_Level_1 Stain_Level_2 Stain_Level_3'
for i in range(0, IMAGES_NUMBER, 4):
    string += f'\n{i:06}.jpg 1 -1 -1 -1'
    string += f'\n{i+1:06}.jpg -1 1 -1 -1'
    string += f'\n{i+2:06}.jpg -1 -1 1 -1'
    string += f'\n{i+3:06}.jpg -1 -1 -1 1'

print(string)