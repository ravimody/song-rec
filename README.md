song-rec
========

recommend songs via collaborative filtering

The algorithm is very simple: 
1. Normalize the listen counts by user (so each user has a summed total of 1 - this gives a view of the listening behavior of a user without taking into account relative listening volumes)
2. Take the dot product between the listening counts of forUser with all other users, and find the nTopUsers with the highest scores. This gives the users with the most similar listening behavior. 
3. For these nTopUsers, sum all their normalized song scores and return the nRecs songs with the highest scores that forUser has never listened to. 

This algorithm should scale well - all three steps should operate in at most O(n*m) time, where n is the number of users and m is the average number of songs each has listened to - this product is the number of non-zero values in the song-user-listen matrix. Further, the first two steps would parallelize quite well by distributing the user's listening data, and the third "reduce" step runs in O(nTopUsers * m) time, which should scale infinitely because none of these values depend on the number of users or songs.  
