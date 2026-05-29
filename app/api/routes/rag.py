from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel


router = APIRouter(prefix="/rag", tags=["rag"])


class AskRequest(BaseModel):
    query: str


@router.post("/ask")
async def ask(request: Request, ask_request: AskRequest):
    return await run_in_threadpool(request.app.state.answer_svc.answer_question, ask_request.query)
