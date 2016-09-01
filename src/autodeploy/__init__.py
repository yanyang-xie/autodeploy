s = '''  

inet 172.31.13.47  Bcst172.31.15.255  Msk255.255.240.0 '''

internal_ip = s.split('Bcst')[0].replace('inet', '').strip()
print internal_ip