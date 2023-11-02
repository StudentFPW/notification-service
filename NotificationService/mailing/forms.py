# from allauth.account.forms import SignupForm
# from django.contrib.auth.models import Group
#
#
# class CustomSignupForm(SignupForm):
#     """
#     The `CustomSignupForm` class is a subclass of `SignupForm` that adds
#     the user to the "common users" group upon saving.
#     """
#
#     def save(self, request):
#         user = super().save(request)
#         common_users = Group.objects.get(name="common users")
#         user.groups.add(common_users)
#         return user
