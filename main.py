from utility import refresh_display
import commands


def main():
    refresh_display()
    while True:
        user_input = input().strip().lower().split()
        if not user_input:
            refresh_display()
            continue
        print()
        cmd = user_input[0]

        try:
            command_func = getattr(commands, cmd + '_cmd')
        except AttributeError:
            refresh_display('Command not found')
            continue

        command_func(user_input[1:])


if __name__ == '__main__':
    main()
