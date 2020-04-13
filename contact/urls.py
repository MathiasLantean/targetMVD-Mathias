from rest_framework import routers

from contact.views import InformationDetail, SendQuestion

router = routers.SimpleRouter()
router.register(r'information', InformationDetail, basename='info')
router.register(r'questions', SendQuestion, basename='send-question')

urlpatterns = router.urls
