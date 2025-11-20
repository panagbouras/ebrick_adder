// Copyright (c) 2024 Zero ASIC Corporation
// This code is licensed under Apache License 2.0 (see LICENSE for details)

// Simple RISC-V program that prints a message and exits

#include "ebrick_memory_map.h"

static inline void puts(char* str) {
	// in this example, the "UART" is simply a memory address where
	// characters are written. each character is transmitted in a
	// UMI packet that is received by the Python stimulus code

	char* s = str;
	char c;
	while ((c = *s++)) {
		*((volatile int*)UART_ADDR) = c;
	}
	*((volatile int*)UART_ADDR) = '\n';
}

int main() {
	// print a message
    puts("Hello World!");
	
	// The adder sequence starts here. The values a and b will be sent to the
	// adder. If the  expected result is receiver the connection works.
	unsigned int a = 1;
	unsigned int b = 1;
	unsigned int expected = 2; // For 1+1, HLS adder gives {carry=1, sum=0} -> 2
	unsigned int result;


	// Write operands
	*((volatile unsigned int*)ADDR_IN_A) = a;
	*((volatile unsigned int*)ADDR_IN_B) = b;

	// Start the adder
	*((volatile unsigned int*)ADDR_AP_CTRL) = 0x1;

	// Read the result
	result = *((volatile unsigned int*)ADDR_OUT_C);

    if (result == expected) {
        return 0; // Return 0 for PASS
    } else {
        return 1; // Return 1 for FAIL
    }
}
