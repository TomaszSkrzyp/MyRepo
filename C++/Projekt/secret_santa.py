import random
import django


lista = ["Michal", "Lukasz", "Pawel", "Mateusz", "Tomek", "Bruno"]
receiver = random.choice(lista)

def zakoduj(imie):
    klucz = random.randint(1, 1000)
    zakodowany = ""
    for char in imie:
        encoded_char = chr(ord(char) + klucz)
        zakodowany += encoded_char
    return zakodowany, klucz

def zdekoduj(zakodowany, klucz):
    zdekodowany = ""
    for char in zakodowany:
        decoded_char = chr(ord(char) - klucz)
        zdekodowany += decoded_char
    return zdekodowany

zakodowany,klucz=zakoduj(receiver)
print(django.get_version())
print(receiver)
print(zakodowany,klucz)
print(zdekoduj(zakodowany,klucz))

p