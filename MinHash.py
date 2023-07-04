import random
import time
import pandas as pd
import numpy as np

# Collection of transaction data
df = pd.read_csv("transactions.csv")

# Customers and obtaining the products they buy
Customers = df["CustomerNo"]
Products = df["ProductName"]

# The dict where the products purchased by each customer will be stored;
CustomerSet = dict()

for i in range(len(Customers)):
        
    CustomerSet.setdefault(str(Customers[i]),[]).append(Products[i])

# Finding unique customers
Customers = Customers.unique()
  
# Deleting duplicates of each product
Products = df["ProductName"].unique()

# A required dict for assigning numbers to products
ProductID = {}

for i in range(len(Products)):
    
    ProductID[Products[i]] = i
    
# A dict where customers will sum up the products they bought with their numbers
CustomerSetID = {}
    
for custom in CustomerSet:
    
    setID = []
    
    for item in CustomerSet[custom]:
        
        setID.append(ProductID[item])
            
    CustomerSetID[custom] =  set(setID)

# Deleting space-consuming variables
del custom,item,ProductID,setID,Products

# Calculating the real Jaccard similarities
t0 = time.time()
print("Calculating the real Jaccard similarities...")

Jsims = {}
for i in range(len(Customers)):

    custom1 = CustomerSetID[str(Customers[i])] # First customer as set

    for j in range(i+1,len(Customers)):
        
        custom2 = CustomerSetID[str(Customers[j])] # Second customer as set

        """
        We need to define 2d array as 1d array.
        To do this, unique indexes can be created to represent each of the 2d array indexes.
        """
        Jsims[(i-1)*(len(Customers)-i/2) + j - i] = len(custom1.intersection(custom2)) / len(custom1.union(custom2))

print("It took {:.4f} seconds to calculate the real Jaccard Similarities" .format(time.time() - t0))

# A function that generates the necessary coefficients for hash functions to be randomly generated
# Function that ensures that the coefficient A is odd
def randomCoeffA(k,prime):
  # A list for 'k' random values
  randomList = []
  
  while k > 0:
    # The process of generating a random number
    randomIndex = random.randrange(1, prime,2) 

    # Checking if the randomly generated coefficient is in the list
    while randomIndex in randomList:
      randomIndex = random.randrange(1, prime,2) 
    
    # Adding the randomly obtained coefficient to the list
    randomList.append(randomIndex)
    k = k - 1
    
  return randomList

# A function that generates the necessary coefficients for hash functions to be randomly generated
# Randomly generated B coefficient between 0 and prime
def randomCoeffB(k,prime):
  # A list for 'k' random values
  randomList = []
  
  while k > 0:
    # The process of generating a random number
    randomIndex = random.randint(0, prime) 

    # Checking if the randomly generated coefficient is in the list
    while randomIndex in randomList:
      randomIndex = random.randint(0, prime) 
    
    # Adding the randomly obtained coefficient to the list
    randomList.append(randomIndex)
    k = k - 1
    
  return randomList

# The number of hashes to be used during MinHashing
numHashes = 5
"""
The number of different customers is 4739. 
The first prime number greater than this number will be used in the hash function 4751.
"""
prime = 4751

t0 = time.time()
print("Generating random hash functions...")

# Hash function = (a * productID + b) Mod(Prime)
# List of coefficients a and b required for the hash function
coeffA = randomCoeffA(numHashes, prime)
coeffB = randomCoeffB(numHashes, prime)

print("Generating MinHash signatures of customers...")

# A list where the signature matrices to be created with hash functions will be kept.
signatures = []
# For each customer
for customer in CustomerSetID.keys():
    
    # A list with the IDs of the products purchased by the customer
    productSet = CustomerSetID[customer]
    
    # The list to keep the customer's signature matrix
    signature = []
    
    # For each hash
    for i in range(0, numHashes):
              
        # Initial hash value
        hash = prime + 1
        
        for productID in productSet:
            
            # Hashing process
            hashValue = (coeffA[i] * productID + coeffB[i]) % prime
            # Checking the change of the hash value for each hash
            if hashValue < hash:
                
                hash = hashValue
        
        # Adding the final hash value to the signature matrix      
        signature.append(hash)
    
    # Collection of signature matrix of each customer
    signatures.append(signature)

print("It took {:.4f} seconds to generate customers' MinHash signatures." .format(time.time() - t0))

# Deleting space-consuming variables 
del signature,hashValue,hash,productID,i,productSet,t0,prime,customer,coeffA,coeffB

t0 = time.time()

print("Calculating customers' Jaccard similarity...")
size = len(signatures)

# Matrix to keep calculated Jaccard similarities
JaccardMinHash = {}

for i in range(0, size):
  # i. customer's MinHash signature
  signature1 = signatures[i]
    
  # Comparison with all other customers
  for j in range(i + 1, size):
    
    # j. customer's MinHash signature
    signature2 = signatures[j]
    
    count = 0
    # Number of cases where MinHash signatures match
    for k in range(0, numHashes):
      count = count + (signature1[k] == signature2[k])
    
    # Approximate Jaccard similarities
    JaccardMinHash[(i-1)*(len(Customers)-i/2) + j - i] = count / numHashes

print("It took {:.4f} seconds to calculate customers' Jaccard similarity." .format(time.time() - t0))

# Comparison of calculated MinHash similarities with real Jaccard similarities
tp = 0
fn = 0
tn = 0
fp = 0

threshold = 0.5
for i in range(size):  
  for j in range(i + 1, size):
      
      k = (i-1)*(len(Customers)-i/2) + j - i
      # Finding True Positive and False Positive numbers
      if JaccardMinHash[k] >= threshold and Jsims[k] >= threshold:
        tp = tp + 1
      elif JaccardMinHash[k] < threshold and Jsims[k] < threshold:
        tn = tn + 1
      elif JaccardMinHash[k] >= threshold and Jsims[k] < threshold:
        fp = fp + 1
      else:
        fn = fn + 1

print("True Positive: {} ".format(tp))
print("True Negative: {} ".format(tn))
print("False Positive: {} ".format(fp))
print("False Negative: {} ".format(fn))

del i,j,k,size,numHashes,tp,tn,fp,fn,signatures,signature1,signature2,threshold,t0,count
