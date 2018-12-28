from django.conf.urls import url

from motion.views import LegacyAddView, MotionsView, MotionView


urlpatterns = [
    url(r'^actions/add/?$', LegacyAddView.as_view(), name='actions_add'),
    url(r'^(?P<pk>[0-9]+)/?$', MotionView.as_view(), name='motions'),
    url(r'^$', MotionsView.as_view(), name='motions'),
]
