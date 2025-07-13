from rest_framework.routers import DefaultRouter

from .views import PolicyModelViewSet

router = DefaultRouter()
router.register(r"policies", PolicyModelViewSet, basename="policy")

urlpatterns = router.urls
