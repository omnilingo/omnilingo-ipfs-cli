import ipfshttpclient

# /ipfs/QmYP2e5YzecZaBmh1ozjLSaNeDYGLMoVQ3sgsBcsshh79p
# show available languages
available_languages = {}

def run():
    IPFS_API_URL = 'http://127.0.0.1:8080'
    IPFS_HASH_PREFIX = '/ipfs/'
    client = ipfshttpclient.connect()
    client = ipfshttpclient.connect(IPFS_API_URL)
    try:
        response = client.cat(IPFS_HASH_PREFIX+"QmYP2e5YzecZaBmh1ozjLSaNeDYGLMoVQ3sgsBcsshh79p")
        print(response)
    except Exception as e:
        print(e)

# let the user pick one
# start giving random tasks
# show task with an empty space in it
# read users input
# valid input
# give an answer


# make a web look to it
if __name__=="__main__":
    run()