class User:
    def __init__(self, user_id, username):
        self.id = user_id
        self.id = username
        self.follower = 0
        self.following = 0


    def follow(self, user):
        user.follower +=1
        self.following +=1

user_1 = User("001", "Max")
user_2 = User("002", "Maxi")
user_2.follow(user_1)
print(user_1.follower)