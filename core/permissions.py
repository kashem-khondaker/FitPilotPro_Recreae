from django.shortcuts import render
from rest_framework import permissions
from classes.models import FitnessClass, ClassBooking
from payments.models import Payment
from feedback.models import Feedback
from accounts.models import Profile

# Create your views here.

class IsVerifiedUser(permissions.BasePermission):
    """Only verified users can access the view."""
    message = "You must be a verified user to access this."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verified

class IsAdminOrStaff(permissions.BasePermission):
    """Admin and Staff users can access the view."""
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role in ['ADMIN', 'STAFF'] or request.user.is_superuser)

class IsAdminOrStaffOrReadOnly(permissions.BasePermission):
    """ only admin and staff can edit, others can only read """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'STAFF']

class IsMemberOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow members to edit their own objects."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'MEMBER'

class IsOwnerOrAdminStaff(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""
    message = "You do not have permission to edit this object."

    def has_object_permission(self, request, view, obj):
        # allow read-only access for all users
        if request.user.role in ['ADMIN', 'STAFF']:
            return True
            
        # only allow owners to edit their own objects
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'member'):
            return obj.member == request.user
        return False

class IsAdminOrStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Anyone (even anonymous) can read (GET, HEAD, OPTIONS)
    - Only Admin and Staff can create/update/delete
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role in ['ADMIN', 'STAFF'] or request.user.is_superuser

class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'MEMBER'

class IsMemberOrAdminStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user.role in ['ADMIN', 'STAFF', 'MEMBER']
        return False

    def has_object_permission(self, request, view, obj):
        # Members can only modify their own bookings
        if request.user.role == 'MEMBER':
            if isinstance(obj, ClassBooking):
                return obj.user == request.user
        return True


class ProfilePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user.role in ['ADMIN', 'STAFF', 'MEMBER']
        return False

    def has_object_permission(self, request, view, obj):
        # Members can only modify their own profile
        if request.user.role == 'MEMBER':
            if isinstance(obj, Profile):
                return obj.user == request.user
        return True


class FeedbackPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user.role in ['ADMIN', 'STAFF', 'MEMBER']
        return False

    def has_object_permission(self, request, view, obj):
        # Members can only modify their own feedback
        if request.user.role == 'MEMBER':
            if isinstance(obj, Feedback):
                return obj.user == request.user
        return True

class PaymentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user.role in ['ADMIN', 'STAFF', 'MEMBER']
        return False

    def has_object_permission(self, request, view, obj):
        # Members can only modify their own payments
        if request.user.role == 'MEMBER':
            if isinstance(obj, Payment):
                return obj.user == request.user
        # Staff and Admin can access all payments
        return request.user.role in ['ADMIN', 'STAFF']