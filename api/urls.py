from django.urls import path , include
from rest_framework.routers import DefaultRouter
from classes.views import FitnessClassViewSet, ClassBookingViewSet
from memberships.views import MembershipPlanViewSet, MembershipViewSet
from payments.views import PaymentViewSet
from feedback.views import FeedbackViewSet
from attendance.views import AttendanceViewSet
from reports.views import ReportViewSet
from accounts.views import UserProfileView

router = DefaultRouter()

# router.register(r'users/profile', UserProfileView, basename='userprofile')
router.register(r'fitness_classes', FitnessClassViewSet, basename='fitnessclass') # ok 
router.register(r'class_bookings', ClassBookingViewSet, basename='classbooking') # ok 
router.register(r'membership_plans', MembershipPlanViewSet, basename='membershipplan') # ok 
router.register(r'memberships', MembershipViewSet, basename='membership') # ok
router.register(r'payments', PaymentViewSet, basename='payment') # ok
router.register(r'feedbacks', FeedbackViewSet, basename='feedback') # ok 
router.register(r'attendances', AttendanceViewSet, basename='attendance') # 
# router.register(r'reports', ReportViewSet, basename='report') #


urlpatterns = [
    path('' , include(router.urls)),
    path('auth/' , include('djoser.urls')),
    path('auth/' , include('djoser.urls.jwt')),
]



# /users/

# /users/me/

# /users/resend_activation/

# /users/set_password/

# /users/reset_password/

# /users/reset_password_confirm/

# /users/set_username/

# /users/reset_username/

# /users/reset_username_confirm/

# /token/login/ (Token Based Authentication)

# /token/logout/ (Token Based Authentication)

# /jwt/create/ (JSON Web Token Authentication)

# /jwt/refresh/ (JSON Web Token Authentication)

# /jwt/verify/ (JSON Web Token Authentication)