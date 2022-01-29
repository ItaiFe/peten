from pywebsocket.server import WebsocketServer, WebsocketClient
import random 

def on_client_connect(server : WebsocketServer, 
                      client : WebsocketClient) -> None:
    # Add this client's socket id to a channel's user list.
    server.default_channel["users"].append(client.get_id())
    client.data["current_channel"] = server.default_channel

    print(server.channel_list)

def on_client_disconnect(server : WebsocketServer, 
                          client : WebsocketClient) -> None:
    # Remove the client from the channel it is currently in.
    client.data["current_channel"]["users"].remove(client.get_id())

    print(server.channel_list)

def on_client_data(server : WebsocketServer, 
                   client : WebsocketClient,
                   data) -> None:
    # Echo client's message.
    print("Received from client:", data)
    if data == "get_board":
        board = [[[random.randint(1, 3) if i < 2 else 0, [
                    i, j]] for j in range(7)] for i in range(6)]
        server.send_string(client.get_id(), str(board))

server = WebsocketServer("localhost", 9998,
                         client_buffer_size       = 1024,
                         pass_data_as_string      = True,
                         daemon_handshake_handler = False, # if set to True, main process 
                                                           # will exit immediately. Be sure to
                                                           # create an endless loop after
                                                           # server.start() has been called.
                         debug                    = False)

# You can set your own variables to server like below:
server.channel_list = {
    "general" : {
        "users" : []
    },
    "news" : {
        "users" : []
    }
}
server.default_channel = server.channel_list["general"]

server.set_special_handler("client_connect",    on_client_connect)
server.set_special_handler("client_disconnect", on_client_disconnect)
server.set_special_handler("client_data",       on_client_data)

server.start()