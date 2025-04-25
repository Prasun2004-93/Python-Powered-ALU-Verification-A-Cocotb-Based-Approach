import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_alu(dut):
    print("Running random test cases with carry/borrow verification...")

    for op in range(8):  # Test all 8 operations
        print(f"\nTesting Operation {op}")
        for i in range(10):  # 10 random tests per operation
            A = random.randint(0, 0xFFFF)
            B = random.randint(0, 0xFFFF)
            dut.A.value = A
            dut.B.value = B
            dut.Op.value = op
            await Timer(1, units='ns')  # Wait for combinational logic

            # Calculate expected results
            if op == 0:  # Addition
                full_result = A + B
                expected_Y = full_result & 0xFFFF
                expected_C = 1 if full_result > 0xFFFF else 0
                expected_V = 1 if (A & 0x8000) and (B & 0x8000) and not (expected_Y & 0x8000) or \
                                 not (A & 0x8000) and not (B & 0x8000) and (expected_Y & 0x8000) else 0
            elif op == 1:  # Subtraction
                expected_Y = (A - B) & 0xFFFF
                expected_C = 1 if A < B else 0
                expected_V = 1 if (A & 0x8000) and not (B & 0x8000) and not (expected_Y & 0x8000) or \
                                 not (A & 0x8000) and (B & 0x8000) and (expected_Y & 0x8000) else 0
            elif op == 2:  # AND
                expected_Y = A & B
                expected_C = 0
                expected_V = 0
            elif op == 3:  # OR
                expected_Y = A | B
                expected_C = 0
                expected_V = 0
            elif op == 4:  # XOR
                expected_Y = A ^ B
                expected_C = 0
                expected_V = 0
            elif op == 5:  # NOT
                expected_Y = ~A & 0xFFFF
                expected_C = 0
                expected_V = 0
            elif op == 6:  # Left Shift
                expected_Y = (A << 1) & 0xFFFF
                expected_C = 1 if A & 0x8000 else 0
                expected_V = 0
            elif op == 7:  # Arithmetic Right Shift
                expected_Y = (A >> 1) | (A & 0x8000)  # Sign extension
                expected_C = A & 0x0001
                expected_V = 0

            # Expected N and Z flags
            expected_N = 1 if expected_Y & 0x8000 else 0
            expected_Z = 1 if expected_Y == 0 else 0

            # Verify results
            assert dut.Y.value == expected_Y, f"Op {op}, Test {i}: Expected Y={hex(expected_Y)}, got {hex(dut.Y.value)} (A={hex(A)}, B={hex(B)})"
            assert dut.C.value == expected_C, f"Op {op}, Test {i}: Expected C={expected_C}, got {dut.C.value} (A={hex(A)}, B={hex(B)})"
            assert dut.V.value == expected_V, f"Op {op}, Test {i}: Expected V={expected_V}, got {dut.V.value} (A={hex(A)}, B={hex(B)})"
            assert dut.N.value == expected_N, f"Op {op}, Test {i}: Expected N={expected_N}, got {dut.N.value} (A={hex(A)}, B={hex(B)})"
            assert dut.Z.value == expected_Z, f"Op {op}, Test {i}: Expected Z={expected_Z}, got {dut.Z.value} (A={hex(A)}, B={hex(B)})"

            # Highlight carry generation
            if dut.C.value == 1:
                print(f"Op {op}, Test {i}: Carry/Borrow generated (C=1), A={hex(A)}, B={hex(B)}, Y={hex(dut.Y.value)}")

    print("\nAll random tests passed successfully!")
