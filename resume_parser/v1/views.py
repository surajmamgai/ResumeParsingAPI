from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from v1.resumeparser import ResumeParser
import json
import os
import urllib.request

# Create your views here.
def home(request):
    return JsonResponse(status=status.HTTP_202_ACCEPTED,data={"message":"api working"})

@csrf_exempt
def extract(request):
    output = {}
    try:
        _status = status.HTTP_200_OK
        # print(request.body)
        if request.body:
            data = json.loads(request.body)
            # content_header = request.META.get('HTTP_CONTENT_DISPOSITION')
            # filename = content_header.split('filename=')[1].strip('"')
            url = data.get("resume",None)
            resume = os.path.basename(url)
            urllib.request.urlretrieve(url, "v1/resumes/" + resume)
            hobbies = ''
            language = ''
            pin_code = ''

            hobbies_list = []
            language_list = []
            pin_code_list = []

            # print(resume)
            # print('==========================================================')
            first_name = ''
            middle_name = ''
            last_name = ''
            dob = ''
            gender = ''
            nationality = ''
            marital_status = ''   
            passport = ''
            hobbies=''
            hobbies_list.clear()
            language = ''
            language_list.clear()
            address = ''
            landmark = ''
            state = ''
            pin_code = ''
            pin_code_list.clear()

            output = ResumeParser('resumes/'+resume).get_extracted_data()
            os.remove("v1/resumes/" + resume)
            name = output['full_name']
            dob = output['date_of_birth']
            hobbies_list = output['hobbies']
            language_list = output['languages']
            if type(output['pin']) == type([]):
                pin_code_list = output['pin']
                if len(pin_code_list)>0:  
                    pin_code = pin_code_list[0]   
                else: 
                    pin_code = 'NA'
            else:
                pin_code=output['pin']

            first_name = name[0]
            middle_name = name[1]
            last_name = name[2]
            dob = output['date_of_birth']
            gender = output['gender']
            nationality = output['nationality']
            marital_status = output['maritial_status']
            passport = output['passport_number']

            if len(hobbies_list)>0:

                for i in range(len(hobbies_list)):
                    hobbies = hobbies+hobbies_list[i]+","

            else:
                hobbies = 'NA'

            if len(language_list)>0:

                for i in range(len(language_list)):
                    language = language+language_list[i]+","

            else:
                language = 'NA'

            address = output['address']
            landmark = output['city']
            state = output['state']      
            mobile = output['mobile_number']
            email = output['email']

    except:
        _status = status.HTTP_400_BAD_REQUEST

    return JsonResponse(status=_status,data=output)
            