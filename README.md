# MinHash Algorithm for Sales Transactions

Today, data is growing rapidly in the information society. An incredible amount of structured and unstructured data is generated every day from social networks, financial industries, medical devices and digital equipment and similar tools. In the age of technology, one of the areas where the biggest data is formed is e-commerce. With the development of technology in recent years, e-commerce plays an important role in supporting the development of businesses. Thanks to e-commerce, businesses can access and establish a wider market presence by providing cheaper and more efficient distribution channels for their products or services.

In this study, it is aimed to find the similarities between the customers by creating MinHash signatures of the product information of the customers by using the data set of one-year sales transaction of the UK-based e-commerce (online retail).

# Dataset

The dataset used in the study was taken from Kaggle (Ramos, 2018). The dataset used in the study contains information about the one-year sales process of the UK-based e-commerce (online retail). This London-based store has been selling gifts and household items for adults and children through its website since 2007. This store has customers from all over the world and often shop directly for themselves. Small businesses that buy in bulk and sell to other customers through retail channels are also included in the dataset.

# Jaccard Similarity

The Jaccard similarity coefficient is a statistical method used to measure the similarity and diversity of sample sets. Jaccard similarity measures similarity between finite sets of samples and is defined as the size of the intersection divided by the size of the union of sample sets, as indicated in the expression given below.

$$ J(A,B) = \frac{|A\cap B|}{|A\cup B|}$$

Jaccard similarity can take a value between 0 and 1. If all elements of both sets are common, the Jaccard similarity is 1. If the number of elements of the intersection of two sets is the empty set, then the Jaccard similarity takes the value 0.

# MinHash Algorithm

The MinHash algorithm is a technique used to efficiently calculate an accurate estimate of the Jaccard similarity coefficient. The MinHash algorithm was developed by Andrei Broder (1997) and was first used in the AltaVista search engine to detect duplicate web pages and exclude them from search results.


In the MinHash algorithm, a permutation of the rows is taken for the MinHash representation of a column in the characteristic matrix. For two sets in the characteristic matrix S and T, let h be a hash function that maps members in the characteristic matrix to different integers. The MinHash value for a column (set) is hmin, the number (or element) of the first 1 row in that column. If the MinHash value is applied to both S and T sets, it is seen that the MinHash values (hmin (S) = hmin (T)) are equal if the item with the minimum hash value among all the elements of S∪T is located at the S∩T intersection (Wu et al., 2018) ). The probability that this is true, P, is exactly equal to the Jaccard index as given below.

$$ J(S,T) = P[h_{min}(S) = h_{min}(T)] $$

However, it is not feasible in terms of both time and workload for a large universal set to generate explicit random permutations. Therefore, in practice, uniform mapping is often used. It is possible to simulate the permutation effect of the characteristic matrix using the random hash function. The simplest version of the MinHash scheme uses k different hash functions; where k is a constant integer parameter and represents each set of S with k values of hmin (S) for these k functions.

The general form of the hash function used in this study is given below.

$$ h_{min} (S_i) =(a_{i} .x_{i} + b{i}) mod p$$

Here, p denotes a prime number greater than the number of members in the characteristic matrix, ai and bi denotes an integer less than the prime number p, and xi the unique number assigned to the elements in each member.

# Scheme of Study

In the study, firstly, the customer-product information of the data received via Kaggle was taken. And then each product is assigned a unique ID between 0 and the number of products.

For a determined number of hash functions at the beginning, the coefficients ai and bi in the hash function given in Eq.3 are randomly generated in a way that is different for each hash function. MinHash signature of each customer was created for the determined hash functions, and the approximate Jaccard similarity of all customers was obtained from these signature matrices. Afterwards, the estimated Jaccard similarities calculated with the real Jaccard similarities obtained previously for all customer pairs are compared. During the comparison, customer pairs with values above 0.5 from approximate and actual values are considered to be similar customers. For this threshold value, the number of true positive, true negative, false positive and false negative was calculated according to the number of hash functions.

# Results

In this study, different values between 5 and 30 were given to the number of hash functions and this process was repeated 10 times for each hash function. The results were evaluated according to the mean of the repeated solutions. In Figure 1, the graph of the average generation times of MinHash signatures according to the number of hash functions is given. As can be seen in the graph obtained, the time to create hash functions has increased gradually as the complexity of the process has increased.

![image](https://github.com/HuseyinOzdemir1/MinHash_Algorithm_for_Sales_Transactions/assets/75394581/ef1b9517-073b-4297-9b96-245fe7465dc3)

Average calculation times of approximate Jaccard similarity for each number of hash functions are given in Figure 2. It took approximately 194.7329 seconds to calculate the true Jaccard similarity for all customer pairs. When the graph given in Figure 2 is examined, the calculation time of approximate Jaccard similarity varies between about 10 percent and 38 percent of the calculation time of the real Jaccard similarity according to the number of hash functions. Considering the hardware of the computer where the operation is performed, it can be said that the MinHash algorithm is very effective in the computation time.

![image](https://github.com/HuseyinOzdemir1/MinHash_Algorithm_for_Sales_Transactions/assets/75394581/42abcbd1-71bc-4629-b841-8279d940730d)

It is necessary to check whether the MinHash algorithm is created in effective times, as well as the accuracy of the approximate Jaccard similarities obtained. Therefore, the approximate Jaccard similarity calculated with the previously obtained real Jaccard similarity is compared for all customer pairs. During the comparison, customer pairs with values above 0.5 from approximate and actual values are considered to be similar customers. For this threshold value, the number of true positive, true negative, false positive and false negative was calculated according to the number of hash functions.

In Figure 3, the variation of the number of true positives (the number of those estimated to be similar when the products are actually similar) and the number of hash functions is given. Considering the results of the graph obtained, the number of true positives increased with the increase in the number of hash functions. The reason for this is that the MinHash algorithm better represents the real data set thanks to the increase in the number of hashes. In real Jaccard similarities, the number of similar client pairs that exceed the threshold is 309, and the number of client pairs that exceed the threshold in the maximum number of hashes and are actually similar is 270.

![image](https://github.com/HuseyinOzdemir1/MinHash_Algorithm_for_Sales_Transactions/assets/75394581/84db499b-90dc-40be-820c-b45da3a38755)

In Figure 4, the variation of the number of true negatives (the number of those predicted as not similar when the products are actually not similar) and the number of hash functions is given. In real Jaccard similarity, the number of dissimilar client pairs below the threshold is 11226382, and the number of customer pairs that fall below the threshold in the maximum number of hashes and are actually dissimilar is 11226195. Looking at the graph, it can be said that the true negative number is successful in converging to its true value.

![image](https://github.com/HuseyinOzdemir1/MinHash_Algorithm_for_Sales_Transactions/assets/75394581/3e1df303-de92-4f83-8072-c4a49d1bfd53)

In Figure 5, the variation of the number of false positives (the number of those predicted to be similar when the products are not actually similar) and the number of hash functions is given. The number of customer pairs that exceed the threshold in the maximum number of hashes and are actually dissimilar is 187. The calculated approximate Jaccard similarity of these client pairs usually ranges from 0.5 to 0.6. The number of false positives can be reduced by increasing the number of hash functions or by creating hash functions that better represent the data set. Looking at the graph, it can be said that with increasing the number of hash functions, the number of false positives gradually converges to zero.

![image](https://github.com/HuseyinOzdemir1/MinHash_Algorithm_for_Sales_Transactions/assets/75394581/a9482bc8-7cd1-4e6a-aefc-5d95dc493366)

In Figure 6, the variation of the number of false negatives (the number of predicted products as being similar but not similar) with the number of hash functions is given. Looking at the graph, it can be said that the number of false negatives gradually converges to zero with increasing the number of hash functions. The number of false negatives can be reduced by increasing the number of hash functions, as in the number of false positives, or by creating hash functions to better represent the data set.

![image](https://github.com/HuseyinOzdemir1/MinHash_Algorithm_for_Sales_Transactions/assets/75394581/023f401f-7d1a-4bf5-ba06-110d3cac010a)

