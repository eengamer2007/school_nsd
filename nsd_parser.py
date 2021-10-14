def nsd_parser_from_file(input_file):
    # open file and it if it doesn't extist handle the error
    try:
        print(input_file[-3:len(input_file)])
        if not input_file[-3:len(input_file)] in ["txt"]:
            print("file not a supported file type")
            exit()
        f = open(input_file)
    except FileNotFoundError:
        print("file: {} not found".format(input_file))
        exit()
    in_arr = []
    for i in f:
        if not i.strip() == "":
            in_arr.append(i.strip())
    in_arr.append("program_end")
    print(in_arr)
    f.close()

    parsed = nsd_pass(in_arr,[])

    print(parsed)
    return parsed

location = 0

def nsd_pass(arr, out_arr):
    global location
    last_if = 0
    last_else = 0
    while location < len(arr) -1:
        print("line:", location,",", arr[location])
        match arr[location].lower().split():
            case ["while", statement]:
                location += 1
                out = nsd_pass(arr,["while", statement])
                out_arr.append(out)
            case ["loop"]:
                location += 1
                out = nsd_pass(arr,["loop"])
                out_arr.append(out)
            case ["for", *statement]:
                location += 1
                stat_str = ""
                for i in statement:
                    stat_str += i
                out = nsd_pass(arr,[])
                for_arr = ["for",stat_str]
                for_arr.append(out)
                out_arr.append(for_arr)
            case ["if", *statement]:
                location += 1
                stat_str = ""
                for i in statement:
                    stat_str += i
                if_arr = ["if", stat_str]
                out = nsd_pass(arr,[])
                print(out)
                if_arr.append(out)
                out = nsd_pass(arr,[])
                print(out)
                if_arr.append(out)
                out_arr.append(if_arr)
                last_if = 1
            case ["else"]:
                location += 1
                return out_arr
            case ["end"]:
                location += 1
                return out_arr
            case x:
                location += 1
                print(x)
                out_arr.append(arr[location-1])
    return out_arr