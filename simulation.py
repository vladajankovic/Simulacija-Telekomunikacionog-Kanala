from math import *
from random import *
import matplotlib.pyplot as plt


#######################################################################################

def lzw_code(characters1, dictionary1):
    w = ""
    output = []
    for index0 in range(0, len(characters1), 1):
        k = characters1[index0]
        wk = w + k
        ind2 = False

        tmp = dictionary1.values()  # Proveri da li je WK u recniku
        if wk in tmp:
            ind2 = True

        if ind2:
            w = wk
        else:
            for index1 in range(0, len(dictionary1), 1):  # Ako ne postoji u recniku ispisi W i dodaj WK u recnik
                if w == dictionary1[index1]:
                    output.append(index1)
                    break
            dictionary1[len(dictionary1)] = wk
            w = k

    for index0 in range(0, len(dictionary1), 1):
        if w == dictionary1[index0]:
            output.append(index0)
            break
    return output


def binary_repetition_code(n, array):
    output = []
    for nums in array:
        for bit in nums:
            for a in range(0, n, 1):
                output.append(bit)
    return output


def channel(p, signal):
    for bit in range(0, len(signal), 1):
        r = random()
        if r < p:
            signal[bit] = '1' if signal[bit] == '0' else '0'
    return signal


def lzw_decode(numbers, dictionary2):
    output = []
    old = numbers[0]
    ################################################
    tmp = dictionary2.keys()
    if old not in tmp:
        # print("NUMBER NOT IN DICTIONARY! CRITICAL ERROR!")
        t = [-1]
        return t
    s = dictionary2[old]
    output.append(dictionary2[old])  # ŠTA AKO JE SE PRVO SLOVO NE NALAZI U REČNIKU !!!!!!
    c = s[0]
    ##################################################
    for index3 in range(1, len(numbers), 1):
        new = numbers[index3]
        tmp = dictionary2.keys()
        if new in tmp:
            s = dictionary2[new]
        else:
            ################################################################################
            if old not in tmp:
                # print("NUMBER NOT IN DICTIONARY! CRITICAL ERROR!")
                t = [-1]
                return t
            ################################################################################
            s = dictionary2[old]
            s = s + c
        output.append(s)
        c = s[0]
        ################################################################################
        if old not in tmp:
            # print("NUMBER NOT IN DICTIONARY! CRITICAL ERROR!")
            t = [-1]
            return t
        dictionary2[len(dictionary2)] = dictionary2[old] + c
        ###################################################################################
        old = new

    tmp1 = []
    for word in output:
        for index2 in range(0, len(word), 1):
            tmp1.append(word[index2])
    return tmp1


def majority_decision(n, array, bitgroup):
    output = []
    ones = 0
    count = 0
    for bit in array:
        if bit == '1':
            ones += 1
        count += 1
        if count == n:
            out = '1' if ones > n / 2 else '0'
            output.append(out)
            ones = 0
            count = 0
    g = 0
    st = ""
    tmp = []
    for out in output:
        st = st + out
        g += 1
        if g == bitgroup:
            tmp.append(st)
            st = ""
            g = 0
    return tmp


def check_for_errors(array1, array2):
    min1 = len(array2) if len(array1) >= len(array2) else len(array1)
    cnt = len(array1) - len(array2) if len(array1) - len(array2) > 0 else 0
    for index2 in range(0, min1, 1):
        if array1[index2] != array2[index2]:
            cnt += 1
    return cnt / len(array1)


##########################################################################################

text = open("test.txt", 'r')
text = text.read()
print("\nSent message:")
print(text, end='\n\n')

characters = []  # Izdvojeni karakteri iz teksta
dictionary = {}  # recnik za LZW
init_dictionary = {}
seed()

for ch in range(0, len(text), 1):  # pravljenje recnika i izdvajanje simbola iz unosa
    if text[ch] == '\n':
        continue
    characters.append(text[ch])
    if len(dictionary) == 0:
        dictionary[len(dictionary)] = text[ch]
    else:
        ind1 = 0
        for index in range(0, len(dictionary), 1):
            if text[ch] == dictionary[index]:
                break
            ind1 = ind1 + 1
        if ind1 == len(dictionary):
            dictionary[len(dictionary)] = text[ch]

init_dictionary = dictionary.copy()  # Save the initial Dictionary

lzw_out = lzw_code(characters, dictionary)  # izlazna sekvenca LZW algoritma
print("Sequence after LZW: ")
print(lzw_out, end='\n\n')

maxnumber = max(lzw_out)  # Broj bita za kodovanje odgovara broju bita porebnih za kodovanje najveceg broja
bits_to_format = log2(maxnumber) + 1 \
    if log2(maxnumber) - floor(log2(maxnumber)) == 0 \
    else ceil(log2(maxnumber))
bits = "0" + str(bits_to_format) + "b"  # Formatiranje numericke sekvence u binarnu
for index in range(0, len(lzw_out), 1):
    lzw_out[index] = format(lzw_out[index], bits)
print("Binary representation: ")
print(lzw_out, end='\n\n')

channel_in_3_1 = binary_repetition_code(3, lzw_out)  # Izlaz iz zastitnog kodera sam ponavljanjem (3,1)
print("Channel input sequence (3,1) coding: ")
print(channel_in_3_1, end='\n\n')

channel_in_5_1 = binary_repetition_code(5, lzw_out)  # Izlaz iz zastitnog kodera sam ponavljanjem (5,1)
print("Channel input sequence (5,1) coding: ")
print(channel_in_5_1, end='\n\n')

channel_error = []
for it in range(1, 80, 7):
    channel_error.append(it / 1000)
pe_3_1 = []
pe_5_1 = []

repeat = 10

for index in range(0, len(channel_error), 1):
    print("###################################################", end='\n\n')
    print("        Simulation ", end='')
    print(index + 1, end='\n\n')
    print("Channel error: ", end='')
    print(channel_error[index])
    avg_3_1 = 0
    avg_5_1 = 0

    for o1 in range(0, repeat, 1):
        while True:
            channel_out_3_1 = channel(channel_error[index], channel_in_3_1.copy())  # Simulacija Kanala
            # print("Channel output sequence: ", end='')
            # print(channel_out, end='\n')

            channel_out_3_1 = majority_decision(3, channel_out_3_1, bits_to_format)  # Vecinsko odlucivanje
            # print("Majority decision: ", end='')
            # print(channel_out, end='\n')

            for index1 in range(0, len(channel_out_3_1), 1):  # Formatiranje u cele brojeve
                channel_out_3_1[index1] = int(channel_out_3_1[index1], 2)
            # print("LZW decompression input: ", end='')
            # print(channel_out, end='\n')

            channel_out_3_1 = lzw_decode(channel_out_3_1, init_dictionary.copy())  # Dekodovanje poruke
            if channel_out_3_1[0] == -1:
                dummy = 1
                # print("LZW DECOMPOSITION FAILURE! RETRANSMISSION REQUESTED!")
                # print("RETRANSMITTING . . .", end='\n\n')
            else:
                break
        avg_3_1 += check_for_errors(characters, channel_out_3_1)

    for o1 in range(0, repeat, 1):
        while True:
            channel_out_5_1 = channel(channel_error[index], channel_in_5_1.copy())  # Simulacija Kanala
            # print("Channel output sequence: ", end='')
            # print(channel_out, end='\n')

            channel_out_5_1 = majority_decision(5, channel_out_5_1, bits_to_format)  # Vecinsko odlucivanje
            # print("Majority decision: ", end='')
            # print(channel_out, end='\n')

            for index1 in range(0, len(channel_out_5_1), 1):  # Formatiranje u cele brojeve
                channel_out_5_1[index1] = int(channel_out_5_1[index1], 2)
            # print("LZW decompression input: ", end='')
            # print(channel_out, end='\n')

            channel_out_5_1 = lzw_decode(channel_out_5_1, init_dictionary.copy())  # Dekodovanje poruke
            if channel_out_5_1[0] == -1:  # Pri neuspesnom dekodovanju
                dummy = 1
                # print("LZW DECOMPOSITION FAILURE! RETRANSMISSION REQUESTED!")
                # print("RETRANSMITTING . . .", end='\n\n')
            else:
                break
        avg_5_1 += check_for_errors(characters, channel_out_5_1)

    # print("Received message: ", end='')
    # print(channel_out)
    # print("Original message: ", end='')
    # print(characters)

    pe_3_1.append(avg_3_1 / repeat)
    print("Symbol error 3-1: ", end='')
    print(pe_3_1[index])
    pe_5_1.append(avg_5_1 / repeat)
    print("Symbol error 5-1: ", end='')
    print(pe_5_1[index])

print("\nError probability (3,1): ")
print(pe_3_1)
print("\nError probability (5,1): ")
print(pe_5_1)

plt.plot(channel_error, pe_3_1, label="(3,1)")
plt.plot(channel_error, pe_5_1, label="(5,1)")
plt.xlabel("Verovatnoca greske u kanalu")
plt.ylabel("Verovatnoca greske po sibmolu")
plt.grid()
plt.legend()
plt.show()
