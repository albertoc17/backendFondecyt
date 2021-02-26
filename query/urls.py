from rest_framework import routers

from .viewsets import BookViewSet, QueryApiViewSet

router = routers.SimpleRouter()
router.register('books', BookViewSet)
router.register('querys', QueryApiViewSet)

urlpatterns = router.urls

