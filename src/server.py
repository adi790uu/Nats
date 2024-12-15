import asyncio

class AsyncNatsServer:
    def __init__(self, host='127.0.0.1', port=4222):
        self.host = host
        self.port = port
        self.clients = set()

    async def start(self):
        try:
            server = await asyncio.start_server(
                self.handle_client,
                self.host,
                self.port
            )
            print(f"Server is listening on {self.host}:{self.port}")

            async with server:
                await server.serve_forever()
        except Exception as e:
            print(f"Error: {e}")

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        self.clients.add(writer)
        try:
            info_message = "INFO {\"server_id\":\"DEMO\"}\r\n"
            writer.write(info_message.encode())
            await writer.drain()

            while True:
                try:
                    data = await reader.read(1024)
                    if not data:
                        break

                    message = data.decode('utf-8')
                    if message.startswith('PING'):
                        response = "PONG\r\n"
                        writer.write(response.encode())
                        await writer.drain()
                except asyncio.CancelledError:
                    break
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()
            print(f"Connection closed with {addr}")
    async def cleanup(self):
            print("Cleaning up server...")
            for writer in self.clients:
                writer.close()
                await writer.wait_closed()

async def main():
    server = AsyncNatsServer()
    try:
        await server.start()
    except KeyboardInterrupt:
            print("Shutting down server...")
            await server.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down server...")
