from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register("interval", IntervalView, basename="interval")

urlpatterns = router.urls