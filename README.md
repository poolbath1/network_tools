# Network_tools
Network tools for Python Dev Accelerator class

## echo_server
Run the echo server like so:

    $ python echo_server.py

and in a seperate terminal:

    $ python echo_client.py "this is the message to send to the server"

Running the server script in one terminal should allow you to run the client script in a separate terminal. The client script takes an argument which is the message to send.  Upon completing, the response from the server is printed to stdout.

## HTTP2
Very simple HTTP server. Echo_server.py runs this now.

Original sources forked and modified from:
  - [Constantine Hatzis](https://github.com/constanthatz/network_tools/tree/echo)
  - [Henry Howes](https://github.com/henrykh/network_tools/tree/echo)
  - [Mark Saiget](https://github.com/bm5w/network_tools)
  - [Nick Becker](https://github.com/nbeck90/network_tools/blob/HTTP2/server.py)
