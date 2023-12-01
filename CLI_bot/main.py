phone_book = {
    'Andrii':'+380123456789',
    'Dima': '+380234567890'
}

loop = True


def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
        except KeyError as e:
            result = '\tError. Record not found in phone book.'
        except ValueError as e:
            result = '\tError. Phone number expected to be 9...12 digits.'
        except IndexError:
            result = '\tError. Wrong Command format.\n' + helper()
            # result = helper()
        except Exception as e:
            result = 'Exception\n' + e
        return result
    return inner


def helper(*tokens):
    msg ='''
        hello   - відповідає у консоль "How can I help you?
        add     - За цією командою бот зберігає у пам'яті новий контакт. <Name> <phone number>
        change  - За цією командою бот зберігає в пам'яті новий номер телефону існуючого контакту. <Name> <phone number>
        phone   - За цією командою бот виводить у консоль номер телефону для зазначеного контакту <Name>.
        show all- За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.
        good bye- бот завершує свою роботу після того, як виведе у консоль "Good bye!".
        close   - бот завершує свою роботу після того, як виведе у консоль "Good bye!".
        exit    - бот завершує свою роботу після того, як виведе у консоль "Good bye!".
        help    - Вивод цього повідомлення.
        .       - завершення роботи бота.
        '''
    return msg


@input_error
def bye(*tokens):
    
    global loop

    if (tokens[0] == 'good'):
        if (len(tokens) != 2) or (tokens[1] != 'bye'):
            raise IndexError
    
    msg = 'Good bye!'
    loop = False

    return msg


@input_error
def hello(*tokens):
    msg = "How can I help you? "
    return msg


@input_error
def add(*tokens):
    global phone_book

    if len(tokens) == 3:

        if not phone(*tokens[:2]).startswith('\tError. '):
            msg = f'Record {tokens[1]} already exists in phone book.'
        else:
            phone_no = number_check(tokens[2])

            if phone_no.isdigit():
                phone_book[tokens[1]] = '+' + phone_no
                msg = f'contact {tokens[1]}: +{phone_no} added.'
            else:
                msg = phone_no
    else:
        raise IndexError
    
    return msg


@input_error
def change(*tokens):
    global phone_book

    if len(tokens) != 3:
        raise IndexError
    if tokens[1] in phone_book.keys():
        phone_no = number_check(tokens[2])
        phone_book[tokens[1]] = '+' + phone_no
        msg = f'contact {tokens[1]}: updated to +{phone_no}'
    else:
        raise KeyError

    return msg


@input_error
def phone(*tokens):
    global phone_book

    if len(tokens) != 2:
        raise IndexError

    if tokens[1] in phone_book.keys():
        msg = f'{tokens[1]}: {phone_book.get(tokens[1])}'
    else:
        raise KeyError

    return msg


@input_error
def show(*tokens):
    global phone_book

    if tokens[1].lower() == 'all':
        msg = ''
        for key, value in phone_book.items():
            msg = msg + f'{key}: {value}\n'
        msg = msg[:-1]
    else:
        raise KeyError

    return msg


def normalize(string: str):
    string = string.strip()
    string = string.split(' ')
    string = [i for i in filter(lambda x: x !='', string)]
    string[0] = string[0].lower()
    string = ' '.join(string)
    return string


def number_check(input: str):
    
    if input.startswith('+'):
        output = input[1:]
    if not input.isdigit():
        raise ValueError
    if len(input) == 12:
        output = input
    elif len(input) == 10:
        output = '38' + input
    elif len(input) == 9:
        output = '380' + input
    else:
        raise ValueError

    return output


@input_error
def main():
    COMMANDS = {
        'hello': hello,
        'show': show,
        'add': add,
        'change': change,
        'phone': phone,
        'good': bye,
        'close': bye,
        'exit': bye,
        'help': helper
    }

    msg = 'Enter command: '

    while loop:
        inp = normalize(input(msg))  # .lower().strip()
        
        if inp == '':
            continue
        elif inp == '.':
            break
        
        inp = inp.split(' ')

        resp = COMMANDS.get(inp[0], helper)(*inp)
        print(resp)

if __name__ == '__main__':
    main()