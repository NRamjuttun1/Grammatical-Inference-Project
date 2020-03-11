def func(var, *ovar):
    if (ovar == None):
        print(var)
    else:
        print(ovar)

func("Hello")
func("Hello", "GoodBye")
