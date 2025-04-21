# A dekorátorokhoz szükséges `wraps` segédfüggvény importálása, hogy megőrizze az eredeti függvény nevét és docstringjét
from functools import wraps

# Django válaszok és segédfüggvények importálása
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

        # Ha a felhasználó nincs bejelentkezve, átirányítja a login oldalra
        if not request.user.is_authenticated:
            return redirect('login')

        # Ha nem szuperuser, hibát dob vagy sablont renderel
        if not request.user.is_superuser:
            #return HttpResponseForbidden("You are not allowed to view this page.")
            return render(request, 'registration/forbidden.html', status=403)

        # Ha minden rendben, meghívja az eredeti nézetet
        return view_func(request, *args, **kwargs)

    # Visszatér a dekorátor által módosított függvénnyel
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

            # Ha a felhasználó nincs bejelentkezve, átirányítja a login oldalra
            if not request.user.is_authenticated:
                return redirect('login')

            # Ha nincs meg a szükséges engedély
            if not request.user.has_perm(perm):
                if raise_exception:
                    # Ha a `raise_exception=True`, akkor 403 hibát ad vissza
                    return HttpResponseForbidden("You do not have permission to view this page.")
                    # vagy használható egy egyedi sablon is:
                    # return render(request, 'registration/forbidden.html', status=403)

                # Ha nincs `raise_exception`, akkor visszairányítja az előző oldalra (vagy kezdőlapra)
                return redirect(request.META.get('HTTP_REFERER', '/'))

            # Jogosultság rendben, meghívja az eredeti nézetet
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
