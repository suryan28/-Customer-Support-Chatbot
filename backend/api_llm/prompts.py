class Prompts:
    @staticmethod
    def keywords_prompt_gen(user_query, keywords):
        sample_json = """
                    {
                    "answer": ["response"]                 
                    }
                    """
        prompt = [
            {
                "role": "system",
                "content":
                    f"Your task is to identify keywords from the 'user_query' to provide identified keywords form the 'KEYWORDS' list in responses.\n"
                    f"KEYWORDS: ###{keywords}###\n"
                    f"You must need to use 'KEYWORDS' list to check keywords from user_query.\n"
                    "Keep in mind: In 'KEYWORDS' list some keys have more then one words, so compare keywords in user query accordingly. What user_query is looking for.\n"
                    "Only identify the full keyword from the 'KEYWORDS' only if the 'user_query' have that full keyword in it.\n"
                    "IMPORTANT: Do not return keyword if sub key match for example: user_query - 'fund' it is not copletely matching with 'refund' similar for other\n"
                    f"Please always make sure 'user_query' can ask about multiple keywords which is present in keywords list, "
                    f"So check carefully and identify those keywords.\n"
                    "FOR EXAMPLE: user_query - 'can you tell me about string1 and string2'\n In this we have two "
                    "strings 'string1' and 'string2' which is present in provided list.\n"
                    "Then response should be only if keyword is present in user_query [string1, string2]"
                    "IMPORTANT: Always remember that If user_query is not match to keywords list then must return None in response .\n"
                    "Please return nothing but a JSON in the following format:\n"
                    f"{sample_json}\n"
            },
            {
                "role": "user",
                "content":
                    f"user_query: ###{user_query}###"
                    "user_query is inside two ### ###.\n"
            }
        ]
        print(prompt)
        return prompt

    @staticmethod
    def username_prompt_gen(data):
        sample_json = """
            {
            "answer": "response",
            "isvalid": "True or False"        
            }
            """
        prompt = [
            {
                "role": "system",
                "content": "You are a system designed to extract the name of the user from the user_query.\n"
            },
            {
                "role": "user",
                "content":
                    "Your task is to extract the name of the user from the user_query.\n"
                    f"user_query: ###{data}###\n"
                    "Be sure to only include the name of the user.\n"
                    "Set the 'isvalid' field to True or False, indicating whether the user query corresponds to the name of the user.\n"
                    "Ensure that the 'response' field only contains the generated response message, without introducing new information or generating fictional content.\n"
                    "Please return nothing but a JSON in the following format:\n"
                    f"{sample_json}\n"
            }
        ]

        return prompt

    @staticmethod
    def usertype_prompt_gen(data):
        sample_json = """
                    {
                        "answer": "response",   
                    }
                    """
        prompt = [
            {
                "role": "system",
                "content": "You are a system designed to identify the keywords from the user_query.\n"
            },
            {
                "role": "user",
                "content":
                    "Your task is to identify the keywords from the provided user_query.\n"
                    f"The user_query is: {data}.\n"
                    "The Only Possible keywords: [parent, coach, player, icc]\n"
                    "Extract the keywords from the user_query and check if they are form the possible keywords.\n"
                    "If other than the possible keywords or multiple keywords then"
                    """return : { "answer": "None" } in response.\n"""
                    "Must sure to match the exert keywords form the user_query\n"
                    "Ensure that the 'response' field only contains the generated response message, without "
                    "introducing new information or generating fictional content.\n"
                    "Please return nothing but a JSON in the following format:\n"
                    f"{sample_json}\n"
            }
        ]
        return prompt

    @staticmethod
    def sports_prompt_gen(data):
        sample_json = """
                            {
                            "answer": "response",
                            "isvalid": "True or False"        
                            }
                            """
        prompt = [
            {
                "role": "system",
                "content": "You are a system designed to identify the type of sports from the user_query.\n"
            },
            {
                "role": "user",
                "content":
                    "Your task is to identify the type of sports from the user_query.\n"
                    f"user_query is {data}.\n"
                    "Please return nothing but a JSON in the following format:\n"
                    f"{sample_json}\n"
                    "The possible sports types are: baseball, softball, and soccer.\n"
                    "Set the 'isvalid' field to True or False, indicating whether the user query corresponds to one of these sports ONLY.\n"
                    "Be sure to only include the type of sports.\n"
                    "If user_query is not from above types then give isvalid to 'False'.\n"
                    "The 'response' field should contain only the identified type of sport, and the output should exclusively consist of this generated response message without introducing new information or fictional content."
            }
        ]
        return prompt
