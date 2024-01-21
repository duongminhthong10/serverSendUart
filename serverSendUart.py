import socket
import threading
import serial

def handle_client(client_socket, com_port_1='COM90', com_port_2='COM99', baudrate=115200):
    # Khởi tạo cổng COM
    ser_1 = serial.Serial(baudrate=baudrate, timeout=1)
    ser_2 = serial.Serial(baudrate=baudrate, timeout=1)

    try:
        ser_1.port = com_port_1
        ser_2.port = com_port_2

        while True:
            # Nhận dữ liệu từ client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"Received data from client: {data}")

            # Kiểm tra độ dài của dữ liệu và mở cổng COM tương ứng
            if len(data) < 3:
                ser_2.close()  # Đóng cổng COM99 trước khi mở cổng COM90
                ser_1.open()
                ser_1.write(data.encode('utf-8'))
                print(f"Sent data to {ser_1.name}: {data}")
            else:
                ser_1.close()  # Đóng cổng COM90 trước khi mở cổng COM99
                ser_2.open()
                ser_2.write(data.encode('utf-8'))
                print(f"Sent data to {ser_2.name}: {data}")

            # Phản hồi cho client
            response = "Data received successfully"
            client_socket.send(response.encode('utf-8'))
            print(f"Sent response to client: {response}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Đóng kết nối với client
        client_socket.close()

        # Đảm bảo đóng cổng COM khi kết thúc (nếu đã mở)
        if ser_1.isOpen():
            ser_1.close()
        if ser_2.isOpen():
            ser_2.close()

def start_server(host, port):
    # Khởi tạo server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    running_flag = True  # Biến cờ để theo dõi trạng thái của server

    try:
        while running_flag:
            # Chờ kết nối từ client
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Xử lý mỗi kết nối trong một luồng riêng biệt
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    except KeyboardInterrupt:
        print("Server stopped by user.")
        running_flag = False

    finally:
        # Đóng server socket khi kết thúc
        server_socket.close()

if __name__ == "__main__":
    # Chạy server với host là localhost và port là 12345
    start_server('192.168.1.6', 9999)
