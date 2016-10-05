
def dict_keys_TO_list(rawest_keys):
    raw_keys = str(rawest_keys)
    raw_keys = raw_keys[12:-3]
    raw_keys = raw_keys.replace(',', '')
    raw_keys = raw_keys.replace("'", '')
    keys = raw_keys.split()
    return keys

hoes = [{"Name":"Florida", "Price":10, "Performance":0.6, "Balance":0 },
        {"Name":"Gerorgia", "Price":18, "Performance":0.8, "Balance":0 },
        {"Name":"Angel", "Price":30, "Performance":1.0, "Balance":0 },
        {"Name":"Alex", "Price":5, "Performance":0.2, "Balance":10 }]
answer=""
print("Select h to get help")
looper=1
while(looper):
    looper =0
    answer=input("Hello?\n")
    if(answer=="q"):
        break

    if(answer=="h"):
        print("q" + "\n"
              "inv" + "\n")

    if(answer=="inv"):
        keys = dict_keys_TO_list(hoes[0].keys())
        for x in range(len(keys)):
            print(keys[x] + "\t\t", end="")
        print("")

        for x in range(len(hoes)):
            for y in range(len(keys)):
                print(hoes[x].get(keys[y]), "\t\t", end="")
            print("")