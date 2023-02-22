import re


def feature_construction(rid):
    feature_data = None

    # Step1 Domain Division
    result = re.match('^(\d\d\d\d)(\S\S)(\d\d\d)$', rid)
    if result is None:
        return None
    year = result.group(1)
    dept = result.group(2)
    num = result.group(3)
    # Step2 Fileld Division 
    try:
        feature_data = _integer_identifier(year) + _a1(year) + _a2(dept) + _a3(num[0]) + _a4(num[1]) + _a5(num[2])
    except:
        return None


    return feature_data


def data_encryption(rid, date):
    pass

def _integer_identifier(key):
    key = int(key)
    val = None

    if key >= 2050:
        val = None
    elif key >= 2025:
        val = '9'
    elif key >= 2020:
        val = '8'
    elif key >= 2015:
        val = '7'
    elif key >= 2010:
        val = '6'
    elif key >= 2005:
        val = '5'
    elif key >= 2000:
        val = '4'
    elif key >= 1995:
        val = '3'
    elif key >= 1990:
        val = '2'
    elif key >= 1980:
        val = '1'
    elif key >= 1950:
        val = '0'

    return val

def _a1(key):

    key = int(key)
    val = None

    if key >= 2050:
        val = None
    elif key >= 2025:
        val = 'XCD'
    elif key >= 2020:
        val = 'SCD'
    elif key >= 2015:
        val = 'PBC'
    elif key >= 2010:
        val = 'HZA'
    elif key >= 2005:
        val = 'JAC'
    elif key >= 2000:
        val = 'EAC'
    elif key >= 1995:
        val = 'CEF'
    elif key >= 1990:
        val = 'ABC'
    
    return val

def _a2(key):

    key = str(key)
    val = None
    
    if ord(key[0]) >= ord('Z'):
        val = None
    elif ord(key[0]) >= ord('X'):
        val = '99'
    elif ord(key[0]) >= ord('S'):
        val = '90'
    elif ord(key[0]) >= ord('P'):
        val = '81'
    elif ord(key[0]) >= ord('N'):
        val = '78'
    elif ord(key[0]) >= ord('K'):
        val = '67'
    elif ord(key[0]) >= ord('F'):
        val = '52'
    elif ord(key[0]) >= ord('D'):
        val = '41'
    elif ord(key[0]) >= ord('A'):
        val = '34'
    
    return val


def _a3(key):

    key = int(key)
    val = None
    
    if key >= 10:
        val = None
    elif key >= 6:
        val = 'F'
    elif key >= 4:
        val = 'E'
    elif key >= 2:
        val = 'D'
    elif key >= 0:
        val = 'B'

    return val

def _a4(key):

    key = int(key)
    val = None
    
    if key >= 10:
        val = None
    elif key >= 8:
        val = 'F'
    elif key >= 6:
        val = 'D'
    elif key >= 4:
        val = 'C'
    elif key >= 2:
        val = 'B'
    elif key >= 0:
        val = 'A'

    return val

def _a5(key):

    key = int(key)
    val = None
    
    if key >= 10:
        val = None
    elif key >= 8:
        val = 'Q'
    elif key >= 7:
        val = 'K'
    elif key >= 6:
        val = 'F'
    elif key >= 5:
        val = 'D'
    elif key >= 4:
        val = 'C'
    elif key >= 3:
        val = 'B'
    elif key >= 0:
        val = 'A'

    return val


