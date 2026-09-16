from pathlib import Path
import traceback

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .llm import generate_response
from .models import Ticket
from .retrieval import retrieve_context
from .schemas import AskRequest, AskResponse


# Create the database tables
Base.metadata.create_all(bind=engine)


# Create the FastAPI application
app = FastAPI(
    title="AI-Powered IT Support Assistant"
)


# Find the app folder
BASE_DIR = Path(__file__).resolve().parent

# Find the static folder
STATIC_DIR = BASE_DIR / "static"


# Make CSS and JavaScript available to the browser
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


# Create a database session for each request
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Home page
@app.get("/")
async def home():

    return FileResponse(
        STATIC_DIR / "index.html"
    )


# Health check endpoint
@app.get("/api/health")
async def health():

    return {
        "status": "ok"
    }


# Main support endpoint
@app.post(
    "/api/ask",
    response_model=AskResponse
)
async def ask(
    request: AskRequest,
    db: Session = Depends(get_db)
):

    # Get the user's question
    question = request.question.strip()


    # Basic validation
    if len(question) < 5:

        raise HTTPException(
            status_code=400,
            detail=(
                "Question must contain "
                "at least 5 characters."
            )
        )


    try:

        # Step 1:
        # Search the knowledge base
        context = retrieve_context(
            question
        )


        # Step 2:
        # Send question and retrieved context
        # to Gemini
        answer = await generate_response(
            question,
            context
        )


        # Step 3:
        # Create a ticket
        ticket = Ticket(
            question=question,
            retrieved_context=context,
            ai_response=answer
        )


        # Step 4:
        # Save the ticket
        db.add(ticket)

        db.commit()

        db.refresh(ticket)


        # Step 5:
        # Send the result back to the frontend
        return AskResponse(
            ticket_id=ticket.id,
            answer=answer,
            retrieved_context=context
        )


    except RuntimeError as error:

        # Undo any incomplete database operation
        db.rollback()

        # Show the actual error in the terminal
        print("========== RUNTIME ERROR ==========")
        print(type(error).__name__)
        print(str(error))
        print("===================================")

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


    except Exception as error:

        # Undo any incomplete database operation
        db.rollback()

        # Print the complete error in the terminal
        print("========== ERROR ==========")
        print(type(error).__name__)
        print(str(error))
        traceback.print_exc()
        print("============================")

        # Return the actual error to the frontend
        # temporarily so we can debug it
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )