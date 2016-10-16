
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
while(1):
    answer=input("Hello?\n")
    if(answer=="q"):
        break

    elif(answer=="h"):
        print("q" + "\t\t" + "quit" + "\n" +
              "inv" + "\t\t" + "inventory" + "\n" +
              "use" + "\t\t" + "use hoe" + "\n" +
              "add" + "\t\t" + "add custom hoe" + "\n" +
              "h" + "\t\t" + "display this page")


    elif(answer=="inv"):
        keys = dict_keys_TO_list(hoes[0].keys())
        for x in range(len(keys)):
            print(keys[x] + " "*(16-len(str(keys[x]))), end="")
        print("")

        for x in range(len(hoes)):
            for y in range(len(keys)):
                print(hoes[x].get(keys[y]), " "*(15-len(str(hoes[x].get(keys[y])))), end="")
            print("")

    elif (answer=="use"):
        print("Available hoes:")
        for x in range(len(hoes)):
            print(hoes[x].get("Name"))
        selected_hoe=input("Select one:")

        for x in range(len(hoes)+1):
            if(x==len(hoes)):
                print("Who's ", selected_hoe , "? GTFO!")
            elif(selected_hoe==hoes[x].get("Name")):
                print("Have fun with", selected_hoe, "now hand over", hoes[x].get("Price"), "£!")
                hoes[x]["Balance"]=hoes[x].get("Balance") + hoes[x].get("Price")
                break

    elif(answer=="add"):
        name=input("Name?:")
        price=int(input("Price?:"))
        perforrmance=input("Performance?:")
        hoes.append({"Name":name, "Price":price, "Performance":perforrmance, "Balance":0})

    else:
        print("What do you mean \""+ answer + "\"?")