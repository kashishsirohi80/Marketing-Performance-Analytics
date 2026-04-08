# Marketing Performance Analytics

End to end marketing analytical project using sql , python and power BI.
## Project Overview
This project analyzes marketing campaign performance using real dataset.
It includes data cleaning , SQL modelling , and Power BI dashboard.

An intelligent AI-powered SQL Assistant built with Streamlit and Google Gemini that converts natural language questions into SQL queries for analyzing Campaign and Sales data.

## 📁 Project Structure

```
assignment/
├── ai_tool/                          # Main Streamlit application
│   ├── app.py                        # Main Streamlit app entry point
│   ├── llm.py                        # LLM/Gemini integration
│   ├── db.py                         # Database connection and query execution
│   ├── config.py                     # Configuration and environment variables
│   ├── prompt.py                     # LLM prompt templates
│   ├── memory.py                     # Conversation memory management
│   ├── utils.py                      # Utility functions (SQL cleaning, parsing)
│   ├── requirements.txt              # Python dependencies
│   └── .env (not included)           # Environment variables (create this)
│
├── data/                             # Raw data files
│   ├── Campaign_Raw.csv              # Raw campaign data
│   └── Raw_Shopify_Sales.csv         # Raw Shopify sales data
│
├── python/                           # Data processing scripts
│   └── analysis.py                   # Data cleaning and preprocessing
│
├── sql/                              # Database schema
│   └── schema.sql                    # Table definitions and indexes
│
├── powerbi/                          # Power BI visualizations (optional)
│
├── *.csv files                       # Processed data
│   ├── date_dim.csv                  # Date dimension table
│   ├── fact_sales.csv                # Sales fact table
│   └── fact_campaign.csv             # Campaign fact table
│
├── *.db files                        # SQLite databases
│   ├── cleaned_shopify.db
│   ├── cleaned_campaigns.db
│   └── final.db
│
└── README.md                         # This file
```

## 🔧 Requirements

### System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- MySQL or SQLite database

### Python Dependencies
All dependencies are listed in `ai_tool/requirements.txt`:

```
streamlit            # UI framework for the web app
google-generativeai  # Google Gemini AI API
sqlalchemy          # SQL toolkit and ORM
pandas              # Data manipulation and analysis
python-dotenv       # Load environment variables from .env
pymysql             # MySQL database connector
```

## 🚀 Installation & Setup

### 1. **Clone/Extract the Project**
```bash
cd assignment
```

### 2. **Create a Virtual Environment (Recommended)**
```bash
# For Windows PowerShell
python -m venv .venv
.\.venv\Scripts\activate

# For MacOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. **Install Dependencies**
```bash
pip install -r ai_tool/requirements.txt
```

### 4. **Set Up Environment Variables**
Create a `.env` file in the `ai_tool/` directory with:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
DB_URI=mysql+pymysql://username:password@localhost:3306/your_database
# OR for SQLite:
# DB_URI=sqlite:///path/to/your/database.db
```

**How to get GEMINI_API_KEY:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API Key"
3. Create a new API key for Python
4. Copy and paste it into your `.env` file

### 5. **Load Data into Database**
```bash
# Run the SQL schema to create tables
# Execute sql/schema.sql in your database

# Then run the data cleaning script
cd python
python analysis.py
cd ..
```

### 6. **Prepare CSV Files** (if needed)
The processed data should be available as:
- `date_dim.csv`
- `fact_sales.csv`
- `fact_campaign.csv`

These are generated after running the data cleaning script.

## ▶️ How to Run

### Start the Streamlit Application

**From the project root directory:**

```bash
# Make sure your virtual environment is activated first
.\.venv\Scripts\activate    # Windows PowerShell
# OR
source .venv/bin/activate   # MacOS/Linux

# Navigate to ai_tool directory
cd ai_tool

# Run the Streamlit app
streamlit run app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Using the Application

1. **Open the Web Interface**: Navigate to `http://localhost:8501` in your browser
2. **Ask a Question**: Type any question about your Campaign or Sales data in the input field
   - Example: "What is the total revenue by country?"
   - Example: "Show me the top 10 products by sales"
   - Example: "What was the ROI for each campaign?"
3. **Run Query**: Click the "Run Query" button
4. **View Results**:
   - Generated SQL: See the SQL query created by the AI
   - Query Result: View the data in an interactive table

## 📊 Database Schema

### Fact Tables

**fact_sales**
- `order_id`, `date`, `product_id`, `product_type`
- `shipping_country`, `total_sales`, `net_sales`, `gross_sales`
- `orders`, `items_sold`, `items_returned`, `return_rate`, `aov`

**fact_campaign**
- `campaign_name`, `date`, `country`
- `impressions`, `clicks`, `spend`, `purchases`, `revenue`
- `CTR`, `CPC`, `CPM`, `ROI`

### Dimension Table

**date_dim**
- `date` (PRIMARY KEY), `year`, `month`, `day`, `quarter`

## 🛠️ File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit UI and orchestration logic |
| `llm.py` | Handles Google Gemini API calls for SQL generation |
| `db.py` | Database connection and query execution |
| `config.py` | Environment variable management |
| `prompt.py` | LLM prompt engineering and templates |
| `memory.py` | Conversation history and context management |
| `utils.py` | Utility functions (SQL cleaning, LLM output parsing) |
| `analysis.py` | Data cleaning and preprocessing pipeline |

## 🎯 Key Features

✅ **Natural Language to SQL**: Convert questions to SQL queries using AI  
✅ **Conversation Memory**: Maintain context across multiple queries  
✅ **Error Handling**: Graceful handling of SQL errors with user feedback  
✅ **Interactive UI**: Beautiful Streamlit interface with code display  
✅ **Data Caching**: Query results are cached for performance  

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Solution**: Re-install dependencies
```bash
pip install -r ai_tool/requirements.txt
```

### Issue: `GEMINI_API_KEY not found`
**Solution**: 
- Create `.env` file in `ai_tool/` directory
- Add your API key: `GEMINI_API_KEY=your_key_here`
- Restart the Streamlit app

### Issue: `Database connection error`
**Solution**:
- Verify `DB_URI` in `.env` is correct
- Check if database server is running
- Ensure tables are created using `schema.sql`

### Issue: Streamlit port already in use
**Solution**: Run on a different port
```bash
streamlit run app.py --server.port 8502
```

## 📝 Example Questions to Ask

- "What is the total sales by country?"
- "Show me the top 5 campaigns by ROI"
- "How many items were returned this month?"
- "What is the average order value by product type?"
- "Compare campaign performance across countries"

## 🔐 Security Notes

⚠️ **Never commit `.env` file** to version control  
⚠️ **Keep API keys private** - regenerate if accidentally exposed  
⚠️ **Database credentials** should be environment-specific  

## 📚 Technologies Used

- **Frontend**: Streamlit
- **AI Model**: Google Gemini
- **Database**: MySQL/SQLite
- **ORM**: SQLAlchemy
- **Data Processing**: Pandas
- **Language**: Python 3.8+

## 📞 Support

For database schema questions, refer to `sql/schema.sql`  
For data processing details, check `python/analysis.py`  
For LLM configuration, see `ai_tool/llm.py` and `ai_tool/prompt.py`

---

**Last Updated**: April 2026  
**Assignment Status**: Complete ✅
