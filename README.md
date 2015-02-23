# Network_tools
Network tools for Python Dev Accelerator class

## echo_server
Run the echo server like so:

    $ python echo_server.py

and in a seperate terminal:

    $ python echo_client.py "this is the message to send to the server"

Running the server script in one terminal should allow you to run the client script in a separate terminal. The client script takes an argument which is the message to send.  Upon completing, the response from the server is printed to stdout.

Original sources forked and modified from:
  - [Constantine Hatzis](https://github.com/constanthatz/network_tools/tree/echo)
  - [Henry Howes](https://github.com/henrykh/network_tools/tree/echo)
