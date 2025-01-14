import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
from llamaapi import LlamaAPI
from agents.prompts import SYSTEM_PROMPT, USER_PROMPT, FAILED_MESSAGE

class LlamaSpymaster():
    def __init__(
        self,
        # model_id="meta-llama/Llama-3.2-3B-Instruct"
        model_id="llama3.1-8b",
        api_key="LA-ab3f8483f8dc4606b11f5d8c690d3f240da98970c45f4b74aafa9fc3c5f435e6"
    ):
        # self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        # self.model = AutoModelForCausalLM.from_pretrained(model_id)
        # self.device="cuda"
        # self.model = self.model.to_device(self.device)
        print("Loading LLamaAPI")
        self.llama = LlamaAPI(api_key)
        print("Loaded")
        self.model = model_id

    def _get_response(
        self,
        messages
    ):
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        )
        input_ids = input_ids.to_device(self.device)
        # input_ids = self.tokenizer(input_ids)
        generated_tokens = self.model.generate(
            input_ids,
            max_new_tokens=1000,
            temperature=0.3,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        # generated_tokens = self.model.generate(**input_ids)
        return generated_tokens
    

    def get_response(
        self,
        messages
    ):
        request = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        response = self.llama.run(request)
        return response

    def make_clue(
        self,
        good_words,
        bad_words
    ):
        print("Making clue")
        run_prompt = USER_PROMPT
        run_prompt += "\n\n\nGOOD WORDS:\n"
        for word in good_words:
            run_prompt += word + "\n"
        run_prompt += "\n"
        run_prompt += "BAD WORDS:\n"
        for word in bad_words:
            run_prompt += word + "\n"
        run_prompt += "\n"
        run_prompt += "RESPONSE:"

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": run_prompt.strip()}
        ]

        failed = True
        while failed:
            print(f"GENERATING FOR MESSAGES")
            for message in messages:
                print(message)
            response = self.get_response(messages)
            print("RESPONSE")
            print(type(response), response)
            response = response.text
            print("TEXT")
            print(response)

            response = json.loads(response)
            response = response["choices"][0]["message"]["content"]
            print(type(response), response)

            try:
                response = json.loads(response)
            except:
                print("FAILED TO READ RESPONSE. TRYING AGAIN.")
                messages.append({"role": "assistant", "content": response.strip()})
                messages.append({"role": "user", "content": FAILED_MESSAGE})
                failed = True
            else:
                print("GOT VALID RESPONSE")
                condition1 = len(response) == 2
                condition2 = "selected_words" in response and "clue" in response
                if condition1 and condition2:
                    print("RESPONSE KEYS ARE VALID")
                    failed = False
                else:
                    print("RESPONSE KEYS ARE INVALID:")
                    print(response)
                    failed = False

        return response


if __name__ == "__main__":
    spymaster = LlamaSpymaster()
    clue = spymaster.make_clue(
        good_words=["ambulance", "stick", "queen", "cycle", "satellite", "grace", "mouse", "diamond", "casino"],
        bad_words=["berry", "watch", "air", "parachute", "line", "rock", "stadium", "bottle", "thumb", "foot", "himalayas", "part", "kid", "piano", "belt", "lawyer"]
    )
    print("CLUE:", clue)