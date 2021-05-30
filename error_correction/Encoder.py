# message has to be the message in binary format
# basis is a List of the number representatives of the letters
def encode(message, basis):
    if not check_message(message):
        return False
    # transform binary message into a number
    int_message = int(message, 2)
    return_list = []

    for x in basis:
        return_list.append(int_message % x)

    return return_list


# checks if the message is not empty and in binary format
def check_message(message):
    if message:
        for character in message:
            if character != '0' and character != '1':
                return False
        return True
    return False


def main():
    print(encode("10110100", [13, 7, 15, 17, 11]))


if __name__ == "__main__":
    # execute only if run as a script
    main()
