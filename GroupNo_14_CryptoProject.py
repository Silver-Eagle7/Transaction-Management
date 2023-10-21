#importing required libraries
import hashlib
import datetime
import random
import time
import sqlite3

GENERATOR = 4
PRIME = 1101

def hex2bin(s):
    mp = {'0' : "0000", 
          '1' : "0001",
          '2' : "0010", 
          '3' : "0011",
          '4' : "0100",
          '5' : "0101", 
          '6' : "0110",
          '7' : "0111", 
          '8' : "1000",
          '9' : "1001", 
          'A' : "1010",
          'B' : "1011", 
          'C' : "1100",
          'D' : "1101", 
          'E' : "1110",
          'F' : "1111" }
    bin = ""
    i=0
    while i in range(len(s)):
        bin = bin + mp[s[i]]
        i = i+1
    return bin
      
# Binary to hexadecimal conversion
def bin2hex(s):
    mp = {"0000" : '0', 
          "0001" : '1',
          "0010" : '2', 
          "0011" : '3',
          "0100" : '4',
          "0101" : '5', 
          "0110" : '6',
          "0111" : '7', 
          "1000" : '8',
          "1001" : '9', 
          "1010" : 'A',
          "1011" : 'B', 
          "1100" : 'C',
          "1101" : 'D', 
          "1110" : 'E',
          "1111" : 'F' }
    hex = ""
    i=0
    while i in range(0,len(s)):
        ch=""
        for j in range(0,4):
            ch = ch + s[i+j]
        hex = hex + mp[ch]
        i=i+4
          
    return hex
  
# Binary to decimal conversion
def bin2dec(binary): 
        
    binary1 = binary 
    decimal, i, n = 0, 0, 0
    while(binary != 0): 
        ten = 10
        dec = binary % ten
        two = 2
        decimal += dec * pow(two, i) 
        binary = binary//10
        i = i + 1
    return decimal
  
# Decimal to binary conversion
def dec2bin(num):
    x = num 
    res = bin(num).replace("0b", "")
    if(len(res)%4 != 0):
        t=4
        l=1
        temp = len(res)
        div = temp
        div = div / t
        div = int(div)
        counter =(t * (div + l)) 
        counter = counter - temp
        i = 0
        while i in range(0, counter):
            res = '0' + res
            i=i+1
    return res
  
# Permute function to rearrange the bits
def permute(k, arr, n):
    alpha = n
    permutation = ""
    i=0
    while i in range(0, n):
        y = arr[i]
        y = y-1
        z = k[y]
        permutation += z
        i = i+1
    return permutation
  
# shifting the bits towards left by nth shifts
def shift_left(k, nth_shifts):
    s = ""
    i = 0
    while i in range(nth_shifts):
        j = 1
        while j in range(len(k)):
            s = s + k[j]
            j = j + 1
        s = s + k[0]
        k = s
        s = "" 
        i = i + 1
    return k    
  
# calculating xow of two strings of binary number a and b
def xor(a, b):
    ans = ""
    i = 0
    while i in range(len(a)):
        x = a[i]
        y = b[i]
        if x == y:
            ans = ans + "0"
        else:
            ans = ans + "1"
        i = i + 1
    return ans
  
# Table of Position of 64 bits at initail level: Initial Permutation Table
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2, 
                60, 52, 44, 36, 28, 20, 12, 4, 
                62, 54, 46, 38, 30, 22, 14, 6, 
                64, 56, 48, 40, 32, 24, 16, 8, 
                57, 49, 41, 33, 25, 17, 9, 1, 
                59, 51, 43, 35, 27, 19, 11, 3, 
                61, 53, 45, 37, 29, 21, 13, 5, 
                63, 55, 47, 39, 31, 23, 15, 7] 
  
# Expansion D-box Table
exp_d = [32, 1 , 2 , 3 , 4 , 5 , 4 , 5, 
         6 , 7 , 8 , 9 , 8 , 9 , 10, 11, 
         12, 13, 12, 13, 14, 15, 16, 17, 
         16, 17, 18, 19, 20, 21, 20, 21, 
         22, 23, 24, 25, 24, 25, 26, 27, 
         28, 29, 28, 29, 30, 31, 32, 1 ]
  
# Straight Permutaion Table
per = [ 16,  7, 20, 21,
        29, 12, 28, 17, 
         1, 15, 23, 26, 
         5, 18, 31, 10, 
         2,  8, 24, 14, 
        32, 27,  3,  9, 
        19, 13, 30,  6, 
        22, 11,  4, 25 ]
  
# S-box Table
sbox =  [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], 
          [ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], 
          [ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], 
          [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]],
             
         [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], 
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], 
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], 
           [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]], 
    
         [ [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], 
           [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], 
           [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], 
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]], 
        
          [ [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], 
           [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], 
           [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], 
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14] ], 
         
          [ [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], 
           [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], 
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], 
           [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]], 
        
         [ [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], 
           [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], 
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], 
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13] ], 
          
          [ [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], 
           [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], 
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], 
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12] ], 
         
         [ [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], 
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2], 
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], 
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11] ] ]
    
# Final Permutaion Table
final_perm = [ 40, 8, 48, 16, 56, 24, 64, 32, 
               39, 7, 47, 15, 55, 23, 63, 31, 
               38, 6, 46, 14, 54, 22, 62, 30, 
               37, 5, 45, 13, 53, 21, 61, 29, 
               36, 4, 44, 12, 52, 20, 60, 28, 
               35, 3, 43, 11, 51, 19, 59, 27, 
               34, 2, 42, 10, 50, 18, 58, 26, 
               33, 1, 41, 9, 49, 17, 57, 25 ]
  
def encrypt(pt, rkb, rk):
    pt = hex2bin(pt)
      
    pt = permute(pt, initial_perm, 64)
      
    left = pt[0:32]
    right = pt[32:64]
    i = 0
    while i in range(0, 16):
        right_expanded = permute(right, exp_d, 48)
          
        xor_x = xor(right_expanded, rkb[i])
  
        sbox_str = ""
        j = 0
        while j in range(0, 8):
            tem = xor_x[j * 6] + xor_x[j * 6 + 5]
            row = bin2dec(int(tem))
            tem1 = xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]
            col = bin2dec(int(tem1))
            val = sbox[j][row][col]
            sbox_str += dec2bin(val)
            j = j + 1
              
        sbox_str = permute(sbox_str, per, 32)
          
        result = xor(left, sbox_str)
        left = result
          
        if(i != 15):
            left, right = right, left 
        i = i + 1
      
    combine = left
    combine += right
      
    cipher_text = permute(combine, final_perm, 64)
    return cipher_text

def DES(pt):
    key = "133457799BBCDFF1"
  

    key = hex2bin(key)
  
    keyp = [57, 49, 41, 33, 25, 17, 9, 
            1, 58, 50, 42, 34, 26, 18, 
            10, 2, 59, 51, 43, 35, 27, 
            19, 11, 3, 60, 52, 44, 36, 
            63, 55, 47, 39, 31, 23, 15, 
            7, 62, 54, 46, 38, 30, 22, 
            14, 6, 61, 53, 45, 37, 29, 
            21, 13, 5, 28, 20, 12, 4 ]
  
 
    key = permute(key, keyp, 56)
  
 
    shift_table = [1, 1, 2, 2, 
                2, 2, 2, 2, 
                1, 2, 2, 2, 
                2, 2, 2, 1 ]
  

    key_comp = [14, 17, 11, 24, 1, 5, 
            3, 28, 15, 6, 21, 10, 
            23, 19, 12, 4, 26, 8, 
            16, 7, 27, 20, 13, 2, 
            41, 52, 31, 37, 47, 55, 
            30, 40, 51, 45, 33, 48, 
            44, 49, 39, 56, 34, 53, 
            46, 42, 50, 36, 29, 32 ]

    left = key[0:28]     
    right = key[28:56]  
  
    rkb = []
    rk  = []
    i = 0
    while i in range(0, 16):
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])
      
        combine_str = left
        combine_str += right
      
        round_key = permute(combine_str, key_comp, 48)
   
        rkb.append(round_key)
        rk.append(bin2hex(round_key))
        i = i + 1

    cipher_text = bin2hex(encrypt(pt, rkb, rk))
    return cipher_text


def hash_block(block):
    sha = hashlib.sha256()
    #hash the data from all the tuples of the block
    sha.update(str(block[0]).encode() + str(block[1]).encode() + str(block[2]).encode()  + str(block[3]).encode() + str(block[4]).encode())
    x = sha.hexdigest()
    #parts = [x[i:i+4] for i in range(0, len(x), 4)]
    a = x[0:16]
    b = x[16:32]
    c = x[32:48]
    d = x[48:64]
    #ans = DES(a)+DES(b)+DES(c)+DES(d)
    ans = DES(a.upper()) + DES(b.upper()) + DES(c.upper()) + DES(d.upper())
    return ans

#function to add the first block to the blockchain 
def genesis_block():
    r = random.randint(1, PRIME - 1)
    b = random.randint(0,1)
    traID = random.randint(1, 1000000000)
    new_block = [0, traID, datetime.datetime.now(),0,'x','y','69']
    hash_of_block = hash_block(new_block)
    new_block.append(hash_of_block)
    return new_block

#function to create a new block
def createBlock(index, traID, previous_hash, data, sender, receiver, amount):
    block = [index, traID, previous_hash,data, sender, receiver, amount]
    hash_of_block = hash_block(block)
    block.append(hash_of_block)
    return block

#function to verify if the blockchain is valid
def verifyChain(blockchain):
    for i in range(1,len(blockchain)):
        #current block's previous hash
        current = blockchain[i][3]
        #previous block's current hash
        if(i-1>0):
            previous = blockchain[i-1][8]
        else:
            return True    
        #check if the block itself has been tampered with
        if(blockchain[i][8] != hash_block(blockchain[i])):
            return False
        #check  if the hashes are in orderly fashion in the chain
        if(previous != current):
            return False
    return True

#function to mine new blocks to add to the chain
def mine(index, traID, blockchain):
    #start time to mine blocks
    start = time.time()
    #get the traID for the previous block
    traID = blockchain[index - 1][1]
    #calculate y
    y = (GENERATOR ** int(traID)) % PRIME
    #bruteforce values of r and b to solve for the ZKP
    for i in range(0, PRIME - 1):
        for j in range(0, 2):
            #calculate h
            h = (GENERATOR ** i) % PRIME
            #calculate s
            s = (i + j * int(traID)) % (PRIME - 1)
            #calculate the first_proof and the second_proof
            first = (GENERATOR ** s) % PRIME
            second = (h * (y ** j)) % PRIME
            #check if both are equal
            if first == second:
                duration = time.time() - start
                temp = str(i)+" "+str(j)
                #return the [r,b] tuple and the time it took to mine the block
                return temp, duration

'''
    Structure of the Blockchain list:
        0th index -- index
        1st index -- transactionID
        2nd index -- Previous block's hash
        3rd index -- data corresponding to ZKP
        4th index -- Sender
        5th index -- Receiver
        6th index -- Amount
        7th index -- Current block's hash
'''
#function to print the blockchain in a readable manner
def print_chain(blockchain, index):
    for i in range(len(blockchain)):
        if i == index:
            print("Index -- ",blockchain[i][0])
            print("traID -- ", blockchain[i][1])
            print("Hash -- ", blockchain[i][7])
            print("Previous Hash -- ", blockchain[i][2])
            print("Sender -- ",blockchain[i][4])
            print("receiver -- ",blockchain[i][5])
            print("Amount -- ", blockchain[i][6])
            print()

def viewUser(username, blockchain, nt):
    i=0
    found = False
    l=len(blockchain)
    while i in range(l):
        if(blockchain[i][4] == username):
            print("Transaction ID -- ",blockchain[i][1])
            print("Sent to -- ",blockchain[i][5])
            print("Amount -- ", blockchain[i][6])
            print()
            found = True
        elif(blockchain[i][5] == username):
            print("Transaction ID -- ",blockchain[i][1])
            print("Recieved from -- ",blockchain[i][4])
            print("Amount -- ", blockchain[i][6])
            print()
            found = True
        i=i+1
    if(found==False):
        print("User not found")        



#main function
def main():
    #initialize the blockchain
    mydb = sqlite3.connect("crypto.db")
    mycursor = mydb.cursor()
    mycursor.execute("select * from Data_entry")
    myresult = mycursor.fetchall()
    blockchain = []
    #add the genesis block
    blockchain.append(genesis_block())
    for x in myresult:
        blockchain.append(x)
    index = int(blockchain[len(blockchain)-1][0])+1
    c = int(input("Enter No of transactions: "))
    transactions = []
    for i in range(c):
        sender, receiver, amount = input().split()
        transactions.append((sender, receiver, amount))
    i=0
    #loop to continuosly verify, mine and add new blocks to the chain
    while i in range(c):
        #boolean function to verify if chain is valid
        print("Is chain valid -- ", verifyChain(blockchain))
        #random traID generator to act as secret data stored on the chain
        traID = random.randint(1, 1000000000)
        
        #mine and get the time required to mine new blocks
        data, duration = mine(index, traID, blockchain)
        print("Time to mine -- ", duration, " seconds")
        #add the new block to the chain
        blockchain.append(createBlock(index, traID,blockchain[len(blockchain)-1][7],data,transactions[i][0],transactions[i][1],transactions[i][2]))
        sql = "INSERT INTO Data_entry (index_table, transID, previous_hash, data_ZKP, sender, receiver, amount, current_hash) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (index, traID, blockchain[len(blockchain) - 2][7], data, transactions[i][0], transactions[i][1], transactions[i][2],blockchain[len(blockchain)-1][7])
        mycursor.execute(sql,val)
        mydb.commit()
        #print the new block
        print_chain(blockchain, index)
        index = index + 1
        i=i+1
    uname = input("Enter username: ")
    viewUser(uname, blockchain, c)    

if __name__ == "__main__":
    main()
    
