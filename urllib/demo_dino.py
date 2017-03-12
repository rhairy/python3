"""
Retrieve password from DinoPass.com and print it to the console.
"""
import urllib.request

response = urllib.request.urlopen('http://dinopass.com/password/simple')

password = response.readline()
print(password.decode())
