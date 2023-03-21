def normalize_str(x):
    x = str(x)
    x = x.upper()
    x = x.replace(',','')
    x = ' '.join(x.split())
    x = x.replace(' ','_')
    return x
