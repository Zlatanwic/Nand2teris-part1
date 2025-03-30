import sys

sys.path.insert(0, "../hack_code")
from hack_code import Code

sys.path.insert(0, "../symbol_table")
from symbol_table import Symbol_table

from enum import Enum
import re


class InstructionType(Enum):
    A_INSTRUCTION = 1
    C_INSTRUCTION = 2
    L_INSTRUCTION = 3


class Parser:
    def __init__(self, raw_rows=[]):
        self.raw_rows = raw_rows  # assembler read the file and transfer the content to a raw_row list
        self.first_pass_result = []  # filled after first pass. without L-instruction and comments
        self.second_pass_result = []  # filled after second pass
        self.current_instruction = ""
        self.symbol_table = Symbol_table()
        self.code = Code()

    def remove_wAndc(self, s: str) -> str:
        # remove all content after "//" and whitespace by calling strip
        if "//" in s:
            s, _ = s.split("//")
        return s.strip()

    def run_first_pass(self):
        # update the first_pass list for L-instruction
        for row in self.raw_rows:
            self.current_instruction = self.remove_wAndc(row)
            if len(self.current_instruction) == 0:
                continue
            if self.instructionType() != InstructionType.L_INSTRUCTION:
                self.first_pass_result.append(self.current_instruction)
            # update symbol table if L-instruction
            else:
                label_address = len(self.first_pass_result)
                self.symbol_table.add(self.symbol(), label_address)

    def run_second_pass(self):
        # update the binary_rows
        var_address = 15
        for row in self.first_pass_result:
            self.current_instruction = row
            # C instruction
            if self.instructionType() == InstructionType.C_INSTRUCTION:
                self.second_pass_result.append(
                    "111" +
                    self.code.comp(self.comp()) +
                    self.code.dest(self.dest()) +
                    self.code.jump(self.jump())
                )
            elif self.instructionType() == InstructionType.A_INSTRUCTION:
                # A instruction with numbers
                s = self.symbol()
                if s.isdigit():
                    self.second_pass_result.append(self.code.addr(int(s)))
                # A instruction with letters
                else:
                    if self.symbol_table.get(s) is None:
                        var_address += 1
                        self.symbol_table.add(s, var_address)
                    self.second_pass_result.append(self.code.addr(self.symbol_table.get(s)))

    def get_binary_codes(self) -> list:
        return self.second_pass_result

    def instructionType(self) -> InstructionType:
        # check instruction type based on current_instruction
        if "@" in self.current_instruction:
            return InstructionType.A_INSTRUCTION
        elif "(" in self.current_instruction:
            return InstructionType.L_INSTRUCTION
        else:
            return InstructionType.C_INSTRUCTION

    def symbol(self) -> str:
        # extract str from symbols including A instruction and label
        assert self.instructionType() in [InstructionType.L_INSTRUCTION, InstructionType.A_INSTRUCTION]
        if self.current_instruction.startswith("@"):
            symbol_str = self.current_instruction[1:]
        else:
            symbol_str = self.current_instruction[1:-1]
        return symbol_str.strip()

    # separate C instruction into three parts
    def dest(self) -> str:
        assert self.instructionType() == InstructionType.C_INSTRUCTION
        if "=" not in self.current_instruction:
            return "NULL"
        else:
            dest_str, _ = self.current_instruction.split("=")
        return dest_str.strip()

    def comp(self) -> str:
        # use regular expression to extract comp string
        assert self.instructionType() == InstructionType.C_INSTRUCTION
        match = re.search(r"(?:.*=\s*)?([^;]*)(?:\s*;.*)?", self.current_instruction)
        comp_str = match.group(1)
        return comp_str.strip()

    def jump(self) -> str:
        assert self.instructionType() == InstructionType.C_INSTRUCTION
        if ";" not in self.current_instruction:
            return "NULL"
        else:
            _, jump_str = self.current_instruction.split(";")
        return jump_str.strip()
