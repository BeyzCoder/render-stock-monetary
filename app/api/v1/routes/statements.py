from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from api.v1.services import item_statements

router = APIRouter()


async def service_statement(ticker: str, statement_type: str) -> JSONResponse:
    try:
        content = await item_statements.get_item(ticker, statement_type)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    
    return JSONResponse(
        content=content,
        status_code=status.HTTP_200_OK,
        media_type='application/json',
    )


@router.get("/income/{ticker}")
async def income(ticker: str) -> JSONResponse:
    return await service_statement(ticker, 'INCOME_STATEMENT')


@router.get("/balance/{ticker}")
async def balance(ticker: str) -> JSONResponse:
    return await service_statement(ticker, 'BALANCE_SHEET')


@router.get("/cash/{ticker}")
async def cash(ticker: str) -> JSONResponse:
    return await service_statement(ticker, 'CASH_FLOW_STATEMENT')