# pwnable.kr -- Rookiss -- crypto1

## 1. Challenge

> We have isolated the authentication procedure to another box using RPC.  
> The credential information between RPC is encrypted with AES-CBC, so it will be secure enough from sniffing.  
> I believe no one can login as admin but me :p  
>   
> Download : http://pwnable.kr/bin/client.py  
> Download : http://pwnable.kr/bin/server.py  
>   
> Running at : nc pwnable.kr 9006  

## 2. Solution

Download `client.py`:

```python
#!/usr/bin/python
from Crypto.Cipher import AES
import base64
import os, sys
import xmlrpclib
rpc = xmlrpclib.ServerProxy("http://localhost:9100/")

BLOCK_SIZE = 16
PADDING = '\x00'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: c.encrypt(pad(s)).encode('hex')
DecodeAES = lambda c, e: c.decrypt(e.decode('hex'))

# server's secrets
key = 'erased. but there is something on the real source code'
iv = 'erased. but there is something on the real source code'
cookie = 'erased. but there is something on the real source code'

# guest / 8b465d23cb778d3636bf6c4c5e30d031675fd95cec7afea497d36146783fd3a1
def sanitize(arg):
	for c in arg:
		if c not in '1234567890abcdefghijklmnopqrstuvwxyz-_':
			return False
	return True

def AES128_CBC(msg):
	cipher = AES.new(key, AES.MODE_CBC, iv)
	return EncodeAES(cipher, msg)

def request_auth(id, pw):
	packet = '{0}-{1}-{2}'.format(id, pw, cookie)
	e_packet = AES128_CBC(packet)
	print 'sending encrypted data ({0})'.format(e_packet)
	sys.stdout.flush()
	return rpc.authenticate(e_packet)

if __name__ == '__main__':
	print '---------------------------------------------------'
	print '-       PWNABLE.KR secure RPC login system        -'
	print '---------------------------------------------------'
	print ''
	print 'Input your ID'
	sys.stdout.flush()
	id = raw_input()
	print 'Input your PW'
	sys.stdout.flush()
	pw = raw_input()

	if sanitize(id) == False or sanitize(pw) == False:
		print 'format error'
		sys.stdout.flush()
		os._exit(0)

	cred = request_auth(id, pw)

	if cred==0 :
		print 'you are not authenticated user'
		sys.stdout.flush()
		os._exit(0)
	if cred==1 :
		print 'hi guest, login as admin'
		sys.stdout.flush()
		os._exit(0)

	print 'hi admin, here is your flag'
	print open('flag').read()
	sys.stdout.flush()

```

You can see that `client.py` just joins `id`, `pw` and `cookie` with `"-"` and encrypts the joined string with AES-CBC, then sends the ciphertext to `server.py` by RPC. Before sending ciphertext, `client.py` will show the ciphertext to you, which may leak `cookie`.

The first thing we should do is finding out the length of `cookie`. As there is padding, which looks like PKCS5 padding, during the process of encryption, we can try to build many messages that the lengths of are increasing by sending different `id`s and `pw`s.

For example, I sent empty `id` and `pw`. The remote returned a ciphertext

```
---------------------------------------------------
-       PWNABLE.KR secure RPC login system        -
---------------------------------------------------

Input your ID

Input your PW

sending encrypted data (6242e07a0ab2a3f24e922635da556f9267e18342bf8fd63d1dc783fcdde09abc6368a50b0ca6b383d04c77cd7fb44cf1720197ad4c8d45a3175761e37951e00b)
```

which is 64 bytes long. So the length of `cookie` should vary from `64 - 16 - 2 = 46` to `64 - 1 - 2 = 61` where `2` is for 2 join chars `"-"`. Then I sent empty `id` and one char `"-"` as `pw`. The remote returned

```
---------------------------------------------------
-       PWNABLE.KR secure RPC login system        -
---------------------------------------------------

Input your ID

Input your PW
-
sending encrypted data (2d46c1d48d5566429b5d7ba6514d6a3b9d799be938049bfe1e89a0cdfb8b64ca3244b1b6abdd2d578bdf667047c3dcb5ca93ae378594a4dad3528aa51f535129)
```

where the length of the ciphertext is still 64 bytes. Later I tried many times with empty `id` and increasing `pw`. Finally  I got a ciphertext with 80 bytes when I sent empty `id` and `-------------`, 13 chars, as `pw`. 

So there must be

```
13 + 2 + len(cookie) + 16 = 80
len(cookie) = 49
```

After that we can leak `cookie` one by one:

1. Let `id` be empty and `pw` be `"-------------------------------------------------------------"`, 61 chars long.

   So the first 64 chars of the joined message would be

   ```
   ---------------------------------------------------------------X
   ```

   where `"X"` is the first char of `cookie`. 

2. Send `id` and `pw` and you will get a ciphertext `CX`.

3. Let `id` be empty and `pw` be `--------------------------------------------------------------Y`, 63 chars long.

   So the first 64 chars of the joined message would be

   ```
   ---------------------------------------------------------------Y
   ```

4. Send `id` and `pw` and you will get a ciphertext `CY`.

5. If the first 64 bytes of `CX` is the same with the first 64 bytes of `CY`, we can know that the char you guess, `Y`, matches `X`.

Repeat and you will get the whole `cookie`:

```python
cookie = 'you_will_never_guess_this_sugar_honey_salt_cookie'
```

Now calculate `pw` and use it to get flag.

```python
import hashlib
id = 'admin'
cookie = 'you_will_never_guess_this_sugar_honey_salt_cookie'
pw = hashlib.sha256((id + cookie).encode()).hexdigest()
print(pw)
# Output:
# fcf00f6fc7f66ffcfec02eaf69d30398b773fa9b2bc398f960784d60048cc503
```

```
---------------------------------------------------
-       PWNABLE.KR secure RPC login system        -
---------------------------------------------------

Input your ID
admin
Input your PW
fcf00f6fc7f66ffcfec02eaf69d30398b773fa9b2bc398f960784d60048cc503
sending encrypted data (05c4ccfd4880c92339b995c7754ec2e6567f2ed91d955cb7144c1b6037855db1b3a8525e74d30fd4505bb38c975b86f23d0e5aa23eed44b9beaa7e2195da93ba53cb08758a261ada5612245f49d25b81aa5a297aa5d555886073b17e2ed719b3607da6fbfe40b260a45485910404d69c818a2faedac7bb3a727cfbb53eab8406)
hi admin, here is your flag
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

