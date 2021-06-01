import argparse

parser = argparse.ArgumentParser(description="Programm for fiend count of "
                                             "friends")
parser.add_argument("user_id", help="user id in vk",
                    type=int)
