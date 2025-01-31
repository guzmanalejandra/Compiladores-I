from shunting import ShuntingYard

def main():
    regex = input("Ingresa regex: ")
    shunting_yard = ShuntingYard(regex)
    postfix = shunting_yard.to_postfix()
    print("Postfix notation:", postfix)

if __name__ == "__main__":
    main()
