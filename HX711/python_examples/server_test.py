from server_raspi import ServerRas

server_ras = ServerRas()


while True:
    # receive data
    data = server_ras.receive_data()
    print(data)
    if data is None:
        print("Failed to receive data. Closing connection.")
        break
    print(f"Received:{data}")

    if server_ras.send_data("Message"):
        print('sent msg')
    else:
        print('failed')
        break

server_ras.close()
