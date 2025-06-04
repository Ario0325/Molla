from .forms import LoginForm, RegisterForms

def auth_forms(request):
    return {
        'login_form': LoginForm(),
        'register_form': RegisterForms()
    }