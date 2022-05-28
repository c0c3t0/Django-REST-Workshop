from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import password_validation as validators
from django.core import exceptions
from rest_framework import serializers

UserModel = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, 'password')

    # hash password in database
    def create(self, validated_data):
        user = super().create(validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user

    # remove password from response
    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop('password')
        return result

    # invoke django password validators
    # def validate(self, data):
    #     user = UserModel(**data)
    #     password = data.get('password')
    #
    #     errors = dict()
    #     try:
    #         validators.validate_password(password=password, user=user)
    #
    #     except exceptions.ValidationError as exception:
    #         errors['password'] = list(exception.messages)
    #
    #     if errors:
    #         raise serializers.ValidationError(errors)
    #
    #     return super().validate(data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
