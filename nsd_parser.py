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
        if i.strip() == "":
            continue
        in_arr.append(i.strip())
    in_arr.append("program_end")
    f.close()

    nsd_pass(in_arr,[])
#   { 
    '''
    commands_array = []

    #cheching if the command given is a loop, for-loop, end, if, else,endif
    for i in f:
        match i.lower().strip().split():
            case ["loop", statment]:
                indentation += 1
            case ["loop"]:
                indentation += 1
            case ["for", *statment] as thing:
                indentation += 1
            case ["for"]:
                print("for-loop without statement")
                exit()
            case ["end"]:
                indentation -= 1
                if indentation < 0:
                    print("too many end statements")
                    exit()
            case ["if", *statement]:
                pass
            case ["if"]:
                print("if statments without statments")
                exit()
            case ["else"]:
                pass
            case ["endif"]:
                pass
            case ["else if", *statement] | ["elif", *statement]:
                print("we dont do else if statements here")
                exit()
            case stuf:
                pass
    f.close()
    '''
#   }
    return ["hello", "hello", ["for", "a", ["while", "a", ["if", "a", ["hello","bye"],["bye"]], ["loop","cheese"], "cheese"], "hello", "hello"],["loop","cheese"]]
    #return commands_array

def nsd_pass(arr, out_arr):
    i = 0
    while i < len(arr):
        print("line: , ", i, arr[i])
        match arr[i].lower().split():
            case ["while", statement]:
                out_arr.append("while ")
                out_arr.append(statement)
                out = nsd_pass(arr[i+1:],[])
                out_arr.append(out[0])
                i += out[1]
            case ["loop"]:
                out_arr.append("loop")
                out = nsd_pass(arr[i:],[])
                out_arr.append(out[0])
                i += out[1]
            case ["for", *statment] as thing:
                out_arr.append("while ")
                out_arr.append(statment)
                out = nsd_pass(arr[i+1:],[])
                out_arr = out[0]
                i += out[1]
            case ["if", *statement]:
                out_arr.append("if ")
                out_arr.append(statement)
                out = nsd_pass_if(i,arr)
                out_arr.append(out[0])
                i += out[1]
            case ["else"]:
                print("found else without if")
                raise MemoryError
            case ["end"]:
                return (out_arr, i)
            case x:
                print(x)
                out_arr.append(arr[i])
        i += 1
    return out_arr

def nsd_pass_if(start, arr):
    i = start
    while i < len(arr):
        print("line: , ", i, arr[i])
        match arr[i].lower().split():
            case ["while", statement]:
                out_arr.append("while ")
                out_arr.append(statement)
                out = nsd_pass(arr[i+1:],[])
                out_arr.append(out[0])
                i += out[1]
            case ["loop"]:
                out_arr.append("loop")
                out = nsd_pass(arr[i:],[])
                out_arr.append(out[0])
                i += out[1]
            case ["for", *statment] as thing:
                out_arr.append("while ")
                out_arr.append(statment)
                out = nsd_pass(arr[i+1:],[])
                out_arr = out[0]
                i += out[1]
            case ["if", *statement]:
                out_arr.append("if ")
                out_arr.append(statement)
                out = nsd_pass_if(i,arr)
                out_arr.append(out[0])
                i += out[1]
            case ["else"]:
                print("found else without if")
                raise MemoryError
            case ["end"]:
                return (out_arr, i)
            case x:
                print(x)
                out_arr.append(arr[i])
        i += 1
    return (out_arr,i)