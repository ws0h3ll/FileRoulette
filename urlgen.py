import string
import random
def urlgen(a,s,t): #a is link to append to, s is the size of the appended string, t is the type of string
  chars = ''
  if 'a' in t:
    chars += string.ascii_lowercase
  if 'A' in t:
    chars += string.ascii_uppercase
  if '1' in t:
    chars += string.digits
  
  print(a + ''.join(random.choice(chars) for _ in range(s))) # return could be put here
"""
a = link to append to 
s = size of end 
t = type of chars to do

For uppercase letters put 'A' in the t variable, for lowercase letters put 'a' in the t variable for numbers put '1' in the t variable
suggested improvement : is much simpler and less lines of code
by nemo as an attempt at an improvement on cm-steffens script 'urlgen'
"""
