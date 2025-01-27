accepted_letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'å', 'ä', 'ö'}
dic_l2n = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 
'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, 'å': 26, 'ä': 27, 'ö': 28} 
dic_n2l = {value: key for key, value in dic_l2n.items()} 

def main(filename):
###################################################################
# Open the input, put it to lowercase, keep only the accepted letters (Swedish alphabet)
  try:
    with open('input.txt', 'r') as file:
      content = file.read()
      content = content.lower()
      plaintext = ""
      for i in range(0, len(content)):
        if content[i] in accepted_letters:
          plaintext += content[i]
  except FileNotFoundError:
    print(f"Error: File input.txt not found.")
    return None
  try:
    with open('vig-group2.plain', 'w') as file:
      file.write(plaintext)
      print(f"Content written successfully to vig-group2.plain.")
  except IOError as e:
    print(f"An error occurred while writing to the file vig-group2.plain")
#################################################################################
# Correcting the length of the sanitized text
  length = len(plaintext)
  while (length<200 or length>600):
    if (length<200):
      print(f"Len: {length}, input text is too short, making it longer")
      plaintext = plaintext+plaintext
    if(length>600):
      print(f"Len: {length}, input text is too long, making it shorter")
      plaintext=plaintext[:599] # shorten text if too long
    length= len(plaintext)
  
#####################################################################
# Iterate over the key and put it in parallel with each letter of the text to generate to 
# the encrypted numerical value. Convert it to text and add to result. ²
  res =""
  try:
    with open('vig-group2.key', 'r') as file:
      key = file.read()
      key = key.rstrip('\n')
  except FileNotFoundError:
    print(f"Error: File vig-group2.key not found.")
  c=0 #counter to iterate on the key
  for i in range(0,length):
    gen_value = (dic_l2n[plaintext[i]] + dic_l2n[key[c]]) % 29
    gen_letter = dic_n2l[gen_value]
    res += gen_letter
    c=(c+1)%(len(key))
  print(res)

#########################################################################
# Write the result in the file 
  try:
    with open('vig-group2.crypto', 'w') as file:
      file.write(res)
      print(f"Content written successfully to vig-group2.crypto.")
  except IOError as e:
    print(f"An error occurred while writing to the file vig-group2.crypto")

if __name__ == "__main__":
  main("input.txt")
