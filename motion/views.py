import json

from django.http import Http404
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import MoreLikeThis
from rest_framework.response import Response
from rest_framework.views import APIView

from motion.documents import MotionDocument
from motion.models import Motion
from motion.serializers import MotionSerializer
from motion.tools import add_motion_from_json

DEFAULT_PAGE = 1
DEFAULT_PAGE_ITEMS = 30


class LegacyAddView(APIView):
    authentication_classes = []

    def post(self, request):
        json_data = json.loads(request.data.get('json'))
        motion = add_motion_from_json(json_data)
        return Response(motion.id)


class MotionsView(APIView):

    def get(self, request):
        search_options = json.loads(request.GET.get('search'))
        page = int(request.GET.get('page', DEFAULT_PAGE)) - 1
        page_items = int(request.GET.get('pageItems', DEFAULT_PAGE_ITEMS))

        query = build_search_query(search_options)

        index_from = page * page_items
        index_to = index_from + page_items

        sort_options = ['-convention.year', '-convention.slot']

        s = MotionDocument.search().sort(*sort_options).query(query)[index_from:index_to]
        qs = s.to_queryset()
        data = {
            'page': page,
            'page_items': page_items,
            'items': MotionSerializer(qs, many=True).data,
            'total': s.count()
        }
        return Response(data=data)


def build_search_query(search_options):
    query = None

    if not search_options or search_options.get('body') in [u'', None]:
        query = Q()
    else:
        query = Q("multi_match", query=search_options.get('body', u''), fields=['title', 'body'])

    # convention
    if search_options.get('convention'):
        query &= build_convention_query(search_options.get('convention'))

    # section
    if search_options.get('section'):
        query &= build_section_query(search_options.get('section'))

    # submitters
    if search_options.get('submitters'):
        query &= build_submitters_query(search_options.get('submitters'))

    # referrals
    if search_options.get('referred'):
        query &= build_referred_query(search_options.get('referred'))

    # status
    if search_options.get('status'):
        query &= build_status_query(search_options.get('status'))

    return query


def build_section_query(sections):
    query_parts = []
    for section_name in sections:
        query_parts.append(Q('term', section__name=section_name))
    return Q('bool', must=query_parts)


def build_convention_query(conventions):
    query_parts = []
    for convention_label in conventions:
        query_parts.append(Q('term', convention__label=convention_label))
    return Q('bool', must=query_parts)


def build_submitters_query(submitters):
    query_parts = []
    for submitter_name in submitters:
        term_query = Q('term', submitters__name=submitter_name)
        nested_query = Q('nested', path="submitters", query=term_query)
        query_parts.append(nested_query)
    return Q('bool', must=query_parts)


def build_referred_query(submitters):
    query_parts = []
    for submitter_name in submitters:
        term_query = Q('term', referrals__name=submitter_name)
        nested_query = Q('nested', path="referrals", query=term_query)
        query_parts.append(nested_query)
    return Q('bool', must=query_parts)


def build_status_query(allowed_statuus):
    query_parts = []
    for status in allowed_statuus:
        query_parts.append(Q('term', status=status))
    return Q('bool', should=query_parts, minimum_should_match=1)


class MotionView(APIView):

    def get(self, request, pk=None):
        if pk is None:
            raise Http404()
        try:
            motion = Motion.objects.get(pk=pk)
        except Motion.DoesNotExist:
            raise Http404()
        return Response(data=MotionSerializer(motion).data)
