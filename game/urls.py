from rest_framework import routers
from .api import MachineViewSet, RetailViewSet, ShopViewSet, TransactionViewSet, UserViewSet

router = routers.DefaultRouter()

router.register('api/machine', MachineViewSet, 'machines')
router.register('api/user', UserViewSet, 'users')
router.register('api/retail', RetailViewSet, 'retails')
router.register('api/shop', ShopViewSet, 'shops')
router.register('api/transaction', TransactionViewSet, 'transactions')

urlpatterns = router.urls
