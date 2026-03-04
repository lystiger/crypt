num = 14445

# list to an array to store the asciiiiii

chars = []

while num > 0:
    #get to the last character
    ascii = num % 256

    # convert and append it to the arrray to store itt
    chars.append(chr(ascii))

    #remove the last byte
    num //= 256

message ="".join(reversed(chars))

#should be 8m right?

print(message)

# why 256? 1 byte = 8 bits => 0 -> 255 values = 256 values

