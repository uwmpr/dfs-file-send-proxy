import requests, json, os, random

async def send_file(channel_id, auth, filename):
    print(filename)
    head = {
        "Content-Type": "application/json",
        "Authorization": auth
    }
    id = random.randint(1,99)
    filesize = os.path.getsize("file_send/" + filename)
    body = {
        "files":[
            {
                "filename": filename,
                "file_size": filesize,
                "id": id,

            }
        ]
    }
    response = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/attachments', headers=head, json=body)
    if (response.status_code == 200):
        data = json.loads(response.text)
        url = data["attachments"][0]["upload_url"]
        upload_filename = data["attachments"][0]["upload_filename"]
        with open("file_send/" + filename, "rb") as file:
            response2 = requests.put(url, data=file)
        if(response2.status_code == 200):
            head = {
                "Authorization": auth,
            }
            body = {
                "content": "",
                "channel_id": channel_id,
                "attachments": [
                    {
                        "id": id,
                        "filename": filename,
                        "uploaded_filename": upload_filename
                    }
                ]
            }
            response3 = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=head, json=body)
            if (response3.status_code == 200):
                os.remove("file_send/" + filename)
                return 200
            else:
                print ("!")
                return 500

        else:
            print("ok")
            return 500
    else:
        print("lp")
        return 500