from rest_framework.serializers import ModelSerializer

from submitter.models import Submitter


class SubmitterSerializer(ModelSerializer):
    class Meta:
        model = Submitter
        fields = ('id', 'name',)