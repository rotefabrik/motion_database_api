from django.conf.urls import url

from motion.views import LegacyAddView, MotionsView

urlpatterns = [
    url(r'^actions/add/?$', LegacyAddView.as_view(), name='actions_add'),
    url(r'^$', MotionsView.as_view(), name='motions'),
]