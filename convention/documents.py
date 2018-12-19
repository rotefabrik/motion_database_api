from django_elasticsearch_dsl import DocType, fields, Index

from convention.models import Convention

convention_index = Index('conventions')
convention_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@convention_index.doc_type
class ConventionDocument(DocType):
    label = fields.KeywordField()
    slot = fields.KeywordField()

    class Meta:
        model = Convention
        fields = ('year',)
