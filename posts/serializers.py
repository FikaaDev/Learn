from rest_framework import serializers
from .models import Post
# Serializers allows us to validate the data from the API and also forward the data to the database in a json format.

class PostSerializerWOModel(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    title = serializers.CharField(max_length = 50)
    content = serializers.CharField()
    created =  serializers.DateTimeField(read_only = True)

class PostSerializer(serializers.ModelSerializer):
    # Converting Django models objects into JSON
    # Then convert this JSON into data which can be saved into DB using serializer 
    title = serializers.CharField(max_length = 50)
    content = serializers.CharField()
    created =  serializers.DateTimeField(read_only = True)
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "created",
        ]
    