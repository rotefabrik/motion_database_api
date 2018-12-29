from django.conf.urls import url, include


urlpatterns = [
    url(r'^motions/?', include('motion.urls', namespace=u'motion')),
]
