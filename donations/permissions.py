from rest_framework.permissions import BasePermission


class DonationsPermission(BasePermission):
    """
    edit only when donor
    """

    def has_object_permission(self, request, view, obj):
        return obj.donor == request.user
