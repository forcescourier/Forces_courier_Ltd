from django.shortcuts import render



# @login_required  --(add this when we star working with dashboard)--
# @user_passes_test(lambda u: u.is_superuser) --(add this when we star working with dashboard)--
def dashboard(request):
    return render(request, 'core/index.html')
