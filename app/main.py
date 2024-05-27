from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum

from app.router.urls import get_routers

app = FastAPI(title="Instagram Influencers Data")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return JSONResponse(content="Welcome to Instagram Influencers Data")


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({

            "status": 400,
            "message": "Bad Request",
            "error": {
                "code": "SCHEMA_VALIDATION_FAILED",
                "description": "field data missing",
                "detail": exc.errors()
            }
        }
        ),
    )


for api in get_routers():
    app.include_router(api().router)

handler = Mangum(app)
