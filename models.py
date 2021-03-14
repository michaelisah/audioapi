from sqlalchemy import func

from db import db


class AudioModel(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    fileType = db.Column(db.String(100), default='song')
    metaData = db.Column(db.Text, nullable=False)
    uploadedTime = db.Column(db.DateTime, server_default=func.now())

    # for Song
    # - name
    # - duration

    # for Podcast
    # - name
    # - host
    # - participants
    # - duration

    # for Audiobook
    # - title
    # - author
    # - narrator
    # - duration
