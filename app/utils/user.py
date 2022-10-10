

def is_valid_password(password):
    l, u, d = 0, 0, 0
    if (len(password) >= 8):
        for i in password:
            # counting lowercase alphabets
            if (i.islower()):
                l+=1 
            # counting uppercase alphabets
            if (i.isupper()):
                u+=1
            # counting digits
            if (i.isdigit()):
                d+=1
    
    return (l>=1 and u>=1 and d>=1 and l+u+d==len(password))