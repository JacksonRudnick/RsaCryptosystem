import random

def prime_generation():
    num_of_bits = 2048
    
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

#Euclids gcd
def find_relative_prime():
    
    return

#Extended Euclids
def find_multiplicative_inverse():
    
    return

first_prime = 1
second_prime = 1

while prime_test(first_prime) != True:
    first_prime = prime_generation()

while prime_test(second_prime) != True:
    second_prime = prime_generation()

print(first_prime)
print(second_prime)