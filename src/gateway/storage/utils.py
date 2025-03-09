import pika, json # type: ignore

import pika.spec # type: ignore

def upload_file(file, fs, channel, access):
    try:
        file_id = fs.put(file)
    except Exception as error:
        return str(error), 500 
    
    message = {
        "video_fid" : str(file_id),
        "mp3_fid" : None,
        "username" : access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            message=json.dumps(message), 
            property=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
        )
    except Exception as error:
        print(error)
        fs.delete(file_id)
        return "internal server error", 500
