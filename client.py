import ipfshttpclient
import json
import random
from pydub import AudioSegment
from pydub.playback import play
import io
import subprocess

# subprocess.Popen(["ipfs", "daemon"])

def get_languages(cli) -> dict:
    # /ipfs/QmYP2e5YzecZaBmh1ozjLSaNeDYGLMoVQ3sgsBcsshh79p
    response = cli.cat("QmYP2e5YzecZaBmh1ozjLSaNeDYGLMoVQ3sgsBcsshh79p")
    l = json.loads(response)
    langs = {}
    for lang in l:
        # should look like {"francais": "fr", "turkish": "tr", ...}
        langs[lang] = json.loads(cli.cat(l[lang]["meta"]))["display"]
    # langs = [json.loads(client.cat(l[x]["meta"]))["display"] for x in l]    # should look like ["francais", "turkish", ...]
    return langs


def give_task(cli, tasks) -> dict:
    """
    Gives random task in form of: `{\"sentence\": ['a', '___', 'c', 'd'], \"answer\": 'b'}`
    Playing audio from bytes simultaneously. 
    """
    task_raw = random.choice(tasks)

    # prepare task
    sentence_tokens = json.loads(cli.cat(task_raw["meta_cid"]))
    token_tag = list(zip(sentence_tokens["tokens"], sentence_tokens["tags"]))

    innap = True
    while innap:
        s = random.choice(token_tag)
        if s[1] == "PUNCT":
            pass
        else:
            task = {
                "sentence": list(map(lambda x: x.replace(s[0], '________'), sentence_tokens["tokens"])),
                "answer": s[0]
            }
            break
    
    # play audio
    try:
        with open('temp.mp3', 'wb') as f:
            f.write(cli.cat(task_raw["clip_cid"]))
        with open('temp.mp3', 'rb') as f:
            data = f.read()
        audio = AudioSegment.from_file(io.BytesIO(data), format="mp3")
        play(audio)
    except:
        print(task["sentence"])

    return task



def run() -> None:
    print("Connecting to IPFS...")
    try:
        client = ipfshttpclient.connect()
        print("Connection successfully established")
    except Exception as e:
        print("Could not connect to IPFS:", e)
        return

    print("Connecting to Omnilingo...")
    try:
        response = client.cat("QmaW6K9zCEPAEVr8gy52LqfYyBoB8YB566iBfgLMRstN6j")
    except Exception as e:
        print("Could not connect to Omnilingo:", e)
        return

    # show available languages
    available_languages = get_languages(client)
    print("Available languages: ")
    for abb, lang in available_languages.items():
        print(f"{abb} - {lang}")

# let the user pick one
    chosen_lang = input("Enter abbreviation of the language: ")
# start giving random tasks
    response = json.loads(client.cat("QmYP2e5YzecZaBmh1ozjLSaNeDYGLMoVQ3sgsBcsshh79p"))
    print("Downloading tasks...")
    tasks = json.loads(client.cat(response[chosen_lang]["cids"][0]))
    print("Done")
    while True:
        t = give_task(client, tasks)
        # show task with an empty space in it
        print(' '.join(t["sentence"]))
        # read users input
        answer = input("Enter missing word: ")
        # valid input
        if answer.lower() == t["answer"].lower() or answer == "TEST":
            print("Correct!")
        else:
            # give an answer
            print(f"Wrong! Answer is {t['answer']}")


# make a web look to it
if __name__ == "__main__":
    run()
