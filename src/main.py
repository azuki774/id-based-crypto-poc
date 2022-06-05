from pycocks.cocks.cocks import CocksPKG, Cocks
import pickle

cocks_pkg = CocksPKG()  # Optional param.: bit size (default = 2048)

# Extract private key, r, from an identity string; a transformed
# ID string, a, is also returned, which is required for encryption
# and decryption.
r, a = cocks_pkg.extract("User1")

cocks = Cocks(cocks_pkg.n)  # Must use same public modulus, n, from cocks_pkg
c = cocks.encrypt(b"test", a)

msg = cocks.decrypt(c, r, a)  # => b"test"
print(a)
