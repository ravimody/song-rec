song-rec
========

recommend songs via collaborative filtering

The algorithm is very simple: 

1. Normalize the listen counts by user (so each user has a summed total of 1 - this gives a view of the listening behavior of a user without taking into account relative listening volumes)
2. Take the dot product between the listening counts of forUser with all other users, and find the nTopUsers with the highest scores. This gives the users with the most similar listening behavior. 
3. For these nTopUsers, sum all their normalized song scores and return the nRecs songs with the highest scores that forUser has never listened to. 

This algorithm should scale well - all three steps should operate in at most O(n*m) time, where n is the number of users and m is the average number of songs each has listened to - this product is the number of non-zero values in the song-user-listen matrix (my benchmarks show there is some dependency on the total number of songs in the dataset - some operations in my code do run in O(number_songs) time, but these are pretty minor operations and can likely be optimized with more time). The third "reduce" step runs in O(nTopUsers * m) time, which should scale infinitely because none of these values depend on the number of users or songs. Also, the first two steps would parallelize quite well by distributing the user's listening data. Further, if it's desired to generate multiple user's recommendations at once, step 2 can be sped up by replacing it with a matrix multplication of many user's scores. 

My 2011 macbook air with 4 GB of RAM can generate a user's recommendations in 100 ms in a universe of 10k users and 1M songs. This would obviously be much faster on a better machine :)  Also, as discussed above, this could be scaled up to many more users by parallelizing over the users. 
