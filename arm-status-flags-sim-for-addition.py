"""
CEC 320
Dr. Jianhua Liu
A program that simulates signed and unsigned n-bit addition and ARM status flag updates
Created by Zachary Donaldson for testing purposes only.
4/9/2024
"""

def BIN(dec, n_bits):  # Converts given decimal number to n-bit binary number stored as an array

	mag = abs(dec)

	bin_num = [int(0)] * n_bits

	for n in range(len(bin_num)):
		if mag >= pow(2, len(bin_num)-(n+1)):
			bin_num[n] = int(1)
			mag -= pow(2, len(bin_num)-(n+1))

	if dec < 0:
		bin_num = negate_bin(bin_num)

	return bin_num


def to_bin(arr):  # Converts given binary array to an actual binary number for printing purposes
	str = "0b"
	for n in arr:
		str += "{}".format(n)

	return str

def dec(arr):  # Converts given binary array back to a decimal number
	num = 0
	for i in range(len(arr)):
		n = (len(arr)-1) - i
		num += arr[i] * pow(2,n)

	return num


def negate_bin(arr):  # I don't remember what this does. All I know is that it works.

	new = arr
	for i in range(len(new)):
		new[i] = 0 if new[i] == 1 else 1

	n_bits = len(new)


	one = BIN(1, n_bits)
	carry_row = BIN(0, n_bits + 1)
	result = BIN(0, n_bits)

	for i in range(n_bits):
		n = (n_bits - 1) - i
		if arr[n] + one[n] + carry_row[n] == 1:
			result[n] = 1
		elif arr[n] + one[n] + carry_row[n] > 1:
			carry_row[n - 1] = 1
			if arr[n] + one[n] + carry_row[n] > 2:
				result[n] = 1
	return result


def addition(R0, R1, n_bits):  # This function is used by both add() and adds()
	x = R0
	y = R1

	if x < 0:
		x += pow(2, n_bits)
	if y < 0:
		y += pow(2, n_bits)

	bin_x = BIN(x, n_bits)
	bin_y = BIN(y, n_bits)

	carry_row = BIN(0, n_bits + 1)
	result = BIN(0, n_bits)

	for i in range(n_bits):
		n = (n_bits - 1) - i
		if bin_x[n] + bin_y[n] + carry_row[n + 1] == 1:
			result[n] = 1
		elif bin_x[n] + bin_y[n] + carry_row[n + 1] > 1:
			carry_row[n] = 1
			if bin_x[n] + bin_y[n] + carry_row[n + 1] > 2:
				result[n] = 1

	return result, carry_row, bin_x, bin_y


def adds(R0, R1, n_bits):  # addition for signed numbers

	result, carry_row, bin_x, bin_y = addition(R0, R1, n_bits)

	V = (carry_row[0] & 0b1) | (result[0] ^ (bin_x[0] | bin_y[0]))
	deci = dec(result) if result[0] == 0 else 0 - dec(negate_bin(result))
	N = 1 if deci < 0 else 0

	return result, deci, V, N


def add(R0, R1, n_bits):  # addition for unsigned numbers

	result, carry_row, bin_x, bin_y = addition(R0, R1, n_bits)

	C = carry_row[0]
	deci = dec(result)
	Z = 1 if deci==0 else 0

	return result, deci, C, Z


##################################################
"""change these vars as needed"""
n_bits = 5  # number of bits per number
d1 = 11  # first number
d2 = -18  # second number
##################################################


b1 = BIN(d1, n_bits)
b2 = BIN(d2, n_bits)

result1, deci1, C, Z = add(d1,d2,n_bits)  # results of unsigned addition
result2, deci2, V, N = adds(d1,d2,n_bits)  # results of signed addition

# Magic Printy Stuff
print("{} = {}".format(d1, to_bin(b1)))
print("{} = {}".format(d2, to_bin(b2)))

print("\n{} + {}".format(d1, d2))
print("{}\n{}\n--------\n{}".format(to_bin(b1), to_bin(b2), to_bin(result1)))

print("\nUnsigned: {} | C={}, Z={}".format(deci1, C, Z))
print("  Signed: {} | V={}, N={}".format(deci2, V, N))

