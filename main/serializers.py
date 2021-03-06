from rest_framework import serializers
from .models import article


# class articleSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100)
#     author = serializers.CharField(max_length=100)
#     email = serializers.EmailField(max_length=100)
#     date = serializers.DateTimeField()

#     def create(self, validated_data):
#         return article.objects.create(validated_data)
    
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title',instance.title)
#         instance.author = validated_data.get('author',instance.author)
#         instance.email = validated_data.get('email',instance.email)
#         instance.date = validated_data.get('date',instance.date)
#         instance.save()

#         return instance

class articleSerializer(serializers.ModelSerializer):
    class Meta:
        model = article
        fields = ['idd','title','author','email','date']

        #or we can just do that
        # fields = '__all__'

    # def validate_idd(self, id):
    #     if id<10:
    #         raise serializers.ValidationError('Id should be greater than 10')