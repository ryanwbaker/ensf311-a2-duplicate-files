import random # needed for create_table()
import hashlib # provides md5 (and othr crypto hash functions)

def string_hash(message, prime_number=31, modulo_value=256): 
    """ implementation of string hashing
    https://en.wikipedia.org/wiki/Universal_hashing#Hashing_strings

    message (bytes): message to be hashed
    prime_number (int): a special prime, e.g. 31
    modulo_value (int): modulo divisor, e.g 256 for 8bit hash

    returns: (str) hash as hex formated string
    """
    hash_value = 0
    for c in message:
        hash_value = ((hash_value * prime_number) + c) % modulo_value
    return "{:08x}".format(hash_value)  


def create_table(seed=55):
    """Creates a list of 256 random values for Pearson hashing.

    Adapted from Python code found here:
    https://en.wikipedia.org/wiki/Pearson_hashing

    seed: (int) seed for random number generator
    returns: (list) table of numbers 0-255 in random order
    """
    # set seed for reproducible results
    random.seed(seed)

    table = list(range(0, 256))
    random.shuffle(table)
    
    return table

def hash8(message, table=create_table()):
    """Pearson hashing, 8bit.

    Adapted from Python code found here:
    https://en.wikipedia.org/wiki/Pearson_hashing

    message: (bytes) message to be hashed
    table: (list) output of create_table()

    returns: (str) hash as hex formated string
    """
    # initialize with length of message, modulo to keep it 8bit
    hash_val = len(message) % 256
    for i in message:
        idx = hash_val ^ i # find table index XOR hash with byte
        hash_val = table[idx] # new hash is table entry
    # return int as hex formated string
    return "{:02x}".format(hash_val) 

def hash64(message, table=create_table()):
    """Pearson hashing, 64bit.
    To get 64 bit hash, we perform 8x 8bit hash in parallel

    Adapted from C code found here:
    https://en.wikipedia.org/wiki/Pearson_hashing

    message: (bytes) message to be hashed
    table: (list) output of create_table()

    returns: (str) hash as hex formated string
    """
    # Initialize 8x 8bit (int) list
    hash_blocks = [0]*8
    for j in range(len(hash_blocks)):
        # initialize hash with table value of first byte
        # add parallel-index so 8 hashes are different
        # modulo to keep it 8bit
        hash_val = table[message[0] + j % 256]
        # start loop at second byte
        for i in range(1, len(message)):
            idx = hash_val ^ message[i] # find table index XOR hash with byte
            hash_val = table[idx] # new hash is table entry
        hash_blocks[j] = hash_val
    # convert 8x 8bit list to hex string
    hash_str = ["{:02x}".format(i) for i in hash_blocks]
    hash_str = ''.join(hash_str)
    return hash_str

def hashfnv32a(message):
    """ 32bit FNV-1a hash
    Reference: 
    https://en.wikipedia.org/wiki/Fowler–Noll–Vo_hash_function

    Adapted from Python code found here:
    https://stackoverflow.com/questions/55482460/calculate-fnv1a32-hash-of-hex-string-in-python

    message: (bytes) message to be hashed
    
    returns: (str) hash as hex formated string
    """

    hash_val = 0x811c9dc5 # base value
    fnv_32_prime = 0x01000193 # a 'special' prime
    uint32_max = 0x100000000 # mask computation to keep it 32bit
    for i in message:
        # XOR hash and message byte
        hash_val = hash_val ^ i 
        # multiply hash with prime, keep it 32bit with modulo
        hash_val = (hash_val * fnv_32_prime) % uint32_max  
    # fromat as 8-point hex string (4bit per hex = 32bit)
    return "{:08x}".format(hash_val) 

def hashmd5(message):
    """Wrapper for hashlib.md5()

    message: (bytes) message to be hashed

    returns: (str) md5 hexdigest
    """
    return hashlib.md5(message).hexdigest()

#TODO: add wrappers for other hashlib functions: SHA-1, SHA-256


if __name__ == '__main__':

    # Pearson hash functions need a pseudo-random table
    t = create_table()

    # test and test_copy are identical, test2 has one character different
    # sines is a binary file
    #TODO: add expected hashes and turn this into a test.
    files = ['files/test.txt', 
            'files/test_copy.txt', 
            'files/test2.txt', 
            'files/sines.pdf']

    for f in files:
        fin = open(f, 'rb')

        message = fin.read()
        h8 = hash8(message, t)
        h64 = hash64(message, t)
        fnv32a = hashfnv32a(message)
        md5 = hashmd5(message)

        print(f)
        print(f"\tPearson hash   8bit {h8}")
        print(f"\tFNV hash      32bit {fnv32a}")
        print(f"\tPearson hash  64bit {h64}")
        print(f"\tMD5 hash     128bit {md5}")

    """Prints
    files/test.txt
        Pearson hash   8bit 98
        FNV hash      32bit eafeb157
        Pearson hash  64bit bec2110a5c4c1972
        MD5 hash     128bit 03dd3df7ab2e7ed8b9e9ad448908931b
    files/test_copy.txt
        Pearson hash   8bit 98
        FNV hash      32bit eafeb157
        Pearson hash  64bit bec2110a5c4c1972
        MD5 hash     128bit 03dd3df7ab2e7ed8b9e9ad448908931b
    files/test2.txt
        Pearson hash   8bit a2
        FNV hash      32bit 7da2aab7
        Pearson hash  64bit cfaf9790f6d7c343
        MD5 hash     128bit bf3e728b9216bb1b1c20aa0855fee71f
    files/sines.pdf
        Pearson hash   8bit 07
        FNV hash      32bit fa93885d
        Pearson hash  64bit b49272d865f55047
        MD5 hash     128bit d85bfea73e319ffc923975362f84c94a
    """


    # check fnv32a with https://www.pelock.com/products/hash-calculator
    # i'Hello' should be F55C314B -> OK
    # print(f"FNV of Hello is {hashfnv32a('Hello'.encode())}")