from scipy import sparse
from sklearn.preprocessing import normalize
from numpy import array
from numpy import inf

# *** library code ***

# driver code to run all the functions
def recommendTracks(dataset, forUser, nRecs, nTopUsers):
   normalized_dataset = normalize_dataset(dataset)
   similar_users = find_similar_users(normalized_dataset, forUser, nTopUsers)
   return(create_recommendations(normalized_dataset, forUser, similar_users, nRecs))

# normalize matrix so each user's plays sum to 1 
def normalize_dataset(dataset):
   return(normalize(dataset,norm='l1', axis=1) )

# find similar users based off of a song-song dot product similarity score
def find_similar_users(normalized_dataset, user, num_similar_users):
   # get the dot product of the user with every user, this is effectively a similarity score 
   score = normalized_dataset[user,:] * normalized_dataset.transpose()
   # flatten matrix into 1-d array of scores, give -infinity score to user so he's not selected
   score = array(score.todense()).flatten()  
   score[user] = -inf
   similar_users = (-score).argsort()[0:num_similar_users]
   return(similar_users)

#  create the recommendations from similar users by summing up their normalized listening data and ranking the summed song scores
def create_recommendations(normalized_dataset, user, similar_users, num_recs):
   # for the top similar_users users sum their play scores
   similar_users_plays = normalized_dataset[similar_users,:]
   similar_songs = similar_users_plays.sum(axis = 0)
   # zero the score of tracks already listened to by user
   songs_already_heard = normalized_dataset[user,:].nonzero()[1]
   similar_songs[:,songs_already_heard] = 0
   # pick the tracks with the num_recs highest summed scores
   similar_songs = array(similar_songs).flatten()
   top_similar_songs = (-similar_songs).argsort()[0:num_recs]
   return(top_similar_songs)

# *** code to generate some test data ***
def get_rand_dataset(num_users = 10000, num_songs = 1000000, avg_songs_per_user = 100, max_plays = 50, seed = 100):
   density = float(avg_songs_per_user) / num_songs
   dataset = sparse.rand(num_users, num_songs, density, random_state = seed, format = 'csr') * max_plays
   dataset = dataset.ceil()
   return(dataset)

# *** benchmark generating 10 recommendations from 20 users ***
dataset = get_rand_dataset(10000, 1000000)
%timeit recommendTracks(dataset, forUser = 0, nRecs = 100, nTopUsers = 20)
# 10 loops, best of 3: 99.3 ms per loop (on 2011 macbook air with 4GB of ram)
