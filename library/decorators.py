from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

# ===========================
# Dekorátor: csak szuperfelhasználók láthatják az adott nézetet
# ===========================
def superuser_required(view_func):
    # A belső függvény fogja lecserélni az eredeti nézetet
    def _wrapped_view(request, *args, **kwargs):
        # Debug: kiírja az aktuális nézetet és a kérés adatait
        print(view_func)
        print(request)
        print(args)
        print(kwargs)
        print(request.user)
        print('auth', request.user.is_authenticated)
        print('super', request.user.is_superuser)


        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_superuser:
            return render(request, 'registration/forbidden.html', status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ===========================
# Dekorátor: adott jogosultság meglétét ellenőrzi
# ===========================
def custom_permission_required(perm, login_url=None, raise_exception=False):
    # Ez a dekorátor egy paraméterezett dekorátor (perm = engedély neve)
    def decorator(view_func):
        @wraps(view_func)  # Megőrzi az eredeti függvény metainformációit
        def _wrapped_view(request, *args, **kwargs):
            # Debug információk kiírása
            print(view_func)
            print(request)
            print(args)
            print(kwargs)
            print(request.user)
            print('auth', request.user.is_authenticated)
            print('super', request.user.is_superuser)
            # print(request.user.has_perm('can_view_customer'))

            # Az aktuális felhasználó jogosultságainak lekérése
            user_permissions = request.user.get_user_permissions()
            print(f"User permissions: {user_permissions}")

            if not request.user.is_authenticated:
                return redirect('login')
            if not request.user.has_perm(perm):
                if raise_exception:
                    return HttpResponseForbidden("You do not have permission to view this page.")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
