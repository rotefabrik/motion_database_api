from rest_framework.serializers import ModelSerializer

from convention.models import Convention, Section


class ConventionSerializer(ModelSerializer):
    class Meta:
        model = Convention
        fields = ('id', 'label', 'slot', 'year')


class SectionSerializer(ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name')
