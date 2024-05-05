import streamlit as st
import openai
import os
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from gtts import gTTS 

# Handling API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
eleven_client = ElevenLabs(api_key = ELEVEN_API_KEY)
openai.api_key = OPENAI_API_KEY


def get_prompt(user_input, function):
    # The input should not have too many tokens
    safe_input = user_input[0:4000]
    
    # Prompt engineering
    # "(1) Default", "(2) Advice", "(3) Common mistake", "(4) Explain a word", "(5) A different way", "(7) IELTS Writing Task 2 answering", "(8) IELTS Writing Task 2 assessment", no "(6) Pronounce"
    prompt = f"""
    You are an AI system that serves as an English tutor. Your objective is to help users improve their English skill and achieve proficiency in English. You should provide corrections and initiate dialogues in English. In each step of the conversation, please provide corrections to the sentences.  
      
    User: "So during my English test, I would like to describe my daily routine in the office and my hobbies during my free time."  
      
    "Here's feedback on your previous message:  
      
    Original: "So during my English test, I would like to describe my daily routine in the office and my hobbies during my free time."  
      
    Corrected: "During my English test, I would like to describe my daily routine at the office and my hobbies in my free time."  
      
    Feedback:  
        Removed "So" from the beginning of the sentence because it's not necessary.  
        Changed "in the office" to "at the office" for more natural phrasing.  
        Changed "during my free time" to "in my free time" for a more natural expression.  
      
    Now, let's help you describe your daily routine at the office and your hobbies in your free time:  
      
    Daily routine at the office: Start by outlining the main tasks and responsibilities you have at work. Then, create a few sentences to describe your typical day which includes when you arrive at the office, any meetings you attend, tasks you complete, when you finish work for the day.  
      
    For example: "I usually arrive at the office at around 9 am and start by checking my emails. I often have meetings in the morning to discuss ongoing projects with my team. After lunch, I focus on my main tasks, such as analyzing data or writing reports. I finish work at around 6 pm."  
      
    Hobbies in your free time: Make a list of hobbies or activities that you enjoy doing in your free time. Then, create a few sentences to describe each hobby. Remember to include why you enjoy it and how often you do it.  
      
    For example: "In my free time, I enjoy reading novels which fall into the genres of science fiction or romance. I find it relaxing and a great way to reduce stress. I also like cycling at the weekend because it allows me to stay active."  
      
    Remember to practice speaking these sentences to become more comfortable describing your daily routine and hobbies in English."  
      
    User: "{safe_input}"
    """
    
    if function == "(2) Advice":
        prompt = f"""
        You are an AI system that serves as an English tutor. Your objective is to help users improve their English skill and achieve proficiency in English. The user will enter a topic and you will give a piece of advice related to that topic.  
          
        User: "What is the difference between "discrete" and "discreet"?"  
          
        ""Discrete" and "discreet" are two adjectives that are commonly confused. The two words are pronounced the same and are related in origin, but they have distinct meanings and should not be used interchangeably.  
          
        Discrete means "separate" or "distinct". It's used especially in mathematical and research contexts as the opposite of "continuous". For example: "Countable nouns refer to discrete entities, uncountable nouns to something more continuous or abstract."  
          
        Discreet is used to mean "inconspicuous", "cautious", or "discerning". It's used in less technical contexts, usually to describe people, actions, and things. For example: "Maria is always discreet in her behavior. She weighs up all the alternatives and avoids making any rash decisions.""  
          
        User: "{safe_input}"
        """
    elif function == "(3) Common mistake":
        prompt = f"""
        You are an AI system that serves as an English tutor. Your objective is to help users improve their English skill and achieve proficiency in English.  
        You will now explain a mistake that people often make while using English. Please complete this task.  
        """
    elif function == "(4) Explain a word":
        prompt = f"""
        You are an AI system that serves as an English tutor. Your objective is to help users improve their English skill and achieve proficiency in English. The user will enter a word or phrase. You will explain and use it in an example.  
          
        User: "bite the bullet"  
          
        "To "bite the bullet" is to force yourself to do something unpleasant or difficult, or to be brave in a difficult situation.  
          
        For example: "I hate going to the dentist, but I'll just have to bite the bullet.""  
          
        User: "{safe_input}"
        """
    elif function == "(5) A different way":
        prompt = f"""
        You are an AI system that serves as an English tutor. Your objective is to help users improve their English skill and achieve proficiency in English. The user will enter a sentence and you will provide a different way to convey its idea.  
          
        User: "The impact of climate change on coastal communities is profound."  
          
        "A different way to express that could be: "Coastal communities experience significant effects due to climate change.""  
          
        User: "{safe_input}"
        """
    elif function == "(7) IELTS Writing Task 2 answering":
        prompt = f"""
        The user will enter an IELTS Writing Task 2 question and a band score. Your objective is to answer the question so that you can get that band score.  
        The answer to an IELTS Writing Task 2 is assessed against the following criteria: task response, coherence and cohesion, lexical resource, grammatical range and accuracy.  
          
        Band 9:  
        Task response: The prompt is appropriately addressed and explored in depth. A clear and fully developed position is presented which directly answers the question. Ideas are relevant, fully extended and well supported. Any lapses in content or support are extremely rare.  
        Coherence and cohesion: The message can be followed effortlessly. Cohesion is used in such a way that it very rarely attracts attention. Any lapses in coherence or cohesion are minimal. Paragraphing is skilfully managed.  
        Lexical resource: Full flexibility and precise use are widely evident. A wide range of vocabulary is used accurately and appropriately with very natural and sophisticated control of lexical features. Minor errors in spelling and word formation are extremely rare and have minimal impact on communication.  
        Grammatical range and accuracy: A wide range of structures is used with full flexibility and control. Punctuation and grammar are used appropriately throughout. Minor errors are extremely rare and have minimal impact on communication.  
          
        Band 8:  
        Task response: The prompt is appropriately and sufficiently addressed. A clear and well-developed position is presented in response to the question. Ideas are relevant, well extended and supported. There may be occasional omissions or lapses in content.  
        Coherence and cohesion: The message can be followed with ease. Information and ideas are logically sequenced, and cohesion is well managed. Occasional lapses in coherence and cohesion may occur. Paragraphing is used sufficiently and appropriately.  
        Lexical resource: A wide resource is fluently and flexibly used to convey precise meanings. There is skilful use of uncommon and/or idiomatic items when appropriate, despite occasional inaccuracies in word choice and collocation. Occasional errors in spelling and/or word formation may occur, but have minimal impact on communication.  
        Grammatical range and accuracy: A wide range of structures is flexibly and accurately used. The majority of sentences are error-free, and punctuation is well managed. Occasional, non-systematic errors and inappropriacies occur, but have minimal impact on communication.  
          
        Band 7:  
        Task response: The main parts of the prompt are appropriately addressed. A clear and developed position is presented. Main ideas are extended and supported but there may be a tendency to over-generalise or there may be a lack of focus and precision in supporting ideas or materials.  
        Coherence and cohesion: Information and ideas are logically organised, and there is a clear progression throughout the response. A few lapses may occur, but these are minor. A range of cohesive devices including reference and substitution is used flexibly but with some inaccuracies or some overuse or underuse. Paragraphing is generally used effectively to support overall coherence, and the sequencing of ideas within a paragraph is generally logical.  
        Lexical resource: The resource is sufficient to allow some flexibility and precision. There is some ability to use less common and/or idiomatic items. An awareness of style and collocation is evident, though inappropriacies occur. There are only a few errors in spelling and/or word formation and they do not detract from overall clarity.  
        Grammatical range and accuracy: A variety of complex structures is used with some flexibility and accuracy. Grammar and punctuation are generally well controlled, and error-free sentences are frequent. A few errors in grammar may persist, but these do not impede communication.  
          
        Band 6:  
        Task response: The main parts of the prompt are addressed (though some may be more fully covered than others). An appropriate format is used. A position is presented that is directly relevant to the prompt, although the conclusions drawn may be unclear, unjustified or repetitive. Main ideas are relevant, but some may be insufficiently developed or may lack clarity, while some supporting arguments and evidence may be less relevant or inadequate.  
        Coherence and cohesion: Information and ideas are generally arranged coherently and there is a clear overall progression. Cohesive devices are used to some good effect but cohesion within and/or between sentences may be faulty or mechanical due to misuse, overuse or omission. The use of reference and substitution may lack flexibility or clarity and result in some repetition or error. Paragraphing may not always be logical and/or the central topic may not always be clear.  
        Lexical resource: The resource is generally adequate and appropriate for the task. The meaning is generally clear in spite of a rather restricted range or a lack of precision in word choice. If the writer is a risk-taker, there will be a wider range of vocabulary used but higher degrees of inaccuracy or inappropriacy. There are some errors in spelling and/or word formation, but these do not impede communication.  
        Grammatical range and accuracy: A mix of simple and complex sentence forms is used but flexibility is limited. Examples of more complex structures are not marked by the same level of accuracy as in simple structures. Errors in grammar and punctuation occur, but rarely impede communication.  
          
        Band 5:  
        Task response: The main parts of the prompt are incompletely addressed. The format may be inappropriate in places. The writer expresses a position, but the development is not always clear. Some main ideas are put forward, but they are limited and are not sufficiently developed and/or there may be irrelevant detail. There may be some repetition.  
        Coherence and cohesion: Organisation is evident but is not wholly logical and there may be a lack of overall progression. Nevertheless, there is a sense of underlying coherence to the response. The relationship of ideas can be followed but the sentences are not fluently linked to each other. There may be limited/overuse of cohesive devices with some inaccuracy. The writing may be repetitive due to inadequate and/or inaccurate use of reference and substitution. Paragraphing may be inadequate or missing.  
        Lexical resource: The resource is limited but minimally adequate for the task. Simple vocabulary may be used accurately but the range does not permit much variation in expression. There may be frequent lapses in the appropriacy of word choice and a lack of flexibility is apparent in frequent simplifications and/or repetitions. Errors in spelling and/or word formation may be noticeable and may cause some difficulty for the reader.  
        Grammatical range and accuracy: The range of structures is limited and rather repetitive. Although complex sentences are attempted, they tend to be faulty, and the greatest accuracy is achieved on simple sentences. Grammatical errors may be frequent and cause some difficulty for the reader. Punctuation may be faulty.  
          
        Band 4:  
        Task response: The prompt is tackled in a minimal way, or the answer is tangential, possibly due to some misunderstanding of the prompt. The format may be inappropriate. A position is discernible, but the reader has to read carefully to find it. Main ideas are difficult to identify and such ideas that are identifiable may lack relevance, clarity and/or support. Large parts of the response may be repetitive.  
        Coherence and cohesion: Information and ideas are evident but not arranged coherently and there is no clear progression within the response. Relationships between ideas can be unclear and/or inadequately marked. There is some use of basic cohesive devices, which may be inaccurate or repetitive. There is inaccurate use or a lack of substitution or referencing. There may be no paragraphing and/or no clear main topic within paragraphs.  
        Lexical resource: The resource is limited and inadequate for or unrelated to the task. Vocabulary is basic and may be used repetitively. There may be inappropriate use of lexical chunks (e.g. memorised phrases, formulaic language and/or language from the input material). Inappropriate word choice and/or errors in word formation and/or in spelling may impede meaning.  
        Grammatical range and accuracy: A very limited range of structures is used. Subordinate clauses are rare and simple sentences predominate. Some structures are produced accurately but grammatical errors are frequent and may impede meaning. Punctuation is often faulty or inadequate.  
          
        Band 3:  
        Task response: No part of the prompt is adequately addressed, or the prompt has been misunderstood. No relevant position can be identified, and/or there is little direct response to the question/s. There are few ideas, and these may be irrelevant or insufficiently developed.  
        Coherence and cohesion: There is no apparent logical organisation. Ideas are discernible but difficult to relate to each other. There is minimal use of sequencers or cohesive devices. Those used do not necessarily indicate a logical relationship between ideas. There is difficulty in identifying referencing. Any attempts at paragraphing are unhelpful.  
        Lexical resource: The resource is inadequate (which may be due to the response being significantly underlength). Possible over-dependence on input material or memorised language. Control of word choice and/or spelling is very limited, and errors predominate. These errors may severely impede meaning.  
        Grammatical range and accuracy: Sentence forms are attempted, but errors in grammar and punctuation predominate (except in memorised phrases or those taken from the input material). This prevents most meaning from coming through. Length may be insufficient to provide evidence of control of sentence forms.  
          
        Band 2:  
        Task response: The content is barely related to the prompt. No position can be identified. There may be glimpses of one or two ideas without development.  
        Coherence and cohesion: There is little relevant message, or the entire response may be off-topic. There is little evidence of control of organisational features.  
        Lexical resource: The resource is extremely limited with few recognisable strings, apart from memorised phrases. There is no apparent control of word formation and/or spelling.  
        Grammatical range and accuracy: There is little or no evidence of sentence forms (except in memorised phrases).  
          
        Band 1:  
        Task response: Responses of 20 words or fewer are rated at Band 1. The content is wholly unrelated to the prompt. Any copied rubric must be discounted.  
        Coherence and cohesion: Responses of 20 words or fewer are rated at Band 1. The writing fails to communicate any message and appears to be by a virtual non-writer.  
        Lexical resource: Responses of 20 words or fewer are rated at Band 1. No resource is apparent, except for a few isolated words.  
        Grammatical range and accuracy: Responses of 20 words or fewer are rated at Band 1. No rateable language is evident.  
          
        Band 0:  
        Should only be used where a candidate did not attend or attempt the question in any way, used a language other than English, or where there is proof that a candidate’s answer has been totally memorised.  
          
        User: "{safe_input}"
        """
    elif function == "(8) IELTS Writing Task 2 assessment":
        prompt = f"""
        The user will enter an IELTS Writing Task 2 question and answer. Your objective is to provide an assessment and a band score.  
        The answer to an IELTS Writing Task 2 is assessed against the following criteria: task response, coherence and cohesion, lexical resource, grammatical range and accuracy.  
          
        Band 9:  
        Task response: The prompt is appropriately addressed and explored in depth. A clear and fully developed position is presented which directly answers the question. Ideas are relevant, fully extended and well supported. Any lapses in content or support are extremely rare.  
        Coherence and cohesion: The message can be followed effortlessly. Cohesion is used in such a way that it very rarely attracts attention. Any lapses in coherence or cohesion are minimal. Paragraphing is skilfully managed.  
        Lexical resource: Full flexibility and precise use are widely evident. A wide range of vocabulary is used accurately and appropriately with very natural and sophisticated control of lexical features. Minor errors in spelling and word formation are extremely rare and have minimal impact on communication.  
        Grammatical range and accuracy: A wide range of structures is used with full flexibility and control. Punctuation and grammar are used appropriately throughout. Minor errors are extremely rare and have minimal impact on communication.  
          
        Band 8:  
        Task response: The prompt is appropriately and sufficiently addressed. A clear and well-developed position is presented in response to the question. Ideas are relevant, well extended and supported. There may be occasional omissions or lapses in content.  
        Coherence and cohesion: The message can be followed with ease. Information and ideas are logically sequenced, and cohesion is well managed. Occasional lapses in coherence and cohesion may occur. Paragraphing is used sufficiently and appropriately.  
        Lexical resource: A wide resource is fluently and flexibly used to convey precise meanings. There is skilful use of uncommon and/or idiomatic items when appropriate, despite occasional inaccuracies in word choice and collocation. Occasional errors in spelling and/or word formation may occur, but have minimal impact on communication.  
        Grammatical range and accuracy: A wide range of structures is flexibly and accurately used. The majority of sentences are error-free, and punctuation is well managed. Occasional, non-systematic errors and inappropriacies occur, but have minimal impact on communication.  
          
        Band 7:  
        Task response: The main parts of the prompt are appropriately addressed. A clear and developed position is presented. Main ideas are extended and supported but there may be a tendency to over-generalise or there may be a lack of focus and precision in supporting ideas or materials.  
        Coherence and cohesion: Information and ideas are logically organised, and there is a clear progression throughout the response. A few lapses may occur, but these are minor. A range of cohesive devices including reference and substitution is used flexibly but with some inaccuracies or some overuse or underuse. Paragraphing is generally used effectively to support overall coherence, and the sequencing of ideas within a paragraph is generally logical.  
        Lexical resource: The resource is sufficient to allow some flexibility and precision. There is some ability to use less common and/or idiomatic items. An awareness of style and collocation is evident, though inappropriacies occur. There are only a few errors in spelling and/or word formation and they do not detract from overall clarity.  
        Grammatical range and accuracy: A variety of complex structures is used with some flexibility and accuracy. Grammar and punctuation are generally well controlled, and error-free sentences are frequent. A few errors in grammar may persist, but these do not impede communication.  
          
        Band 6:  
        Task response: The main parts of the prompt are addressed (though some may be more fully covered than others). An appropriate format is used. A position is presented that is directly relevant to the prompt, although the conclusions drawn may be unclear, unjustified or repetitive. Main ideas are relevant, but some may be insufficiently developed or may lack clarity, while some supporting arguments and evidence may be less relevant or inadequate.  
        Coherence and cohesion: Information and ideas are generally arranged coherently and there is a clear overall progression. Cohesive devices are used to some good effect but cohesion within and/or between sentences may be faulty or mechanical due to misuse, overuse or omission. The use of reference and substitution may lack flexibility or clarity and result in some repetition or error. Paragraphing may not always be logical and/or the central topic may not always be clear.  
        Lexical resource: The resource is generally adequate and appropriate for the task. The meaning is generally clear in spite of a rather restricted range or a lack of precision in word choice. If the writer is a risk-taker, there will be a wider range of vocabulary used but higher degrees of inaccuracy or inappropriacy. There are some errors in spelling and/or word formation, but these do not impede communication.  
        Grammatical range and accuracy: A mix of simple and complex sentence forms is used but flexibility is limited. Examples of more complex structures are not marked by the same level of accuracy as in simple structures. Errors in grammar and punctuation occur, but rarely impede communication.  
          
        Band 5:  
        Task response: The main parts of the prompt are incompletely addressed. The format may be inappropriate in places. The writer expresses a position, but the development is not always clear. Some main ideas are put forward, but they are limited and are not sufficiently developed and/or there may be irrelevant detail. There may be some repetition.  
        Coherence and cohesion: Organisation is evident but is not wholly logical and there may be a lack of overall progression. Nevertheless, there is a sense of underlying coherence to the response. The relationship of ideas can be followed but the sentences are not fluently linked to each other. There may be limited/overuse of cohesive devices with some inaccuracy. The writing may be repetitive due to inadequate and/or inaccurate use of reference and substitution. Paragraphing may be inadequate or missing.  
        Lexical resource: The resource is limited but minimally adequate for the task. Simple vocabulary may be used accurately but the range does not permit much variation in expression. There may be frequent lapses in the appropriacy of word choice and a lack of flexibility is apparent in frequent simplifications and/or repetitions. Errors in spelling and/or word formation may be noticeable and may cause some difficulty for the reader.  
        Grammatical range and accuracy: The range of structures is limited and rather repetitive. Although complex sentences are attempted, they tend to be faulty, and the greatest accuracy is achieved on simple sentences. Grammatical errors may be frequent and cause some difficulty for the reader. Punctuation may be faulty.  
          
        Band 4:  
        Task response: The prompt is tackled in a minimal way, or the answer is tangential, possibly due to some misunderstanding of the prompt. The format may be inappropriate. A position is discernible, but the reader has to read carefully to find it. Main ideas are difficult to identify and such ideas that are identifiable may lack relevance, clarity and/or support. Large parts of the response may be repetitive.  
        Coherence and cohesion: Information and ideas are evident but not arranged coherently and there is no clear progression within the response. Relationships between ideas can be unclear and/or inadequately marked. There is some use of basic cohesive devices, which may be inaccurate or repetitive. There is inaccurate use or a lack of substitution or referencing. There may be no paragraphing and/or no clear main topic within paragraphs.  
        Lexical resource: The resource is limited and inadequate for or unrelated to the task. Vocabulary is basic and may be used repetitively. There may be inappropriate use of lexical chunks (e.g. memorised phrases, formulaic language and/or language from the input material). Inappropriate word choice and/or errors in word formation and/or in spelling may impede meaning.  
        Grammatical range and accuracy: A very limited range of structures is used. Subordinate clauses are rare and simple sentences predominate. Some structures are produced accurately but grammatical errors are frequent and may impede meaning. Punctuation is often faulty or inadequate.  
          
        Band 3:  
        Task response: No part of the prompt is adequately addressed, or the prompt has been misunderstood. No relevant position can be identified, and/or there is little direct response to the question/s. There are few ideas, and these may be irrelevant or insufficiently developed.  
        Coherence and cohesion: There is no apparent logical organisation. Ideas are discernible but difficult to relate to each other. There is minimal use of sequencers or cohesive devices. Those used do not necessarily indicate a logical relationship between ideas. There is difficulty in identifying referencing. Any attempts at paragraphing are unhelpful.  
        Lexical resource: The resource is inadequate (which may be due to the response being significantly underlength). Possible over-dependence on input material or memorised language. Control of word choice and/or spelling is very limited, and errors predominate. These errors may severely impede meaning.  
        Grammatical range and accuracy: Sentence forms are attempted, but errors in grammar and punctuation predominate (except in memorised phrases or those taken from the input material). This prevents most meaning from coming through. Length may be insufficient to provide evidence of control of sentence forms.  
          
        Band 2:  
        Task response: The content is barely related to the prompt. No position can be identified. There may be glimpses of one or two ideas without development.  
        Coherence and cohesion: There is little relevant message, or the entire response may be off-topic. There is little evidence of control of organisational features.  
        Lexical resource: The resource is extremely limited with few recognisable strings, apart from memorised phrases. There is no apparent control of word formation and/or spelling.  
        Grammatical range and accuracy: There is little or no evidence of sentence forms (except in memorised phrases).  
          
        Band 1:  
        Task response: Responses of 20 words or fewer are rated at Band 1. The content is wholly unrelated to the prompt. Any copied rubric must be discounted.  
        Coherence and cohesion: Responses of 20 words or fewer are rated at Band 1. The writing fails to communicate any message and appears to be by a virtual non-writer.  
        Lexical resource: Responses of 20 words or fewer are rated at Band 1. No resource is apparent, except for a few isolated words.  
        Grammatical range and accuracy: Responses of 20 words or fewer are rated at Band 1. No rateable language is evident.  
          
        Band 0:  
        Should only be used where a candidate did not attend or attempt the question in any way, used a language other than English, or where there is proof that a candidate’s answer has been totally memorised.  
          
        User: "{safe_input}"
        """
    return prompt


def main():
    st.title("AI English Tutor 😎")    
    st.write("""
    Hello!  
    I am an AI system serving as a tutor.  
    My goal is to help you achieve proficiency in English. 🚀🔥  
      
    You can change the voice and the function using the drop-down menus below.  
    (1) Default: You can initiate dialogues and I will respond. During our conversation, I will provide corrections and suggestions in order to help you improve your English skills.  
    (2) Advice: You can enter a topic and I will give you a piece of advice related to that topic.  
    (3) Common mistake: I will explain a mistake that people often make while using English.  
    (4) Explain a word: You can enter a word or phrase. I will explain it and use it in an example.  
    (5) A different way: You can enter a sentence and I will provide a different way to convey its idea.  
    (6) Pronounce: You can enter something and I will pronounce it.  
      
    (7) IELTS Writing Task 2 answering: You can enter an IELTS Writing Task 2 question and a band score. I will answer the question while targeting that band score.  
    (8) IELTS Writing Task 2 assessment: You can enter an IELTS Writing Task 2 question and answer. I will provide an assessment and a band score.
    """)
    
    voice = st.selectbox(
        "Select a voice: ",
        ["Rachel", "Domi", "Bella", "Antoni", "Elli", "Josh", "Arnold", "Adam", "Sam"]
    )
    
    function = st.selectbox(
        "Select a function: ",
        ["(1) Default", "(2) Advice", "(3) Common mistake", "(4) Explain a word", "(5) A different way", "(6) Pronounce", "(7) IELTS Writing Task 2 answering", "(8) IELTS Writing Task 2 assessment"]
    )
    
    user_input = st.text_area("Enter your input in English: ")

    if st.button('Submit'):
        try:
            lesson = user_input
            if function != "(6) Pronounce":
                # Append the input to the prompt
                prompt = get_prompt(user_input, function)
                
                # Generate a response
                response = openai.chat.completions.create(
                    model = "gpt-3.5-turbo", 
                    messages = [
                        {"role": "system", "content": prompt}
                    ]
                )
                lesson = response.choices[0].message.content
                
                # Print the response
                st.write(lesson)
            
            # Convert the response into audio
            myobj = gTTS(text = lesson, lang = "en", slow = False)
            myobj.save("gtts_lesson.mp3")
            st.audio(data = "gtts_lesson.mp3")
            
            if ELEVEN_API_KEY != "your-elevenlabs-api-key":
                audio = eleven_client.generate(text = lesson, voice = voice, model = "eleven_monolingual_v1")
                save(audio, "eleven_lesson.mp3")
                st.audio(data = "eleven_lesson.mp3")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
