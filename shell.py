from brain.personality import personality
from core.command_processor import processor


def shell():

    print(personality.introduce())

    while True:

        cmd = input("Ahmad > ")

        if cmd.lower() in ["exit", "quit"]:

            print("خداحافظ احمد ❤️")

            break

        result = processor.process(cmd)

        print(result)


if __name__ == "__main__":

    shell()