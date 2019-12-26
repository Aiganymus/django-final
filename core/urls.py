from core.views import AccountViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', AccountViewSet, basename='accounts')

urlpatterns = router.urls
