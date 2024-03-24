import colorama
import socket
import json
import echo_protocol as echo

IP = '127.0.0.1'
PROMPT = 'Guess: '
LINIUTE = ''
CHOICE = ''

def print_report(word, report):
    print(" " * (len(PROMPT)-1), end="")
    for i in range(len(report)):
        if report[i] == 'green':
            print(f'{colorama.Fore.GREEN}{word[i]}{colorama.Style.RESET_ALL}', end="")
        elif report[i] == 'yellow':
            print(f'{colorama.Fore.YELLOW}{word[i]}{colorama.Style.RESET_ALL}', end="")
        else:
            print(f'{word[i]}', end="")
    print()


if __name__ == "__main__":
    colorama.init()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, echo.PORT))

    socket_wrapper = echo.SocketWrapper(sock)

    cuvant = socket_wrapper.recv_msg()

    for i in range(1, len(cuvant) + 1):
        LINIUTE = LINIUTE + '_'

    print("Welcome to Wordle!")

    while CHOICE == '' or CHOICE == "yes":
        print(f"{PROMPT}{LINIUTE}")
        guess = input(PROMPT)
        socket_wrapper.send_msg(guess)
        rcvd = socket_wrapper.recv_msg()
        if not rcvd:
            print("Unexpected end of connection, server is down")
            break
        # {
        #  'type': ''
        #  'value': ['green', 'yellow', '']
        #
        rcvd_deserialized = json.loads(rcvd)
        msg_type = rcvd_deserialized['type']

        if msg_type == 'guessed':
            print_report(guess, rcvd_deserialized['value'])
            print("Well Done! You have guessed the word")
            print("Do you want to play again ? yes/no")
            CHOICE = input(CHOICE)
            if  CHOICE != "yes":
                break
            else:
                CHOICE = ''

        if msg_type == 'out_of_guesses':
            print_report(guess, rcvd_deserialized['value'])
            print("Out of guesses, the game will end")
            print("Do you want to play again ? yes/no")
            CHOICE=input(CHOICE)
            if CHOICE != "yes":
                break
            else:
                CHOICE = ''

        if msg_type == 'bad_guess':
            print('Bad guess, try again')

        if msg_type == 'report':
            print_report(guess, rcvd_deserialized['value'])

    print("Thanks for playing.")