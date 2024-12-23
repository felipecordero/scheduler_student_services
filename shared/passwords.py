# import modules
import string
import random

# store all characters in lists 
s1 = list(string.ascii_lowercase)
s2 = list(string.ascii_uppercase)
s3 = list(string.digits)

characters_number = 4

def password_generator():
    
    # shuffle all lists
    random.shuffle(s1)
    random.shuffle(s2)
    random.shuffle(s3)
    
    # generation of the password (60% letters and 40% digits & punctuations)
    result = []
    
    for x in range(characters_number):
    
        result.append(s1[x])
        result.append(s2[x])
        result.append(s3[x])
    
    # shuffle result
    random.shuffle(result)
    
    # join result
    password = "".join(result)
    return password