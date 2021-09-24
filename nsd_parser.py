def nsd_parser_from_file(input_file):
    '''
    # open file and it if it doesn't extist handle the error
    try:
        f = open(input_file)
    except FileNotFoundError:
        print("file: {} not found".format(input_file))
        exit()

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
    return ["hello", "hello", ["for", "a", ["loop", ["if", "a", ["hello","bye"],["bye"]], ["loop","cheese"], "cheese"], "hello", "hello"],["loop","cheese"]]
    #return commands_array