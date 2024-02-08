import random
import math
import sys

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

def encrypt_message(message, public_key, pq):
	return pow(message, public_key, pq)

def decrypt_message(ciphertext, private_key, pq):
	return pow(ciphertext, private_key, pq)

def encode(s):
	return int.from_bytes(bytes(s, 'utf-8'), byteorder=sys.byteorder)

def decode(n):
    return (n.to_bytes(255, byteorder=sys.byteorder)).decode('utf-8', "ignore")

##################
#START OF PROGRAM#
##################

p = 1
q = 1

while prime_test(p) != True:
	p = prime_generation()

while prime_test(q) != True:
	q = prime_generation()

n = p*q
phi = (p-1)*(q-1)

#public user key
public_key = None

#private user key
private_key = None

while True:
	print("Please select an option: \n	1. Public User\n	2. Private User\n	3. Generate Keys\nEnter your choice: ")

	user_exit = int(input())
	'''
	#User failed to input an allowed option
	if user_exit != 1 and user_exit != 2 and user_exit != 3:
		print("Please select an option: \n	1. Public User\n	2. Private User\n	3. Generate Keys\nEnter your choice: ")

		user_exit = int(input())
	'''
	#Public Key User
	if user_exit == 1:
		#if they dont already have a defined key
		if public_key == None:
			print("Please enter your public key:")
			try:
				public_key = int(input())
			#If they input anything other than an int
			except ValueError:
				print("Key Error")
				quit()

		#options
		print("Please select an option: \n	1. Encrypt A Message\n	2. Authenticate A Digital Signature\nEnter your choice: ")
		user_operation = int(input())

		#Encrypting a message
		if user_operation == 1:
			print("What is your message?")
			m = encode(input())
			print(encrypt_message(m, public_key, n))
		#Authenticating a signature
		elif user_operation == 2:
			print("lullllllllllllll")

	#Private Key User
	if user_exit == 2:
		#if they dont already have a defined key
		if private_key == None:
			print("Please enter your private key:")
			try:
				private_key = int(input())
			#If they input anything other than an int
			except ValueError:
				print("Key Error")
				quit()
		
		print("Please select an option: \n	1. Decrypt A Message\n	2. Sign A Digital Signature\n	3. Show The Keys\nEnter your choice: ")
		user_operation = int(input())

		#Dencrypting a message
		if user_operation == 1:
			print("What is the message?")
			ciphertext = int(input())
			print(decode(decrypt_message(ciphertext, private_key, n)))
		#Authenticating a signature
		elif user_operation == 2:
			print("lullllllllllllll")

	#User wants to generate new keys
	if user_exit == 3:
		public_key = get_public_key(phi)

		private_key = get_private_key(phi, public_key)

		print("Public Key :: ", public_key, "\n")
		print("Private Key :: ", private_key, "\n")