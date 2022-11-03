from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import AdminViewSet, send_code, get_token, UserInfo

router_v1 = DefaultRouter()
router_v1.register('users', AdminViewSet)

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    PASS,
    basename='reviews'
)

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    PASS,
    basename='comments'

)

router_v1.register('genres', PASS, basename='genres')
router_v1.register('categories', PASS, basename='categories')
router_v1.register('titles', PASS, basename='titles')

urlpatterns = [
    path('v1/auth/signup/', send_code, name='get_email_code'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/users/me/', UserInfo.as_view(), name='user_info'),
    path('v1/', include(router_v1.urls))
    ]
