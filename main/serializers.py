from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class ItemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H/%M/%S', read_only=True)
    image = ImageSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Item
        fields = '__all__'
        # exclude = ('__all__')

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        author = request.user

        item = Item.objects.create(user=author, **validated_data)
        for image in images_data.getlist('images'):
            Image.objects.create(item=item, image=image)

        return item

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        instance.images.all().delete()
        images_data = request.FILES
        for image in images_data.getlist('images'):
            Image.objects.create(item=instance, image=image)
        return instance



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        representation['images'] = ImageSerializer(instance.images.all(), many=True, context=self.context).data
        return representation

