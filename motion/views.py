import json

from elasticsearch_dsl import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from motion.documents import MotionDocument
from motion.serializers import MotionSerializer
from motion.tools import add_motion_from_json


class LegacyAddView(APIView):
    authentication_classes = []

    def post(self, request):
        json_data = json.loads(request.data.get('json'))
        motion = add_motion_from_json(json_data)
        return Response(motion.id)


class MotionsView(APIView):

    def get(self, request):
        search_options = json.loads(request.GET.get('search'))

        query = build_search_query(search_options)

        s = MotionDocument.search().query(query)[:30]
        qs = s.to_queryset()
        return Response(data=MotionSerializer(qs, many=True).data)


def build_search_query(search_options):
    if not search_options:
        return Q()

    query = Q("match", body=search_options.get('body', u'')) | Q("match", body=search_options.get('title', u''))

    # convention
    if search_options.get('convention_label'):
        query &= Q('term', convention__label=search_options.get('convention_label'))

    # section
    if search_options.get('section'):
        query &= Q('term', section__name=search_options.get('section'))

    # submitters
    if search_options.get('submitters'):
        query &= build_submitters_query(search_options.get('submitters'))

    # referrals
    if search_options.get('referrals'):
        query &= build_referrals_query(search_options.get('referrals'))

    # status
    if search_options.get('status'):
        query &= Q('term', status=search_options.get('status'))

    return query


def build_submitters_query(submitters):
    query_parts = []
    for submitter_name in submitters:
        term_query = Q('term', submitters__name=submitter_name)
        nested_query = Q('nested', path="submitters", query=term_query)
        query_parts.append(nested_query)
    return Q('bool', must=query_parts)


def build_referrals_query(submitters):
    query_parts = []
    for submitter_name in submitters:
        term_query = Q('term', referrals__name=submitter_name)
        nested_query = Q('nested', path="referrals", query=term_query)
        query_parts.append(nested_query)
    return Q('bool', must=query_parts)
