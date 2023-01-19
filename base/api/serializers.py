from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
	class Meta:
		model=Room#Define the model that will be used to serialize the object
		fields='__all__'#Define which fields will be used in the serialization