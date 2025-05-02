##  Installation 
```bash

Clone the Repository:
git clone https://github.com/SurajSivakumar07/ai_avathar
cd ai_avathar
 ```

## Install Dependencies:
```bash

pip install -r requirements.txt


Run the Application:
 uvicorn orchestrator.main:app --reload --port 8000     
For streamlit:
  cd front_end
  streamlit run app.py --server.port 8501   
```
The API will be available at http://localhost:8000.

The Streamlit will be available at http://localhost:8501.
 
## Setup
Set Up Environment Variables:Create a .env file in the project root:
OPENAI_API_KEY=your-openai-api-key

Replace your-openai-api-key with your actual OpenAI API key.

Initialize Qdrant:The application uses a local Qdrant instance (stored in ./qdrant_data). No additional setup is required, as the code initializes the session_memory collection automatically.
