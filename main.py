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

#lists for storing encryption and lengths
encrypt_list = list()
lenlist = list()

#lists for storing signatures and the message
name_list = list()
signature_list = list()

#generating keys before running main loop
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

print("\nRSA keys have been generated.")

#main loop
while True:

    print("Please select user type: \n	1. Public User\n	2. The owner of the keys\n	3. Exit program\n\nEnter your choice: ")
    user_exit = int(input())

	#Public Key User
    if user_exit == 1:
        while True:
            print("As a public user, what would you like to do? \n	1. Encrypt A Message\n	2. Authenticate A Digital Signature\n	3. Exit\n\nEnter your choice: ")
            user_operation = int(input())

    		#Encrypting a message
            if user_operation == 1:
                print("\nEnter a message: ")
                m = input()
                lenlist.append(len(m))
                encrypt_list.append(encrypt_message(m, public_key, n))
                print("\nMessage was encrypted and sent.\n")
                
            #Authenticating a signature
            elif user_operation == 2:
                
                #Check if theres a signature
                if not signature_list:
                    print("\nThere are no signature to authenticate.\n")
                
                else:
                    print("The following messages are available:")
                    index_two = 0
                    for x in name_list:
                        index_two += 1
                        print("	" + str(index_two) + ". " + str(x))
                    
                    print("Enter your choice: ")
                    user_operation = int(input())
            
                    #checks if signature is valid
                    y = str(name_list[user_operation - 1])
                    z = str(check_signature(signature_list[user_operation - 1], public_key, n))
            
                    index_three = 0
                    for x in y:
                        if(x != z[index_three]):
                            b = False
                        else:
                            b = True
                        index_three += 1
                
                    if(b):
                        print("\nSignature is valid.\n")
                    else:
                        print("\nSignature is not valid.\n")
                        
            elif user_operation == 3:
                break
                
            

	#Private Key User
    if user_exit == 2:
        while True:
            print("As the owner of the keys, what would you like to do? \n	1. Decrypt A Message\n	2. Digitally sign a message\n	3. Show the keys\n	4. Generate a new set of keys\n	5. Exit\n\nEnter your choice: ")
            user_operation = int(input())
        
    		#Dencrypting a message
            if user_operation == 1:
            
                #get the cipher text
                print("The following messages are available:")
                index = 0;
                for x in lenlist:
                    index += 1
                    print("	" + str(index) + ". length = " + str(x))
                
                print("Enter your choice: ")
                try:
                    ciphertext = encrypt_list[int(input())-1]
                except ValueError:
                    print("Message Error")
                    quit()
				
                print("Decrypted message: " + str(decrypt_message(ciphertext, private_key, n)))
                
            #Creating a signature
            elif user_operation == 2:
			
                print("Enter a message:")
                name = input()
			
                #generating the signature
                name_list.append(name)
                signature_list.append(generate_signature(name, private_key, n))
                print("\nMessage signed and sent.\n")
            
            #Show keys
            elif user_operation == 3:
                print("\nPublic Key: " + str(public_key))
                print("\nPrivate Key: " + str(private_key) + "\n")
            
            #Generate new keys
            elif user_operation == 4:
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
            
            #Exit
            elif user_operation == 5:
                break

	#User wants to exit the program
    if user_exit == 3:
        print("Bye for now!")
        break