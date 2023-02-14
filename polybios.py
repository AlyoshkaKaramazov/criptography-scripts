import time

# First I create a dictionary that´s gonna resemble a polybios chart.
# The only probles is that we´re gonna have a repeted value both for the letter i and j so for n and ñ.
polybios_dict = {
    "a" : "AA",
    "b" : "AB",
    "c" : "AC",
    "d" : "AD",
    "e" : "AE",

    "f" : "BA",
    "g" : "BB",
    "h" : "BC",
    "i" : "BD",
    "j" : "BD",
    "k" : "BE",

    "l" : "CA",
    "m" : "CB",
    "n" : "CC",
    "ñ" : "CC",
    "o" : "CD",
    "p" : "CE",

    "q" : "DA",
    "r" : "DB",
    "s" : "DC",
    "t" : "DD",
    "u" : "DE",

    "v" : "EA",
    "w" : "EB",
    "x" : "EC",
    "y" : "ED",
    "z" : "EE",
}

# This function needs a string argument and will return the message encrypted.
def encrypt(message_decrypted):
    encrypted_message = ""
    for character in message_decrypted:
        if character.lower() in polybios_dict.keys():
            encrypted_message += polybios_dict[character.lower()]
        else:
            encrypted_message += character
    return encrypted_message


# This function is going to decrypt the message encrypted by the encrypt function. 
# It also works with any encrypted message that use thepolybios chart with letters as coordinates.
# In case the letter to decrypt is j it will apper as an i, the same for the ñ would be a n.
def decrypt(message_encrypted):
    decrypted_message = ""
    encrypted_letter = ""
    for character in message_encrypted:
        if character.isalpha() == True:
            encrypted_letter += character.upper()
        else:
            decrypted_message += character
        
        if len(encrypted_letter) == 2:
            decrypted_letter = list(filter(lambda x: polybios_dict[x] == encrypted_letter, polybios_dict))[0]
            decrypted_message += decrypted_letter
            encrypted_letter = ""

    return decrypted_message


def run():
    message = input("Write the message you want to encrypt: ")

    print("Your encrypted message is: ")
    print(encrypt(message))

    time.sleep(1)

    print("Your decrypted message is: ")
    print(decrypt(encrypt(message)))

    if encrypt(message) == encrypt(decrypt(encrypt(message))):
        print("The code works!")



if __name__ == "__main__":
    run()