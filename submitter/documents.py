from django_elasticsearch_dsl import fields, DocType, Index

from submitter.models import Submitter

submitter_index = Index('submitters')
submitter_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@submitter_index.doc_type
class SubmitterDocument(DocType):
    name = fields.StringField()

    class Meta:
        model = Submitter
