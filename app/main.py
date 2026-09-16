from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .llm import generate_response
from .models import Ticket
from .retrieval import retrieve_context
from .schemas import AskRequest, AskResponse


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI-Powered IT Support Assistant"
)


BASE_DIR = Path(__file__).resolve().parent

STATIC_DIR = BASE_DIR / "static"


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@app.get("/")
async def home():

    return FileResponse(
        STATIC_DIR / "index.html"
    )


@app.get("/api/health")
async def health():

    return {
        "status": "ok"
    }


@app.post(
    "/api/ask",
    response_model=AskResponse
)
async def ask(
    request: AskRequest,
    db: Session = Depends(get_db)
):

    question = request.question.strip()


    if len(question) < 5:

        raise HTTPException(
            status_code=400,
            detail=(
                "Please enter a technical support "
                "question with at least 5 characters."
            )
        )


    try:

        # Retrieve the best matching solution
        context = retrieve_context(
            question
        )


        # Generate the response
        answer = await generate_response(
            question,
            context
        )


        if not answer:

            answer = (
                "I couldn't generate a solution "
                "for this request. Please try again."
            )


        # Store ticket internally
        ticket = Ticket(
            question=question,
            retrieved_context=context,
            ai_response=answer
        )


        db.add(ticket)

        db.commit()

        db.refresh(ticket)


        # Return response to frontend
        return AskResponse(
            ticket_id=ticket.id,
            answer=answer,
            retrieved_context=context
        )


    except HTTPException:

        raise


    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process the support request. "
                "Please try again."
            )
        )