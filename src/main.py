from fastapi import FastAPI
# from chunks.chunk1_data_ingestion import api as chunk1_api
from chunks.chunk2_sentiment_engine import api as chunk2_api

app = FastAPI(
    title="Fear & Greed Adaptive Trading Framework",
    description="A data-driven trading framework that adapts to market sentiment.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fear & Greed Adaptive Trading Framework API"}

# Include routers from different chunks
# app.include_router(chunk1_api.router, prefix="/chunk1", tags=["Data Ingestion"])
app.include_router(chunk2_api.router, prefix="/chunk2", tags=["Sentiment Engine"])

# In a real application, you would also have routers for other chunks:
# app.include_router(chunk3_api.router, prefix="/chunk3", tags=["Strategies"])
# app.include_router(chunk4_api.router, prefix="/chunk4", tags=["Risk Management"])
# app.include_router(chunk5_api.router, prefix="/chunk5", tags=["Execution"])
# app.include_router(chunk6_api.router, prefix="/chunk6", tags=["Monitoring"])
