from rest_framework.serializers import ModelSerializer

from convention.serializers import ConventionSerializer, SectionSerializer
from motion.models import Motion, Referral
from submitter.serializers import SubmitterSerializer


class ReferralSerializer(ModelSerializer):
    class Meta:
        model = Referral
        fields = ('id', 'name',)


class MotionSerializer(ModelSerializer):
    convention = ConventionSerializer()
    section = SectionSerializer()
    referrals = ReferralSerializer(many=True)
    submitters = SubmitterSerializer(many=True)

    class Meta:
        model = Motion
        fields = ('id', 'convention', 'section', 'title', 'referrals', 'submitters', 'status', 'body')
