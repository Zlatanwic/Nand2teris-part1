import sys
sys.path.insert(0, "../parser")
from parser import Parser

def main():
    #open and save file
    if len(sys.argv) != 3:
        sys.exit("Wrong input")
    inputFileStr = sys.argv[1]
    outFileStr = sys.argv[2]
    raw_rows = []
    bin_codes = []
    with open(inputFileStr, "r") as file:
        for row in file:
            raw_rows.append(row)
    p = Parser(raw_rows)
    p.run_first_pass()
    p.run_second_pass()
    bin_codes = p.get_binary_codes()
    with open(outFileStr, 'w', newline='\n') as file:
        for line in bin_codes:
            file.write(f"{line}\n")

main()