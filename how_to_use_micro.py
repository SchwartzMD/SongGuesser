# run the randomize_server.py file - it runs on your localhost until you stop it

# import the randomize_client file to your file
import randomize_client

# call the method and input a list object with any sort of objects in
# it will return one of those objects randomly
example = [1,"test", [55,2], 3]
random_result = randomize_client.randomObjReturn(example)

# do whatever you would like with the returned result

print(random_result)
