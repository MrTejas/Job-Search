from dotenv import load_dotenv

load_dotenv()
import base64
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai
import re
# import argparse


# parser = argparse.ArgumentParser(description="Process four input arguments.")
# parser.add_argument("filepath1", type=str, help="Path to the input resume")
# parser.add_argument("function", type=str, help="The prompt key")
# parser.add_argument("filepath2", type=str, help="Path to the output response file")

# args = parser.parse_args()


def parse_resume(file_path,func):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    job_description_file = "./user_resume/jd.txt"
    try:
        with open(job_description_file, 'r') as file:
            job_description = file.read()
    except Exception as e:
        print(f"Error reading job description file: {e}")

    # file_path = args.filepath1
    # func = args.function
    # out_response_path = args.filepath2


    def get_gemini_response(input,pdf_cotent,prompt):
        model=genai.GenerativeModel('gemini-1.5-flash')
        response=model.generate_content([input,pdf_content[0],prompt])
        return response.text

    def input_pdf_setup(file_path):
        with open(file_path, 'rb') as uploaded_file:
            if uploaded_file is not None:
                images=pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path=r"C:\Program Files\poppler\Library\bin")
                first_page=images[0]
                img_byte_arr = io.BytesIO()
                first_page.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()

                pdf_parts = [
                    {
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
                    }
                ]
                return pdf_parts
            else:
                raise FileNotFoundError("No file uploaded")


    input_prompt1 = """
    You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements. Give the output in a json format (but as a string, i.e. do not add '''json ''' in the response). 
    """

    input_prompt2 = """
    You are an excellent resume parser. You have the task of reading a resume and telling (in text format) the main points about the resume. Try not leaving any essential detail about the candidate. The output
    should contain various aspects of the candidate that might get him/her hired, such as job experience, projects, coursework, grades, achievements, research_publications, 
    skills, proeficiency in languages, etc. Note that if some aspect is not present, there is no need to add it in the output. In addition to this, based on the past-experience and other factors, write if the user is INTERN, ENTRY-LEVEL, MID-LEVEL, JUNIOR, ASSOCIATE, SENIOR, MANAGER, DIRECTOR, EXECUTIVE, VICE PRESIDENT, CHIEF OFFICER.
    Do not leave out too much of the resume. Explain, in detail about each section. The output should be plain, without much format. Ignore the job description that i have given.
    """

    input_prompt3 = """
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
    your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
    the job description. First the output should come as percentage and then keywords missing and last final thoughts.  Give the output in a json format  (but as a string, i.e. do not add '''json ''' in the response). 
    """


    if func=="desc":
        if file_path is not None:
            pdf_content=input_pdf_setup(file_path)
            with open(job_description_file, 'r') as file:
                job_description = file.read()
                response=get_gemini_response(input_prompt1,pdf_content,job_description)
                response = '\n'.join(response.splitlines()[1:-1])
                # with open(out_response_path, 'w') as file:
                #     file.write(response)
                # print("written response at ",out_response_path)
                return response
        else:
            print("Please provide valid resume path")

    elif func=="text":
        if file_path is not None:
            pdf_content=input_pdf_setup(file_path)
            with open(job_description_file, 'r') as file:
                job_description = file.read()
                response=get_gemini_response(input_prompt2,pdf_content,job_description)
                response = '\n'.join(response.splitlines()[1:-1])
                # with open(out_response_path, 'w') as file:
                #     file.write(response)
                # print("written response at ",out_response_path)
                return response
        else:
            print("Please provide valid resume path")


    elif func=="score":
        if file_path is not None:
            pdf_content=input_pdf_setup(file_path)
            with open(job_description_file, 'r') as file:
                job_description = file.read()
                response=get_gemini_response(input_prompt3,pdf_content,job_description)
                response = '\n'.join(response.splitlines()[1:-1])
                # with open(out_response_path, 'w') as file:
                #     file.write(response)
                # print("written response at ",out_response_path)
                return response
        else:
            print("Please provide valid resume path")



   






def fun(a):
    print(a+1)
