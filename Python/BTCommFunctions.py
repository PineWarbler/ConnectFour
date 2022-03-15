# These functions written by P. Reynolds 3/2022
# note that Python 3.9.x may be required for native socket support

def listen_for_query(addr, port, maxSize=1024, backlog=1):
    '''
    starts a server on this machine's bluetooth card, then connects (first come, first serve) to external device, then returns data sent from external device
    Once the server accepts the query, function will close server instance.
    Recommended to call this function first before calling any related bluetooth query functions

    Parameters:
        addr : str
                the bluetooth address of this machine's bluetooth card in form XX:XX:XX:XX:XX:XX
        port : int
                the channel/port for connection (kinda like a walkie-talkie channel); ports must be equal to communicate across
        maxSize : int (OPTIONAL)
                the maximum size chunk of data to accept from the external device
        backlog : int (OPTIONAL)
                maximum number of connection requests to be held in a queue for processing
    Returns:
        the data submitted from the external device in byte form
    '''
    import socket
    
    data = None
    with socket.socket(socket.AF_BLUETOOTH,
                    socket.SOCK_STREAM,
                    socket.BTPROTO_RFCOMM) as s:
        s.bind((addr, port))
        s.listen(backlog)
        client, address = s.accept()
        while True:
            try:
                data = client.recv(maxSize)
                if data:
                    client.close()
                    s.close()
                    break
            except ConnectionResetError:
                print('Client disconnected')
                break
    return data

def respond_to_client(data_to_send, client_addr, port, maxSize=1024, backlog=1):
    '''
    sends data to a client once; only call this function from the server machine!
    Please be sure to call this function immediately after `listen_for_query` to make sure to not miss data sent from client!

    Parameters:
        data_to_send : bytes
                the data to send to the client
        client_addr : str
                the bluetooth address of the (external) client machine's bluetooth card in form XX:XX:XX:XX:XX:XX
        port : int
                the channel/port for connection (kinda like a walkie-talkie channel); ports must be equal to communicate across
        maxSize : int (OPTIONAL)
                the maximum size chunk of data to accept from the external device
        backlog : int (OPTIONAL)
                maximum number of connection requests to be held in a queue for processing
    Returns:
        Nothing
    '''
    import socket
    ## commence sending data to client  ##
    with socket.socket(socket.AF_BLUETOOTH,
                    socket.SOCK_STREAM,
                    socket.BTPROTO_RFCOMM) as s:

        while True: # wait for connection to become available
            try:
                s.connect((client_addr, port))
                break
            except:
                pass

        s.send(data_to_send)
        s.close()


def send_query_to_server_and_wait(data_to_send, server_addr, addr, port, maxSize=1024, backlog=1):
    '''
    submits a client's query (sends data) to the listening server and waits until the server responds.  Then returns data from server.

    Parameters:
        data_to_send : bytes
                the data to send to the server
        server_addr : str
                the bluetooth address of the (external) server machine's bluetooth card in form XX:XX:XX:XX:XX:XX
        addr : str
                the bluetooth address of this (internal) machine's bluetooth card in form XX:XX:XX:XX:XX:XX
        port : int
                the channel/port for connection (kinda like a walkie-talkie channel); ports must be equal to communicate across
        maxSize : int (OPTIONAL)
                the maximum size chunk of data to accept from the external device
        backlog : int (OPTIONAL)
                maximum number of connection requests to be held in a queue for processing
    Returns:
        the data returned from the server in response to the client's query
    '''
    import socket
    
    ## commence sending data to server  ##
    with socket.socket(socket.AF_BLUETOOTH,
                    socket.SOCK_STREAM,
                    socket.BTPROTO_RFCOMM) as c:

        while True: # wait for connection to become available
            try:
                c.connect((server_addr, port))
                break
            except:
                pass

        c.send(data_to_send)
        c.close()

    ## commence waiting for a server reply ##
    data = None
    with socket.socket(socket.AF_BLUETOOTH,
                    socket.SOCK_STREAM,
                    socket.BTPROTO_RFCOMM) as s:
        while True: # keep trying to make connection with the server
            try:
                s.bind((addr, port))
                s.listen(backlog)
                client, address = s.accept()
                break # because we've made contact
            except:
                pass

        while True: # waiting for server to transmit the data
            try:
                data = client.recv(maxSize)
                if data:
                    client.close()
                    s.close()
                    break
            except ConnectionResetError:
                print('Client unexpectedly disconnected')
                break
    return data
