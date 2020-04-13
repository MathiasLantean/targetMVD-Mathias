from rest_framework import routers

from contact.views import InformationDetail

router = routers.SimpleRouter()
router.register(r'information', InformationDetail, basename='info')

urlpatterns = router.urls
