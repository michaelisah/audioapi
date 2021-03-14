import http.client
import json

from flask import request
from flask_restplus import Namespace, Resource, fields
from marshmallow import Schema, fields as maFields, validate, ValidationError, EXCLUDE
from sqlalchemy import func

from db import db
from models import AudioModel

api = Namespace(name='api', description='CRUD operations for audio file')


# Output formats
class ParseMetaData(fields.Raw):
    def format(self, value):
        return json.loads(value)


audioModel = api.model('Audio', {
    'ID': fields.Integer(),
    # 'fileType': fields.String(),
    'uploadedTime': fields.DateTime(),
    'metaData': ParseMetaData(),
})


# Input formats
# for documentation
audioInputModel = api.parser()
audioInputModel.add_argument(
    'audioFileMetadata',
    required=True,
    location='json'
)


# for input validation
class AudioMetaSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = maFields.Str(required=True, validate=validate.Length(min=1, max=100))
    host = maFields.Str(required=True, validate=validate.Length(min=1, max=100))
    participants = maFields.List(maFields.Str(validate=validate.Length(min=1, max=100)), max=10,  required=False)
    title = maFields.Str(required=True, validate=validate.Length(min=1, max=100))
    author = maFields.Str(required=True, validate=validate.Length(min=1, max=100))
    narrator = maFields.Str(required=True, validate=validate.Length(min=1, max=100))
    duration = maFields.Int(required=True)


@api.route('/<string:audioFileType>/')
class AudioList(Resource):
    @api.doc('list_audio_files')
    @api.marshal_with(audioModel, as_list=True)
    def get(self, audioFileType: str):
        """
        Retrieve all audio files for a specific type
        """

        query = AudioModel.query.filter(func.lower(AudioModel.fileType) == audioFileType.lower()).order_by('ID')
        return query.all()

    @api.expect(audioInputModel)
    @api.doc('add_audio_file')
    def post(self, audioFileType: str):
        """
        Add an audio file.
        """
        if audioFileType == 'song':
            validationSchema = AudioMetaSchema(only=("name", "duration"))
        elif audioFileType == 'podcast':
            validationSchema = AudioMetaSchema(only=("name", "host", "duration"))
        elif audioFileType == 'audiobook':
            validationSchema = AudioMetaSchema(only=("title", "author", "narrator", "duration", "participants"))
        else:
            return "Invalid audio type ", http.client.BAD_REQUEST

        try:
            # Validate and deserialize input
            metaData = validationSchema.load(request.get_json())
        except ValidationError as err:
            return err.messages, http.client.BAD_REQUEST

        # add audio file
        audioFile = AudioModel(
            fileType=audioFileType,
            metaData=json.dumps(metaData)
        )

        db.session.add(audioFile)
        db.session.commit()

        result = api.marshal(audioFile, audioModel)
        return result, http.client.OK


@api.route('/<string:audioFileType>/<int:audioFileID>/')
class Audio(Resource):
    @api.doc('get_audio_file')
    @api.marshal_with(audioModel)
    def get(self, audioFileType: str, audioFileID: int = None):
        """
        Retrieve a specific audio file using ID
        """
        audioFile = AudioModel.query.filter(
            func.lower(AudioModel.fileType) == audioFileType.lower(),
            AudioModel.ID == audioFileID
        ).first()

        if not audioFile:
            # The audio file does not exist
            return '', http.client.BAD_REQUEST

        return audioFile

    @api.expect(audioInputModel)
    @api.doc('update_audio_file')
    def put(self, audioFileType: str, audioFileID: int = None):
        """
        Update an audio file.
        """
        if audioFileType == 'song':
            validationSchema = AudioMetaSchema(only=("name", "duration"))
        elif audioFileType == 'podcast':
            validationSchema = AudioMetaSchema(only=("name", "host", "participants", "duration"))
        elif audioFileType == 'audiobook':
            validationSchema = AudioMetaSchema(only=("title", "author", "narrator", "duration", "participants"))
        else:
            return "Invalid audio type ", http.client.BAD_REQUEST

        try:
            # Validate and deserialize input
            metaData = validationSchema.load(request.get_json())
        except ValidationError as err:
            return err.messages, http.client.BAD_REQUEST

        audioFile = AudioModel.query.filter(
            func.lower(AudioModel.fileType) == audioFileType.lower(),
            AudioModel.ID == audioFileID
        ).first()

        if not audioFile:
            # The audio file does not exist
            return '', http.client.BAD_REQUEST

        # add audio file
        audioFile.metaData = json.dumps(metaData)
        db.session.add(audioFile)
        db.session.commit()

        result = api.marshal(audioFile, audioModel)
        return result, http.client.OK

    @api.doc('delete_audio_file', responses={http.client.OK: 'No content'})
    def delete(self, audioFileType: str, audioFileID: int = None):
        """
        Delete a specific audio file
        """

        audioFile = AudioModel.query.filter(
            func.lower(AudioModel.fileType) == audioFileType.lower(),
            AudioModel.ID == audioFileID
        ).first()
        if not audioFile:
            # The audio file does not exist
            return '', http.client.NO_CONTENT

        db.session.delete(audioFile)
        db.session.commit()

        return '', http.client.OK
