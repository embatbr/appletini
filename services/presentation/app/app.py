"""Module to start everything.
"""


from console import Reader, Writer, Terminal
from clients import BusinessClient
from configs import business_configs


reader = Reader()
writer = Writer()

business_client = BusinessClient(business_configs)

terminal = Terminal(reader, writer, business_client)
terminal.run()