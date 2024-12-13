from src.main import Parser

def test_check_if_commands_are_valid():
    test_cases = ["PING\r\n", "PONG\r\n", "SUB FOO 1\r\n", "PUB CodingChallenge 11\r\nHello John!\r\n"]
    for test_case in test_cases:
        print(test_case)
        parser = Parser(test_case)
        assert parser.check_input_validity() == True
