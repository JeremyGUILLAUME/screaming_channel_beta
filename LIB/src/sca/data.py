from Crypto.Cipher import AES
from os import path
from Crypto.Random import get_random_bytes



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
    return plaintexts, key 



def create_random_data(num_points):
	plaintexts = list()
    
	for i in range(num_points):
		p = get_random_bytes(16)
		plaintexts.append([p[i] for i in range(16)])
        
	k = get_random_bytes(16)
	key = [k[i] for i in range(16)]
	return plaintexts, key



def save_data(data_path, plaintexts, key):
	# Save PLAINTEXT
	with open(path.join(data_path, 'plaintexts.txt'), 'w') as f:
		#f.write('\n'.join(str(bytearray(p)).encode('hex') for p in plaintexts))
		f.write('\n'.join(bytes(p).hex() for p in plaintexts))
	# Save KEY
	with open(path.join(data_path, 'key.txt'), 'w') as f:
		#f.write(''.join(str(bytearray(key)).encode('hex')))
		f.write(''.join(bytes(key).hex()))
