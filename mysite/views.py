
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic  import TemplateView
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError





def index(request):
     return render(request,'index.html')
     
    # return HttpResponse('Home')

def analyze(request):

    djtext = request.POST.get('text','default')
    removepunc = request.POST.get('removepunc', 'off')
    Charcount = request.POST.get('Charcount', 'off')
    Capitalize = request.POST.get('Capitalize', 'off')
    NewLineRemover = request.POST.get('NewLineRemover', 'off')
    ExtraSpaceRemover = request.POST.get('ExtraSpaceRemover','off')
    # print(removepunc)
    # print(djtext)
    if removepunc == "on":
        punctutaion = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
        analyzed = ""
        for char in djtext:
            if char not in punctutaion:
                analyzed = analyzed + char

        # analyzed = djtext
        params = {'purpose':'remove punc', 'analyzed_text':analyzed}
        return render(request,'analyze.html', params)

    

    elif Charcount == "on":
        count = 0
        for char in djtext:
            count += 1
        charcountfun ="Total char is "+ str(count) 
        params = {'purpose':'charcount', 'analyzed_text':charcountfun}
        return render(request,'analyze.html', params)


    elif Capitalize == "on":
        text = str(djtext)
        cap = text.upper()
        
        params = {'purpose':'Capitalize', 'analyzed_text':cap}
        return render(request,'analyze.html', params)

    elif NewLineRemover == "on":
        # rem=djtext.replace("\n","")
        # rem=djtext.replace("\r","")
        #     # rem=print(char)
        
        # params = {'purpose':'NewLineRemover', 'analyzed_text':rem}
        # return render(request,'analyze.html', params)

        analyzed = ""
        for char in djtext:
            if char != "\n" and char!="\r":
                analyzed = analyzed + char
                
        params = {'purpose': 'Removed NewLines', 'analyzed_text':analyzed}
        print(params)
        # Analyze the text
        return render(request, 'analyze.html', params)





    elif ExtraSpaceRemover == "on":
        spc=djtext.replace("  ","")
            
        
        params = {'purpose':'ExtraSpaceRemover', 'analyzed_text':spc}
        return render(request,'analyze.html', params)

        


    else:
        return HttpResponse("Error")



#def contact(request):
    
        
    #return render(request,'contact.html')


def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry" 
			body = {
			'first_name': form.cleaned_data['first_name'], 
			'last_name': form.cleaned_data['last_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, 'dhruv7384@gmail.com', ['formationtext@gmail.com']) 
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ("index")
      
	form = ContactForm()
	return render(request, "contact.html", {'form':form})
        