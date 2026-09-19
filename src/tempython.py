import sys
from errors import error_handling

#basic shape of interpreter
class Tempython:

    #echo code in file and error
    def run(self, source):
        print(source)
        raise NotImplementedError("Scanner Not Implemented")

    #convert to string and call run function
    def run_file(self, path):
        with open(path) as source:
            self.run(source.read())
        if error_handling.error_present:
            return
        return

    #enter REPL mode, echo input with error, and exit REPL mode
    def run_prompt(self):
        while True:
            try:
                line = input("> ")
            except (KeyboardInterrupt):
                return
            self.run(line)
            raise NotImplementedError("Scanner Not Implemented")
        
#correct usage or call correct function based upon input.
def main():
    if len(sys.argv) > 2:
        print("Usage: python src/tempython.py [script]")
        print("Or: python src/tempython.py")
        return
    tempython = Tempython()
    if len(sys.argv) == 2:
        return tempython.run_file(sys.argv[1])
    else:
        tempython.run_prompt()

if __name__ == "__main__":
    sys.exit(main())