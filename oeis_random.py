from random import randint
import urllib
from urllib.request import urlopen
import webbrowser

'''
Notes

- This program should be run in the same directory as a text file 'used.txt',
which will store sequences already seen.
- On Windows, this program can be paired with the Windows Task Scheduler to
automatically open the page for a (pseudo)random sequence at a specified time
each day (or at any regular interval).
'''

# this is a comment
#this is a test

file = r"used.txt"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
lines = [line[:-1] for line in lines]
filein.close()

def tester(url):
    '''
    Parameters
    ----------
    url : str
        url of OEIS page for sequence

    Returns
    -------
    bool
        True if the url is valid and not already used, False otherwise
    '''
    # check page exists 
    try:
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        # check it's not already been fetched on a previous day
        if url[17:] in lines:
            return False
        # check the sequence is not just a placeholder
        elif "allocated for" in html:
            return False
        else:
            return True
        
    except (urllib.error.HTTPError, AttributeError):
        return False

def gen_url():
    # find upper bound
    page = urlopen("https://oeis.org/")
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    ind1 = html.index("Contains") + 9
    ind2 = html.index("sequences.")
    upper_bound = int(html[ind1:ind2-1]) + 1000

    n = randint(1, upper_bound)
    l = len(str(n))
    s = "A" + "0"*(6 - l) + str(n)
    url = "https://oeis.org/" + s
    return s, url

def seq():
    s, url = gen_url()
    # "allocated for" test 
    #s = "A373477"
    #url = "https://oeis.org/" + s
    while not tester(url):
        s, url = gen_url()

    # add working url to used list
    filein2 = open(file, "a", encoding='UTF-8')
    filein2.write(s + "\n")
    filein2.close()
    webbrowser.open(url)

    return s

seq()
