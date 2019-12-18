from rest_framework.permissions import BasePermission, SAFE_METHODS


class DonationsPermission(BasePermission):
    """
    readonly or edit only when donor
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.donor == request.user


class DonationsImagesPermission(BasePermission):
    """
    readonly or delete only when donor
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.donation.donor == request.user
