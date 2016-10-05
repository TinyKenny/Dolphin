import heapq
#is an algorithm
def dict_keys_TO_list(rawest_keys):
    raw_keys = str(rawest_keys)
    raw_keys = raw_keys[12:-3]
    raw_keys = raw_keys.replace(',', '')
    raw_keys = raw_keys.replace("'", '')
    keys = raw_keys.split()
    string_to_return =""
    #print(string_to_return)
    for x in range(len(keys)):
        string_to_return=string_to_return + keys[x] + "\t"
    return string_to_return

hoes = [{"Name":"Florida", "Price":10, "Performance":0.6, "Balance":0 },
        {"Name":"Gerorgia", "Price":18, "Performance":0.8, "Balance":0 },
        {"Name":"Angel", "Price":30, "Performance":1.0, "Balance":0 },
        {"Name":"Alex", "Price":5, "Performance":0.2, "Balance":10 }]
answer=""
print("Select h to get help")
while(1):
    answer=input("Hello?\n")
    if(answer=="q"):
        break

    if(answer=="h"):
        print("q" + "\n"
              "inventory" + "\n")

    if(answer=="inventory"):
        keys = dict_keys_TO_list(hoes[0].keys())
        for x in range(len(keys)):
            print(keys[x] + "", end="")
            '''
        for x in range(len(hoes)):
            print(hoes[x].get("Price") , "\t\t",
                  hoes[x].get("Performance") , "\t" ,
                  hoes[x].get("Balance") , "\t" ,
                  hoes[x].get("Name"))
        '''
            #djdj