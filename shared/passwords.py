# import modules
import string
import random

# store all characters in lists 
s1 = list(string.ascii_lowercase)
s2 = list(string.ascii_uppercase)
# s3 = list(string.digits)
s4 = list(string.punctuation)

characters_number = 15

def password_generator():
    
    # shuffle all lists
    random.shuffle(s1)
    random.shuffle(s2)
    # random.shuffle(s3)
    random.shuffle(s4)
    
    
    # calculate 30% & 20% of number of characters
    part1 = round(characters_number * (30/100))
    part2 = round(characters_number * (20/100))
    
    
    # generation of the password (60% letters and 40% digits & punctuations)
    result = []
    
    for x in range(part1):
    
        result.append(s1[x])
        result.append(s2[x])
    
    for x in range(part2):
    
        # result.append(s3[x])
        result.append(s4[x])
    
    
    # shuffle result
    random.shuffle(result)
    
    
    # join result
    password = "".join(result)
    return password