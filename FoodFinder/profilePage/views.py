from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import Profile  # Import the Profile model

@login_required
def profile_page(request):
    username = request.user.username
    first_name = request.user.first_name
    last_name = request.user.last_name
    
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        favorite_cusine = request.POST.get('favorite_cusine')
        profile.favorite_cusine = favorite_cusine
        profile.save()
        return redirect('profile')  

    context = {
        "greeting": f"hello {username}",
        "first_name": first_name,
        "last_name": last_name,
        "favorite_cusine": profile.favorite_cusine,  # Pass favorite_cusine to the template
        
    }

    return render(request, 'profile.html', context)
