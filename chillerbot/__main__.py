from chillerbot.cmd import Actions, createParser


def main():
    choices = Actions.getActions()

    parser = createParser(choices.keys())
    namespace = parser.parse_args()

    choices[namespace.command]()


if __name__ == '__main__':
    main()
