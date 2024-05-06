import streamlit as st
from openai import OpenAI
from os import getenv
from pygments.lexers import guess_lexer_for_filename
import magic
import os
from langdetect import detect
import google.generativeai as genai



# """# the function is used for saving the uploaded file on the UI to the backend for data collection."""
def sav_uploaded_file(uploaded_file):
    
    if uploaded_file is not None:
        file_name = uploaded_file.name
    # Save the file
        with open(file_name, "wb") as f:
            f.write(uploaded_file.getbuffer())

    file_path = os.path.abspath(file_name)        
    return file_path
        



# """Using "MAGIC" library for converting it into desired lang"""
# def get_file_content(uploaded_file_UI):
#     try:
#         # Detect the programming language
#         # uploadedfile = sav_uploaded_file(uploaded_file_UI)
#         print("uploadedfile,uploadedfile",uploadedfile)
#         # content = uploadedfile.read()
#         content = uploaded_file_UI.read()
#         print("content;;;", content)
#         mime = magic.Magic(mime=True)
#         file_type = mime.from_buffer(content)
#         print("file type;;;;;;", file_type)
#         language = file_type.split('/')[1] if '/' in file_type else None
#         # Reset the file pointer to the beginning
#         uploadedfile.seek(0)
#         # Read the file's text content
#         text_content = uploadedfile.getvalue()
#         return text_content
#     except Exception as e:
#         print("An error occurred:", e)




# """# This function helps in extracting the text of the uploaded file for further processing of the specfic function"""
def read_source_code(uploaded_file):
    # Check if a file was uploaded
    if uploaded_file is not None:
        # Read the contents of the file as bytes
        file_contents = uploaded_file.getvalue()
        # Decode the bytes to text assuming utf-8 encoding
        source_code = file_contents.decode("utf-8")
        return source_code
    else:
        return None



# """# make a custom function for detecting the source code of the uploaded file based on the file extension as the 
# # prebuild libraries could not work properly on 'RAW' files. I can also us them acording to my convience."""

def detect_language(uploaded_file):
    extension = uploaded_file.name.split(".")[-1]
    file_type = ""
    if extension=='py' or extension=='pynb' or extension=='ipynb':
        file_type = "Python"
    if extension=='java':  
        file_type  = 'Java'  
    if extension=='cpp':  
        file_type  = 'C'  

    if extension=='js':
        file_type = 'JavaScript'  
      
    return file_type           





# """functions identifis the function from the text chunk and then converts into specified language by calling LLM.
# # 'text of the file' , 'function to be processed' , 'source langauge' (llm can identify source language itself but i have provided it to lower the chance of halocination), and the 'target lang' as input and return the output code snippet.
# # the LLM model used here is "zephyr" from Hugging face as prescribd in the Assignment Document."""

def cnvtg_func_to_des_lang(text,function_name,source_language, target_language):


    # Now using Google GEMINI
    genai.configure(api_key = 'AIzaSyAQabjCLx3DVZHdZhC0fNbABlxnLFaRHso')


    model = genai.GenerativeModel('gemini-pro')
    # response = model.generate_content(f"""You’re an experienced software developer who takes joy in transferring code snippets from one 
    #                                   language to another. Your specialty lies in accurately identifying specific functions within code and 
    #                                   seamlessly converting them into another programming language.Your task is to convert a specified
    #                                    function within a given code snippet from {source_language} to {target_language}. Locate the function
    #                                      named "{function_name}" within the code, represented by the text: ###{text}###. Once found, convert 
    #                                      only the given function "{function_name}" and return the converted code. Carefully convert only the identified
    #                                        function "{function_name}". Remember, the goal is to bring precision and efficiency to this translation task.If the function "{function_name}"
    #                                        is not present in the code snippet, your response should be 'No such function'. Your output should strictly
    #                                          contain the converted function without any additional text or descriptions, ensuring a clean and concise
    #                                            result.In this process, ensure that the function conversion is accurate and reflects the 
    #                                            original logic appropriately. For example, when converting a function that calculates the
    #                                              square of a number in Python to Java, make sure that the syntax and
    #                                                logic match the original functionality with precision.Do not hallocinate.""")
    response = model.generate_content(f"""You’re an experienced software developer who takes joy in transferring code snippets from one 
                                      language to another.Your task is to find the "{function_name}" from within the code : 
                                      " {text} "
                                    and then convert the code for function "{function_name}"  from {source_language} to {target_language}. 
                                    Carefully convert only the identified function "{function_name}". Remember, the goal is to bring 
                                    precision and efficiency to this translation task.If the function "{function_name}" is not present 
                                    in the code snippet, your response should be "No such function". Your output should strictly
                                    contain the converted function without any additional text or descriptions, ensuring a clean and
                                    concise result.In this process, ensure that the function conversion is accurate and reflects the 
                                    original logic appropriately. For example, when converting a function that calculates the
                                    square of a number in Python to Java, make sure that the syntax and logic match the original 
                                    functionality with precision.""")
    result = response.text

    print("result g:::", result)


# HERE I WAS USING FREE MODELS FROM HUGGIN FACE BUT DUE TO LACK OF ACCURACY I HAVE CHAGED TO GEMINI. THE FUNCTIONS ARE JUST COMMENTED AND CAN BE REUSED
# AS SOON AS NEEDED JUST BY CHANGIG MODEL
    # promptMessage = [
    #              {"role":"system","content":"You’re an experienced software developer who takes joy in transferring code snippets from one language to another. Your specialty lies in accurately identifying specific functions within code and seamlessly converting them into another programming language."}, 
    #             #  {"role": "user", "content": f"You are provided with a code snippet in {source_language}. Your task is to locate the specified function within the code and convert it into {target_language} and return only converted code. The function name is {function_name}, and the corresponding code snippet is represented by the text: ###{text}###.Return only the specific function not whole file in result.If the function cannot be found, return 'No such function'.carefully Do not include any additional text or descriptions; return ONLY the code."}
    #             #  {"role": "user", "content": f"Your task is to convert a specified function within a given code snippet from {source_language} to {target_language}.Locate the function named {function_name} within the code, represented by the text: ###{text}###. Once found, convert only the identified function not whole program file and return the converted code.Carefully Convert only the identified function. Remember, the goal is to bring precision and efficiency to this translation task.If the function cannot be located within the code snippet, the response should be 'No such function'. Your output should strictly contain the converted function without any additional text or descriptions, ensuring a clean and concise result."}
    #              {"role": "user", "content": f"Your task is to convert a specified function within a given code snippet from {source_language} to {target_language}. Locate the function named {function_name} within the code, represented by the text: ###{text}###. Once found, convert only the identified function and return the converted code. Carefully convert only the identified function. Remember, the goal is to bring precision and efficiency to this translation task.If the function cannot be located within the code snippet, the response should be 'No such function'. Your output should strictly contain the converted function without any additional text or descriptions, ensuring a clean and concise result.In this process, ensure that the function conversion is accurate and reflects the original logic appropriately. For example, when converting a function that calculates the square of a number in Python to Java, make sure that the syntax and logic match the original functionality with precision.Do not hallocinate."}
    #          ]

    # client = OpenAI(
    #   base_url="https://openrouter.ai/api/v1",
    #   api_key= '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',
    # )

    # completion = client.chat.completions.create(

    # model="huggingfaceh4/zephyr-7b-beta:free",
    # messages=promptMessage,
    # )
    # print("reult;;")
    # print(completion.choices[0].message.content)
    # result = completion.choices[0].message.content
    

    return result





# """# This function identifies the function from source language and compare it to the converted language using an LLM call."""
def conversion_quality(source_language,target_language,function_name,text,converted_result):

    genai.configure(api_key = 'AIzaSyAQabjCLx3DVZHdZhC0fNbABlxnLFaRHso')

    model = genai.GenerativeModel('gemini-pro')

    # "role":"system","content":"You’re an experienced software developer who takes joy in transferring code snippets from one language to another. Your specialty lies in accurately identifying specific functions within code and seamlessly converting them into another programming language."}, 


    response = model.generate_content(f"""You’re a reliable code evaluator tasked with comparing functions from different programming languages 
                                      and determining the accuracy of their conversion.Your goal is to identify a specific function named {function_name} within a provided 
                                      code snippet in a language {source_language}. The function is denoted in the text as ###{text}###. Once 
                                      identified, your task is to compare this function with {converted_result}, which represents the same 
                                      function in {target_language} programming language. After the comparison, you must evaluate the 
                                      similarity between the two functions and rate it on a scale of 1 to 5, indicating how accurately 
                                      the code has been converted from the source language to the target language. Your final output must 
                                      only be the numeric rating, no additional text and no Explainations.For example, when I provide you 
                                      with code snippets in Python and Java, you need to locate the function named \"calculate_sum\" in Python 
                                      code and compare it with the equivalent function in Java. Then, based on how accurately the Python 
                                      function has been converted to Java, you should assign a rating ranging from 1 to 5 to show the 
                                      conversion quality.""")
    
    result = response.text

    print("result g2:::", result) 


# HERE I WAS USING FREE MODELS FROM HUGGIN FACE BUT DUE TO LACK OF ACCURACY I HAVE CHAGED TO GEMINI. THE FUNCTIONS ARE JUST COMMENTED AND CAN BE REUSED
# AS SOON AS NEEDED JUST BY CHANGIG MODEL 
    # promptMessage = [
    #         {"role":"system","content":"You’re a reliable code evaluator tasked with comparing functions from different programming languages and determining the accuracy of their conversion"},
    #         {"role": "user", "content": f"Your goal is to identify a specific function named {function_name} within a provided code snippet in a language {source_language}. The function is denoted in the text as ###{text}###. Once identified, your task is to compare this function with {converted_result}, which represents the same function in {target_language} programming language. After the comparison, you must evaluate the similarity between the two functions and rate it on a scale of 1 to 5, indicating how accurately the code has been converted from the source language to the target language. Your final output must only be the numeric rating, no additional text and no Explainations.For example, when I provide you with code snippets in Python and Java, you need to locate the function named \"calculate_sum\" in Python code and compare it with the equivalent function in Java. Then, based on how accurately the Python function has been converted to Java, you should assign a rating ranging from 1 to 5 to show the conversion quality."}
    #     ]
    
    # client = OpenAI(
    #   base_url="https://openrouter.ai/api/v1",
    #   api_key= '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',
    # )

    # completion = client.chat.completions.create(

    # model="huggingfaceh4/zephyr-7b-beta:free",
    # messages=promptMessage,
    # )
    # print("reult2;;")
    # print(completion.choices[0].message.content)
    # result = completion.choices[0].message.content
  

    return result    




    
def main():

    st.header("Source Code Converter :red[Assignment]")
    file_uploaded = st.file_uploader("Upload your Program File")
    st.sidebar.header("Submission Details:")
    st.sidebar.subheader("Submitted BY:   :blue[Shashank Srivastava]")
    st.sidebar.subheader("email ID:   :blue[srivastavashashank46@gmail.com]")

    try:
        
        sav_uploaded_file(file_uploaded)
        text_content = read_source_code(file_uploaded)
        # print('text content;;;;', text_content)
        source_langauge = detect_language(file_uploaded)
        st.write(f"The uploaded file is a :red[{source_langauge}] file")
        function_name = st.text_input("write the functions name ",key= 1)
        target_lang= st.text_input("Write the target language anme", key=2)
        result =  st.button("get results", key= 3)


        converted_result = cnvtg_func_to_des_lang(text_content,function_name,source_langauge, target_lang)
        score_of_convsn = conversion_quality(source_langauge,target_lang,function_name,text_content,converted_result)

        

        if result==True:
            st.code(converted_result)
            
            # print("""score""", score_of_convsn)
            st.subheader("Conversion Accuracy Score:")
            st.write(score_of_convsn)

    except:
        " "        



if __name__ == "__main__":
    main()

    