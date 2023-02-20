import random
# This is a program to encrypt and decrypt messages using the DES algorithm.

instructions = """Hi! This is a encryption/decryption DES program.
Select an option:
1.- Message Encryption
2.- Message Decryption"""

def plaintext_to_binary(plaintext_input):    
# This function converts the string to ascii value and then to binary.

# Here i can implement this code to avoid using the padding variable?
#'{0:08b}'.format(6)
#'00000110'

    binary_message = ""
    for character in plaintext_input:
        binary_value = bin(ord(character))
        padding = 10 - len(binary_value)
        binary_value = "0"*padding + binary_value[2:]
        binary_message += binary_value
    return binary_message


def binary_to_plaintext(binary_input):
# This function converts a binary to ascii and then to a string.

    plaintext_message = ""
    x=1
    for binary_group in range(int(len(binary_input)/8)):
        character_value = binary_input[x:x+7]
        character_value = chr(int(character_value,2))
        plaintext_message += character_value
        x += 8
    return plaintext_message


def dict_block64_generator(message):
# This function chops the message in 64-bit blocks.
# If the len(message) do not complete a 64-bit block we add blank spaces.

    if len(message) % 8 != 0:
        padding = 8 - (len(message) % 8)
        message += " "*padding

    x=0
    for block in range(int(len(message)/8)):
        block_name = "Block" + str(block)
        block_value = message[x:x+8]
        block_64_bits[block_name] = block_value
        x+=8


def permutation(matrix, block):
    modified_block = ""
    for bit in matrix:
# It's necesary to less 1 because the values on the matrixes start from 1 and python index starts from 0.
        modified_block += block[bit-1] 
    return modified_block


def key_generator():
# iF THE USER HAS ALREADY A KEY HE CAN USE IT. iF NOT IT'S GOING TO BE RANDOMLY GENERATED

    print("""\nIf you have and want to use a specific 64-bit key select y.\nOtherwise the program is going to create a random key for you.""")
    key_existance = str(input("Do you have an existing key? (y/n) "))

    if key_existance == "y":
        key = str(input("Write your key: "))
    else:
        key = ""
        for bit in range(64):
            bit_value = random.randrange(2)
            key += str(bit_value)
    return key


def left_shift_join(cn, dn, step=2):
    cn_1 = cn[step:] + cn[:step]
    dn_1 = cn[step:] + dn[:step]
    cn_dn_1 = cn_1 + dn_1
    return cn_dn_1


def xor_operation(value1, value2):
    for bit in range(len(value1)):
        a = bool(int(value1[bit]))
        b = bool(int(value2[bit]))
        xor_result = ""
        if a^b == True:
            xor_result += "1"
        
        else:
            xor_result += "0"
    return xor_result


def subkeys_generation(key_56_bit):
    c0 = key_56_bit[:28]
    d0 = key_56_bit[28:]
    for shift in range(16):
        if shift in (0, 1, 8, 15):
            cn_dn = left_shift_join(c0, d0)
        else:
            cn_dn = left_shift_join(c0, d0, 2)
        
        key_name = "k" + str(shift+1)
        key_value = permutation(pc_2_matrix, cn_dn)
        subkeys[key_name] = key_value
    

def feistel(rn, kn):
    expansion = permutation(expansion_P_box, rn)
    input_sboxes = xor_operation(expansion, kn)
    s_box_dict = {}
    
    # Here I'm creating a dict that stores the expansion output divided in 8 groups of 6 bits.
    for bit in range(8):
        s_box_key = "B" + str(bit)
        s_box_value = input_sboxes[bit:bit+6]
        s_box_dict[s_box_key] = s_box_value
        bit += 6

    #  This part reduces the group of 6 bits to 4 by the use of the S-Boxes.
    x = 0
    x_boxes_output = ""
    for key, value in s_box_dict.items():
        x_coordinate_value = int(value[0] + value[5], 2)
        y_coordinate_value = int(value[1:5], 2)
        position = x_coordinate_value + 16*y_coordinate_value

        # Me falta cambiar la salida que es int a binario.
        # Ya sólo revisa que esté correcto.
        x_box_output = (s_boxes[x])[position]

        x_boxes_output += bin(x_box_output)[2:]

        x +=1

# Eliminar el print
    print(len(x_boxes_output))
    feistel_output = permutation(straight_P_box, x_boxes_output)

    return feistel_output
    

def cipher_rounds(li, ri):
# This function makes 2 operations per cicle: a) ln = rn-1  b) ln-1 XOR feistel(rn-1, k1)

    for subkey, value in subkeys.items():
        ln = ri
        feistel_output = feistel(ri, value)

        rn = xor_operation(li, feistel_output)

        # After completing a round it's necesary to reasign li and ri so the next round works with the new values.
        # The 'n' subindex is equivalent to the kn subkey subindex. So when we reach the last lap of the loop the index would be 16. 
        li = ln
        ri = rn
    l16_r16 = li + ri

    return l16_r16


def inverse_permutation(matrix, block):
# This will work for moments when theres no repetition ? Can we change that?

    pass


def run():
    print(instructions)

    try:
        option = int(input("Select a number: "))
        if option == 1:
            cypher_text = ""

            # key_64_bit = key_generator()
            key_64_bit = "0010110111111111011010111010000000010100101101010101001011000000"
            
            #Now the 64-bit key has to transform with the Permuted Choice-1
            key_56_bit = ""
            for i in range(1, len(key_64_bit)+1):
                if i % 8 == 0:
                    continue
                key_56_bit += key_64_bit[i-1] 
            
            # Now the 56-bit key divides into C0 and D0
            c0 = key_56_bit[:28]
            d0 = key_56_bit[28:]

            # Now it's time to generate a dictionary that contains all the 16 subkeys.
            subkeys_generation(key_56_bit)

            # Now we can start the rounds 
            message_decrypted = str(input("Write your plaitext message: "))

            # Now we create a dict with the following structur: Blocki as key : 64-bit block as value.
            dict_block64_generator(message_decrypted)

            for key, value in block_64_bits.items(): # It's going to encrypt each 64-bit block.

                # The first step is to make the Initial Permutation:
                ip = permutation(ip_matrix, plaintext_to_binary(value))

                # The next step is to divide the 64-bit block in 2 32-bit blocks (L0 and R0)
                l0 = ip[:32]
                r0 = ip[32:]

                # After this it's time to start the 16 rounds. This is the first one.
                l16_r16 = cipher_rounds(l0, r0)

                # The next step is to swap the first 32 bits to be the last 32 bits of the block.
                r16_l16 = l16_r16[:32] + l16_r16[32:]

                # To complete the cipher block bit arrange we have to do an inverse permutation with the IP_matrix.
                cypher_binary_block = inverse_permutation(ip_matrix, r16_l16)

                # Finally the only thing left is to convert the 64-bit cypher block to ascii characters.
                cypher_block = binary_to_plaintext(cypher_binary_block)

                cypher_text += cypher_block

            print(cypher_text)

    
        elif option == 2:
            message_encrypted = str(input("Write your encrypted message: "))
            print(binary_to_plaintext(message_encrypted))

        else:
            print("That's not a valid option.\nTry again!")

    except ValueError:
        print("That's not a valid option.\nTry again!")


        


subkeys = {}

ip_matrix = [58, 50, 42, 34, 26, 18, 10, 2,
             60, 52, 44, 36, 28, 20, 12, 4,
             62, 54, 46, 38, 30, 22, 14, 6,
             64, 56, 48, 40, 32, 24, 16, 8,
             57, 49, 41, 33, 25, 17, 9, 1,
             59, 51, 43, 35, 27, 19, 11, 3,
             61, 53, 45, 37, 29, 21, 13, 5,
             63, 55, 47, 39, 31, 23, 15, 7]

pc_2_matrix = [14, 17, 11, 24, 1, 5,
               3, 28, 15, 6, 21, 10,
               23, 19, 12, 4, 26, 8,
               16, 7, 27, 20, 13, 2,
               41, 52, 31, 37, 47, 55,
               30, 40, 51, 45, 33, 48,
               44, 49, 39, 56, 34, 53,
               46, 42, 50, 36, 29, 32]

expansion_P_box = [32, 1, 2, 3, 4, 5, 
                   4, 5, 6, 7, 8, 9,
                   8, 9, 10, 11, 12, 13,
                   12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21,
                   20, 21, 22, 23, 24, 25,
                   24, 25, 26, 27, 28, 29,
                   28, 29, 30, 31, 32, 1]

s_box_1 = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
           0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
           4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
           15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]

s_box_2 = [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
           3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
           0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
           13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]

s_box_3 = [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
           13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
           13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
           1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]

s_box_4 = [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
           13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
           10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
           3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]

s_box_5 = [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
           14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
           4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
           11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]

s_box_6 = [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
           10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
           9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
           4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]

s_box_7 = [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
           13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
           1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
           6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]

s_box_8 = [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
           1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
           7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
           2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]

s_boxes = [s_box_1, s_box_2, s_box_3, s_box_4,
           s_box_5, s_box_6, s_box_7, s_box_8]

straight_P_box = [16, 7, 20, 21,
                  29, 12, 28, 17,
                  1, 15, 23, 26,
                  5, 18, 31, 10,
                  2, 8, 24, 14,
                  32, 27, 3, 9,
                  19, 13, 30, 6,
                  22, 11, 4, 25]

block_64_bits = {}

if __name__ == "__main__":
    run()