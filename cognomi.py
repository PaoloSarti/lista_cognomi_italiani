from bs4 import BeautifulSoup
import urllib.request
import codecs

accentate_dict = {
    'a':['a','à'],
    'e':['e','è','é'],
    'i':['i','ì'],
    'o':['o','ò'],
    'u':['u','ù']
}

def accents_names(name):
    try:
        i = name.index('\'')
    except:
        return [name]
    if i > 0 and name[i-1] in accentate_dict:
        return [name] + [name[:i-1] + c + name[i+1:] for c in accentate_dict[name[i-1]]]
    else:
        return [name]

def get_cognomi(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        return [l.text.split('-')[0].strip() for l in soup.find_all('li') if 'Origine del Cognome' in l.text]

def get_all_cognomi(baseurl = 'http://www.cognomix.it/origine-cognomi-italiani', maxlen=100, verbose=True):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cognomi_set = set()
    for letter in letters:
        for i in range(1, maxlen):
            l = get_cognomi('{}/{}/{}'.format(baseurl, letter, i))
            if all(c not in cognomi_set for c in l):
                if verbose:
                    print(letter, i)
                cur_set = set(ca for c in l for ca in accents_names(c))
                cognomi_set |= set(l)
                for c in sorted(cur_set):
                    yield c
            else:
                break

if __name__ == '__main__':
    with codecs.open('cognomi.txt', 'w', encoding='utf-8') as o:
        for c in get_all_cognomi():
            o.write(c+'\n')