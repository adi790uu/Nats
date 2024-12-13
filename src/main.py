class Parser:
    def __init__(self, input: str):
        self.input = input
        self.commands = {"CONNECT", "PING", "PONG", "SUB", "PUB"}
    def check_input_validity(self):
        try:
            command_split = self.input.split("\r\n")
            command_line = command_split[0]
            command = command_line.split(" ")[0].strip()
            if command not in self.commands:
                return False
            elif command == "PUB":
                return self.validate_pub(command_line, command_split[1:-1])
            elif command == "SUB":
                return self.validate_sub(command_line)
            return True
        except Exception:
            return False

    def validate_sub(self, command_line: str):
        try:
            args = command_line.split(" ")
            if len(args) < 3:
                return False
            return True
        except Exception:
            return False

    def validate_pub(self, command_line: str, body_lines: list):
        try:
            args = command_line.split(" ")
            if len(args) < 3:
                return False
            length = int(args[2])
            body = "\r\n".join(body_lines)

            return len(body) == length
        except Exception:
            return False

input = "PING\r\n"
parser = Parser(input)

valid = parser.check_input_validity()
print(valid)
