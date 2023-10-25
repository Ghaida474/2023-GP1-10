from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import FacultyStaff,Collage
from app.forms import updateFASform,previousworkform,ChangePasswordForm
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages import get_messages


@login_required
def dean_account_home (request):
    user = request.user
    collage_id = user.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
    staff = collage.nostaff 
    faculty = collage.nofaculty
    emp = staff + faculty
    count = len(collage.departments)

    context = {'user': user , 'collage':collage , "emp":emp , 'department':count }
    return render(request, 'dean/Home.html', context)
      
@login_required
def profile_view(request):
    user = request.user
    collage_id = user.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
    collagename = collage.name 
    context = {'user': user , 'collagename':collagename }
    return render(request, 'dean/profile.html' ,context) 

@login_required
def emptypage_view(request):
    user = request.user
    return render(request, 'dean/empty-page.html' ,{'user': user}) 

@login_required
def facultylist_view (request):
    user = request.user
    faculty = FacultyStaff.objects.filter(collageid =user.collageid)
    
    return render(request, 'dean/faculty-list.html', {'faculty' : faculty})

def view_file(request, user_id):
    # Retrieve the user based on the user_id
    user = get_object_or_404(FacultyStaff, pk=user_id)
    # Check if the user has a CV
    if user.cv:
        cv = user.cv  # Assuming that the CV field contains the binary CV data
        response = FileResponse(cv, content_type='application/pdf')  # Change content type accordingly
        response['Content-Disposition'] = f'inline; filename="{user.first_name}-CV.pdf"'  # Provide a filename
        return response

    # If the user doesn't have a CV or the CV is not found, return a 404 error
    raise Http404("CV not found")

@login_required
def editprofile_view(request):
    user = request.user
    form = updateFASform(instance=user)
    form2 = previousworkform()

    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        if form_type == 'form1': 
            form = updateFASform(request.POST, request.FILES, instance=user)   
            if form.is_valid():  
                cv_file = form.cleaned_data['cv']
                if cv_file is not None:
                    user.cv = cv_file.file.read()              
                
                form.save()
                return redirect('dean_account:profile')
            
        elif form_type == 'form2':  
            form2 = previousworkform(request.POST)  
            if form2.is_valid():
                previouswork = form2.cleaned_data['previouswork']
                researchinterest = form2.cleaned_data['researchinterest']

                if previouswork:
                    previous_work = user.previouswork or []
                    for item in previouswork:
                        pw = item
                    if len(pw) < 5 or pw.isdigit():
                         messages.error(request,'Previous Work must be at least 5 characters and not contain only digits.')
                    else: 
                        previous_work.extend(previouswork)
                        user.previouswork = previous_work
                        user.save()
                        return redirect('dean_account:edit-profile')
                   
                if researchinterest:
                    research_interest = user.researchinterest or []
                    for item in researchinterest:
                        ri = item
                    if len(ri) < 5 or ri.isdigit():
                        messages.error(request,'Research Interest must be at least 5 characters and not contain only digits.')
                    else:
                        research_interest.extend(researchinterest)
                        user.researchinterest = research_interest
                        user.save()
                        return redirect('dean_account:edit-profile')

    return render(request, 'dean/edit-profile.html', {'form': form ,'form2':form2, 'user' : user})


def delete_previouswork(request, value_to_delete):
    user = request.user

    if user.previouswork:
        if value_to_delete in user.previouswork:
            user.previouswork.remove(value_to_delete)
            user.save()
        else:
            messages.error(request, 'Value not found in previouswork.')
    else:
        messages.error(request, 'No previouswork values to delete.')

    return redirect('dean_account:edit-profile')


def delete_researchinterest(request, value_to_delete):
    user = request.user

    if user.researchinterest:
        if value_to_delete in user.researchinterest:
            user.researchinterest.remove(value_to_delete)
            user.save()
        else:
            messages.error(request, 'Value not found in previouswork.')
    else:
        messages.error(request, 'No researchinterest values to delete.')

    return redirect('dean_account:edit-profile')

@login_required
def changepassword_view(request):
    user = request.user
    form = ChangePasswordForm(user)
    
    if request.method == 'POST':
        print('here1')
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            # messages(request, 'Password changed successfully.') 
            return redirect('dean_account:profile')

    return render(request, 'dean/change-password.html', {'user': user, 'form': form})

@login_required
def facultyinfo_view(request,faculty_id):
    faculty_member = get_object_or_404(FacultyStaff, id=faculty_id)
    collage_id = faculty_member.collageid.collageid
    collage = Collage.objects.get(collageid=collage_id)
    collagename = collage.name 
    return render(request, 'dean/faculty-view.html', {'faculty_member': faculty_member , 'collagename': collagename})
