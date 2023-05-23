#pip install ipfshttpclient==0.8.0a1
import ipfshttpclient

# /ipfs/QmYP2e5YzecZaBmh1ozjLSaNeDYGLMoVQ3sgsBcsshh79p
# show available languages
available_languages = {}

def run():
    print("Connecting to IPFS...")
    try:
        client = ipfshttpclient.connect()
        print("Connection successfully established")
    except Exception as e:
        print("Could not connect to IPFS:", e)
        return

    print("Connecting to Omnilingo...")
    try:
        response = client.cat("QmYP2e5YzecZaBmh1ozjLSaNeDYGLMoVQ3sgsBcsshh79p")
        print(response)
    except Exception as e:
        print("Could not connect to Omnilingo:", e)
        return

# let the user pick one
# start giving random tasks
# show task with an empty space in it
# read users input
# valid input
# give an answer


# give user a convenient way to upload theirs' data


# make a web look to it
if __name__=="__main__":
    run()
