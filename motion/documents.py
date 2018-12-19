from django_elasticsearch_dsl import fields, DocType, Index

from motion.models import Motion, Referral

motion_index = Index('motions')
motion_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@motion_index.doc_type
class MotionDocument(DocType):
    convention = fields.ObjectField(properties={
        'label': fields.KeywordField(),
        'slot': fields.KeywordField(),
        'year': fields.DateField(),
    })

    section = fields.ObjectField(properties={
        'name': fields.KeywordField(),
    })

    identifier = fields.KeywordField()

    submitters = fields.NestedField(properties={
        'name': fields.KeywordField()
    })

    referrals = fields.NestedField(properties={
        'name': fields.KeywordField()
    })

    status = fields.KeywordField()

    created = fields.DateField()

    class Meta:
        model = Motion
        fields = [
            'title',
            'body',
        ]


referral_index = Index('referrals')
referral_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@referral_index.doc_type
class ReferralDocument(DocType):
    name = fields.StringField()

    class Meta:
        model = Referral
