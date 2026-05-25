from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader(input_files=["C:\Users\jakak\Desktop\Diplomska\backend\scraper\test6.json"]).load_data()