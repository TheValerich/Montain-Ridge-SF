from rest_framework import serializers

from pereval.models import Users, Pereval, Images, Coords


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    image_1 = serializers.URLField(label='URL изображения 1', allow_blank=True)
    image_2 = serializers.URLField(label='URL изображения 2', allow_blank=True)
    image_3 = serializers.URLField(label='URL изображения 3', allow_blank=True)

    class Meta:
        model = Images
        fields = ['title_1', 'image_1', 'title_2', 'image_2', 'title_3', 'image_3']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class PerevalSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    images = ImagesSerializer()
    coordinates = CoordsSerializer()

    class Meta:
        model = Pereval
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'status', 'level',
                  'coordinates',
                  'user',
                  'images']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        images_data = validated_data.pop('images')
        coordinates_data = validated_data.pop('coordinates')

        user = Users.objects.create(**user_data)
        images = Images.objects.create(**images_data)
        coordinates = Coords.objects.create(**coordinates_data)

        pereval = Pereval.objects.create(user=user, images=images, coordinates=coordinates, **validated_data)
        pereval.save()
        return pereval