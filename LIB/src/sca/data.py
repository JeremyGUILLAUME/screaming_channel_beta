from Crypto.Cipher import AES
import os
from os import path, system
from Crypto.Random import get_random_bytes

def create_data(data_type, num_points, data_path):
    if data_type[0] in ["S", "s"]:   #Static Data
        plaintexts, keys = create_static_data(num_points)
    elif data_type[0] in ["R", "r"]: #Random Data
        plaintexts, keys = create_random_data(num_points)
    elif data_type[0] in ["A", "a"]: #Active Data
        plaintexts, keys = create_active_data(num_points)
    save_data(data_path, plaintexts, keys)
    return plaintexts, keys

"""
def create_static_data(num_points):
    # Static PLAINTEXT
    plaintexts = list()
    #kgen= '123456789abcdef123456789abcde0f0'
    kgen= '123456789abcdef123456789abcde0f0'.decode('hex')
    aes_p = AES.new(kgen, 1)
    #p = '00000000000000000000000000000000'
    p = '00000000000000000000000000000000'.decode('hex')
    for i in range(num_points):
        #plaintexts.append(p.decode('hex'))
        plaintexts.append( [ord(p[i]) for i in range(len(p))] )
        p = (aes_p.encrypt(p))  #.encode('hex')[0:32] 
    # Static KEY
    #keys = list()
    #k = '0123456789abcdef123456789abcdef0'
    #keys.append(k.decode('hex'))
    k = '0123456789abcdef123456789abcdef0'.decode('hex')
    key = [ord(k[i]) for i in range(len(k))]
    return plaintexts, key #keys
"""
    
def create_static_data(num_points):
    plaintexts = list()
    
    kgen = '123456789abcdef123456789abcde0f0'
    kgen = bytes.fromhex(kgen)
    aes_p = AES.new(kgen, 1)
    
    p = bytes(16)
    for i in range(num_points):
        plaintexts.append([p[i] for i in range(16)])
        p = (aes_p.encrypt(p))
        
    k = bytes.fromhex('0123456789abcdef123456789abcdef0')
    key = [k[i] for i in range(16)]
    return plaintexts, key #keys
    
"""
def create_random_data(num_points):
    # Random PLAINTEXT
    plaintexts = list()
    for i in range(num_points):
        p = os.urandom(16)
        #plaintexts.append(p)
        plaintexts.append( [ord(p[i]) for i in range(len(p))] )
    # Random KEY
    #keys = list()
    k = os.urandom(16)
    #keys.append(k)
    key = [ord(k[i]) for i in range(len(k))]
    return plaintexts, key #keys
"""
    
def create_random_data(num_points):
	plaintexts = list()
    
	for i in range(num_points):
		p = get_random_bytes(16)
		plaintexts.append([p[i] for i in range(16)])
        
	k = get_random_bytes(16)
	key = [k[i] for i in range(16)]
	return plaintexts, key #keys
    

def create_active_data(num_points):
    # Active PLAINTEXT
    plaintexts = list()
    for i in range(num_points):
        value = i%256
        if value < 16:
            v = "0%s"%hex(value)[2]
        else:
            v = "%s"%hex(value)[2:4]

        p = ""
        for j in range(16):
            p += v
        plaintexts.append(p.decode('hex'))

    # Static KEY
    keys = list()
    k = '0123456789abcdef123456789abcdef0'
    keys.append(k.decode('hex'))
    return plaintexts, keys

def save_data(data_path, plaintexts, key):
	# Save PLAINTEXT
	with open(path.join(data_path, 'pt_.txt'), 'w') as f:
		#f.write('\n'.join(str(bytearray(p)).encode('hex') for p in plaintexts))
		f.write('\n'.join(bytes(p).hex() for p in plaintexts))
	# Save KEY
	with open(path.join(data_path, 'key_.txt'), 'w') as f:
		#f.write(''.join(str(bytearray(key)).encode('hex')))
		f.write(''.join(bytes(key).hex()))

"""
def save_data(data_path, plaintexts, key):
    # Save PLAINTEXT
    with open(path.join(data_path, 'pt_.txt'), 'w') as f:
        f.write('\n'.join(p.encode('hex') for p in plaintexts))
    # Save KEY
    with open(path.join(data_path, 'key_.txt'), 'w') as f:
        f.write('\n'.join(key.encode('hex')))
"""

"""
def save_data(data_path, plaintexts, keys):
    # Save PLAINTEXT
    with open(path.join(data_path, 'pt_.txt'), 'w') as f:
        f.write('\n'.join(p.encode('hex') for p in plaintexts))
    # Save KEY
    with open(path.join(data_path, 'key_.txt'), 'w') as f:
        f.write('\n'.join(k.encode('hex') for k in keys))
"""





 
