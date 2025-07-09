from src.utils.llm_utils import load_chat_model
from src.utils.env_utils import _set_environment_variables

_set_environment_variables()

if __name__ == "__main__":
    
    chain = load_chat_model("google")
    response = chain.invoke("hi, tell me a joke")
    print(response)
