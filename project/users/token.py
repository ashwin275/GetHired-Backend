from rest_framework_simplejwt.tokens import RefreshToken #type:ignore

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    refresh['name'] = user.first_name

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }