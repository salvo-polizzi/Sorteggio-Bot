#setup the token.txt file
import argparse


def create_parser() -> None:
    parser = argparse.ArgumentParser(description="Set up your personal token")
    parser.add_argument("token", type=str, help="The token of your telegram bot")
    return parser


def main():
    #creating token.txt file
    f = open("token.txt", "w")
    
    #creating the parser
    parser = create_parser()
    args = vars(parser.parse_args())

    #writing the token in the file
    f.write(args["token"])



main()