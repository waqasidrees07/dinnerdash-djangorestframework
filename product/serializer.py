from rest_framework import serializers
from .models import Restaurant, Product


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

        def create(self, validated_data):
            product = Product.objects.create(
                title=validated_data['title'],
                description=validated_data['description'],
                price=validated_data['price'],
                category=validated_data['category'],
                image=validated_data['image'],
                restaurant=validated_data['restaurant']
            )
            return product


class GetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id"]


class AddRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["title", "address", "city"]

        def create(self, validated_data):
            restaurant = Restaurant.objects.create(
                title=validated_data['title'],
                address=validated_data['address'],
                city=validated_data['city']
            )
            return restaurant


class GetRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
