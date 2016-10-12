def dict_keys_TO_list(rawest_keys):
    raw_keys = str(rawest_keys)
    raw_keys = raw_keys[12:-3]
    raw_keys = raw_keys.replace(',', '')
    raw_keys = raw_keys.replace("'", '')
    keys = raw_keys.split()
    return keys



lista = {"fruit": "apple", "ammount": 3, "quality": 4}
basket = ['apple', 'banana', 'orange']

keys = dict_keys_TO_list(lista.keys())
for x in range(len(sorted(keys))):
	print (keys[x], end=" ")
	print (lista.get(keys[x]))

for x in set(basket):
	print (x)


"""
print (lista["ammount"])

for i in lista:
	print (lista[i])
"""




















