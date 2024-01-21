import socket

def send_data_to_server(server_host, server_port, data):
    # Khởi tạo socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Kết nối đến server
        client_socket.connect((server_host, server_port))
        print(f"Connected to {server_host}:{server_port}")

        # Gửi dữ liệu đến server
        client_socket.send(data.encode('utf-8'))
        print(f"Sent data to server: {data}")

        # Nhận phản hồi từ server
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received response from server: {response}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Đóng kết nối
        client_socket.close()

if __name__ == "__main__":
    # Địa chỉ IP và port của server
    server_host = 'localhost'
    server_port = 12345

    # Dữ liệu cần gửi
    data_to_send = "Minh"

    # Gửi dữ liệu đến server
    send_data_to_server(server_host, server_port, data_to_send)
