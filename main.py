import random
import math

def prime_generation():
	num_of_bits = 256
	
	random_prime = random.randrange(2**(num_of_bits-1)+1, 2**(num_of_bits)-1)
	
	return random_prime

#fermats test
def prime_test(n):
	k=5
	
	if n == 1 or n == 4:
		return False
	if n == 2 or n == 3:
		return True

	for i in range(k):
		a = random.randint(2, n-2)
		if pow(a, n-1, n) != 1:
			return False
	
	return True

def get_public_key(phi):
	pq = (p-1)*(q-1)
	
	random_num = random.randrange(2, pq)

	while math.gcd(random_num, pq) != 1:
		random_num = random.randrange(2, pq)

	return random_num

#Extended Euclids
def extended_gcd(a, b):
	if b==0:
		return (1, 0, a)

	(x, y, z) = extended_gcd(b, a%b)

	return y, x-a//b*y, z

def get_private_key(phi, e):
	x = extended_gcd(e, phi)

	d = x[0]%phi

	return d

##################
#START OF PROGRAM#
##################

p = 1
q = 1

while prime_test(p) != True:
	p = prime_generation()

while prime_test(q) != True:
	q = prime_generation()

phi = (p-1)*(q-1)

e = get_public_key(phi)

d = get_private_key(phi, e)

print("Public key :: ", e, "\n")
print("Private key :: ", d, "\n")

print("Public key(1) or Private key(2) user?")

user_operation = int(input())

while user_operation != 1 and user_operation != 2:
	print("Public key(1) or Private key(2) user?")

	user_operation = int(input())

while user_operation == 1:
	#Public Key User
	print("Encrypt(1) or Authenticate Signature(2)?")

while user_operation == 2:
	#Private Key User
	print("Decrypt(1) or Generate Signature(2)")

print("here")