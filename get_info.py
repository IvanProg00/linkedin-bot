from re import findall

def transform_text(text=''):
    return ' '.join(findall(r'[A-z]{2,}', text))