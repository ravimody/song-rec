from scipy import sparse


def get_rand_dataset(num_users = 10000, num_songs = 1000000, avg_songs_per_user = 10, max_plays = 20, seed = 100):
   density = float(avg_songs_per_user) / num_songs
   dataset = sparse.rand(num_users, num_songs, density, random_state = seed, format = 'csr') * max_plays
   dataset = dataset.ceil()
   return(dataset)
   
   