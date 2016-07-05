"""Module to start everything
"""


from console import Reader, Writer, Terminal


if __name__ == '__main__':
    reader = Reader()
    writer = Writer()

    terminal = Terminal(reader, writer)
    terminal.run()