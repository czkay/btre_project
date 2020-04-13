from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from contacts.models import Contact

# Create your views here.

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has already made this inquiry
        if request.user.is_authenticated:
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, "You have already an inquiry for this particular listing.")
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        # Disabled due to security issues in deployment
        # send_mail(
        #     'Property Listing Inquiry',
        #     'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info.',
        #     'chong.zi.kang@gmail.com',
        #     [realtor_email, 'chong.zi.kang@hotmail.com'],
        #     fail_silently=False
        # )

        messages.success(request, "Your inquiry has been submitted. A realtor will get back to you shortly.")
        return redirect('/listings/' + listing_id)
