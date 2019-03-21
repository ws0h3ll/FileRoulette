"""Generate a random URL with the specified ruleset.

This module defines the urlgen function. This function can generate random URLs
for all kinds of services. Here are some examples of how to use it:

hastebin.com
    urlgen("https://hastebin.com/raw/{}", "a", 10)

imgur.com
    urlgen("https://imgur.com/{}", "aA1", 7)

pastebin.com
    urlgen("https://pastebin.com/{}", "aA1", 8)

uploadfiles.io
    urlgen("https://uploadfiles.io/{}", "a1", 5)

"""
import string
import sys
import random
def urlgen(a,s,t): #a is link to append to, s is the size of the appended string, t is the type of string
    """Generate a random URL with the specified rules.

    Parameters
    ----------
    template
        A URL template with {} in the place where the generated key goes.
    charset
        A string specifying the types of characters to be included in the key.
        The string can be any combination of the following:
            - a lowercase letter (a-z)
            - an uppercase letter (A-Z)
            - a digit (0-9)
        If the charset contains a lowercase letter, it specifies that the key
        can contain lowercase letters. If it contains an uppercase letter, the
        key can contain uppercase letters. If it contains a digit, the key can
        contain digits.
    length
        The length of the key.

    Returns
    -------
    new_url
        A randomly-generated URL that matches the definition.
    """  
    chars = ''
      for i in t:
        if i in string.ascii_lowercase:
          chars += string.ascii_lowercase
        if i in string.ascii_uppercase:
          chars += string.ascii_uppercase
        if i in string.digits:
          chars += string.digits
      if '{}' not in a:
        print('Missing parameters "{}" please try again')
        sys.exit()
      print(a.format(''.join(random.choice(chars) for _ in range(s))))
urlgen('https://test/{}/test',6,'aZ1')  #valid test


