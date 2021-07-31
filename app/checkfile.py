from app import app








def checkfile(media):
    if not "." in media.filename or media.filename=="":
        return False
    else:
        ext = media.filename.rsplit(".", 1)[1]
        if ext.upper() in app.config["EXTENSIONS"]:
            return True
        else:
            return False
