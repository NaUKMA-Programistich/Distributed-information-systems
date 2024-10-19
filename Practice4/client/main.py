import grpc

from client import simple_pb2, simple_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = simple_pb2_grpc.GreeterStub(channel)
        print("Greeter client started")

        while True:
            print("------------")
            print("Choose an option:")
            print("1. Say Hello")
            print("2. Say Hello Again in stream")
            print("3. Exit")
            option = input("Option: ")
            if option == '1':
                name = input("Enter your name: ")
                response = stub.SayHello(simple_pb2.HelloRequest(name=name))
                print("Greeter client received: " + response.message)
            elif option == '2':
                name = input("Enter your name: ")
                response = stub.SayHelloAgain(simple_pb2.HelloRequest(name=name))
                for resp in response:
                    print("Greeter client received: " + resp.message)
            elif option == '3':
                print("Exiting...")
                break
            else:
                print("Invalid option")

if __name__ == '__main__':
    run()
