from fastapi import FastAPI
from routes.users import users_router
from routes.funds import fund_router
from database import engine
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import models

app = FastAPI()
app.include_router(users_router)
app.include_router(fund_router)
models.Base.metadata.create_all(engine)

# Allow your frontend origin (like http://localhost:3000)
origins = [
    "http://localhost:3000",  # React dev server
    # add other domains if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Accept requests from these origins
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],              # Allow all headers (especially Content-Type, Authorization)
)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
