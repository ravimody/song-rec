from scipy import sparse
from sklearn.preprocessing import normalize
from numpy import array
from numpy import inf

# run an example test:
dataset = get_rand_dataset(1000, 20000)
recommendTracks(dataset, forUser = 0, nRecs = 10, nTopUsers = 10)

def recommendTracks(dataset, forUser, nRecs, nTopUsers):
   normalized_dataset = normalize_dataset(dataset)
   similar_users = find_similar_users(normalized_dataset, forUser, nTopUsers)
   return(create_recommendations(normalized_dataset, forUser, similar_users, nRecs))

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

def find_similar_users(normalized_dataset, user, num_similar_users):
   # get the dot product of the user with every user, this is effectively a similarity score 
   score = normalized_dataset[user,:] * normalized_dataset.transpose()
   # flatten matrix into 1-d array of scores, give -infinity score to user so he's not selected
   score = array(score.todense()).flatten()  
   score[user] = -inf
   similar_users = (-score).argsort()[0:num_similar_users]
   return(similar_users)
   
# normalize matrix so each user's plays sum to 1 
def normalize_dataset(dataset):
   return(normalize(dataset,norm='l1', axis=1) )

def get_rand_dataset(num_users = 10000, num_songs = 1000000, avg_songs_per_user = 10, max_plays = 20, seed = 100):
   density = float(avg_songs_per_user) / num_songs
   dataset = sparse.rand(num_users, num_songs, density, random_state = seed, format = 'csr') * max_plays
   dataset = dataset.ceil()
   return(dataset)
   # todo rhm: remove users with no listens; for now i'll assume this will generate users with at least one listen   
   