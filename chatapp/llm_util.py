import yaml


# Load the YAML file
def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


# Function to dynamically import a class based on a string path (e.g., "langchain_community.chat_models.ChatOllama")
def get_class(class_path):
    module_path, class_name = class_path.rsplit(".", 1)
    module = __import__(module_path, fromlist=[class_name])
    return getattr(module, class_name)


# Open Language Model Server function
def open_llm(server_name):
    config = load_yaml("llms.yaml")
    for server in config["servers"]:
        if server["name"] == server_name:
            class_path = server["class"]
            clazz = get_class(class_path)
            # Remove 'class' and 'name' from the parameters as they're not needed for initialization
            params = {k: v for k, v in server.items() if k not in ["class", "name"]}
            params = {
                "model_id": "amazon.titan-text-express-v1",
                "model_kwargs": {"temperature": 0.1},
            }
            return clazz(**params)
    raise ValueError(f"Server '{server_name}' not found")
