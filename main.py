from time import sleep as sp



def get_weather(sleep: int=1):
    while True:
        print("Hello World")
        if sleep > 0:
            sp(sleep) 

if __name__ == "__main__":
    get_weather(2)

    