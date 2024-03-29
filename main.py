import random
import math
import sys

#generate large prime numbers
def prime_generation():
	#change to 1024 or something larger at some point
	num_of_bits = 256
	
	#generate a random large number
	random_prime = random.randrange(2**(num_of_bits-1)+1, 2**(num_of_bits)-1)
	
	return random_prime

#fermats test
def prime_test(n):
	k=5
	
	#initial check
	if n == 1:
		return False

	#fermat test
	for i in range(k):
		a = random.randint(2, n-2)
		if pow(a, n-1, n) != 1:
			return False
	
	#number is prime
	return True

#create public key using phi
def get_public_key(phi):
	pq = (p-1)*(q-1)
	
	#get a random number
	random_num = random.randrange(2, pq)

	#check number with euclid's gcd
	while math.gcd(random_num, pq) != 1:
		random_num = random.randrange(2, pq)

	return random_num

#Extended Euclids
def extended_gcd(a, b):
	if b==0:
		return (1, 0, a)

	(x, y, z) = extended_gcd(b, a%b)

	return y, x-a//b*y, z

#create private key using extended euclids algo
def get_private_key(phi, e):
	x = extended_gcd(e, phi)

	d = x[0]%phi

	return d

#encrypt message
def encrypt_message(message, public_key, pq):
	return pow(encode(message), public_key, pq)

#decrypt message
def decrypt_message(ciphertext, private_key, pq):
	return decode(pow(ciphertext, private_key, pq))

#encode message into a number
def encode(s):
	return int.from_bytes(bytes(s, 'utf-8'), byteorder=sys.byteorder)

#decode message into a string
def decode(n):
    return (n.to_bytes(255, byteorder=sys.byteorder)).decode('utf-8', "ignore")

#generate a signature as a private user
def generate_signature(name, private_key, n):
	return pow(encode(name), private_key, n)

#verify a signature as a public user
def check_signature(signature, public_key, n):
	return decode(pow(int(signature), public_key, n))

##################
#START OF PROGRAM#
##################

#public user key
public_key = None

#private user key
private_key = None

#established n
n = None

#main loop
while True:
	#options
	print("Please select an option: \n	1. Public User\n	2. Private User\n	3. Generate Keys\n	4. Exit\nEnter your choice: ")

	user_exit = int(input())

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
			m = input()
			print(encrypt_message(m, public_key, n))
		#Authenticating a signature
		elif user_operation == 2:
			#check if user has a defined n for their public key
			if n == None:
				print("Please enter n for your public key:")
				try:
					n = int(input())
				#If they input anything other than an int
				except ValueError:
					print("Input Error")
					quit()

			print("Please input the signature:")
			name = input()
			
			#check the signature
			print(check_signature(name, public_key, n))

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
		
		#options
		print("Please select an option: \n	1. Decrypt A Message\n	2. Generate A Digital Signature\nEnter your choice: ")
		user_operation = int(input())

		#Dencrypting a message
		if user_operation == 1:
			#get the cipher text
			print("What is the message?")
			try:
				ciphertext = int(input())
			except ValueError:
				print("Message Error")
				quit()
				
			print(decrypt_message(ciphertext, private_key, n))
		#Creating a signature
		elif user_operation == 2:
			#check if they have an n defined for their private key
			if n == None:
				print("Please enter n for your private key:")
				try:
					n = int(input())
				#If they input anything other than an int
				except ValueError:
					print("Input Error")
					quit()

			print("Please input your signature:")
			name = input()
			
			#generating the signature
			print(generate_signature(name, private_key, n))

	#User wants to generate new keys
	if user_exit == 3:
		p = 1
		q = 1

		while prime_test(p) != True:
			p = prime_generation()

		while prime_test(q) != True:
			q = prime_generation()

		n = p*q
		phi = (p-1)*(q-1)
		
		public_key = get_public_key(phi)

		private_key = get_private_key(phi, public_key)

		#display the keys
		print("Public Key :: ", public_key, "\n")
		print("Private Key :: ", private_key, "\n")
		print("N :: ", n, "\n")

	#User wants to exit the program
	if user_exit == 4:
		quit()