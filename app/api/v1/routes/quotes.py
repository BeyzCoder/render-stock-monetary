from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from app.api.v1.services import item_quotes

router = APIRouter()

# Return csv file for now.
# async def service_quote(ticker: str, quote_type: str) -> StreamingResponse:
#     try:
#         content = await item_quotes.get_item(ticker, quote_type)
#     except ValueError as err:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    
#     return StreamingResponse(
#         content=iter([content]),
#         status_code=status.HTTP_200_OK,
#         media_type='text/csv',
#         headers={'Content-Disposition': f"attachment; filename={ticker}.csv"}
#     )

async def service_quote(ticker: str, quote_type: str) -> JSONResponse:
    try:
        content = await item_quotes.get_item(ticker, quote_type)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    
    return JSONResponse(
        content=content,
        status_code=status.HTTP_200_OK,
        media_type='application/json',
    )


@router.get("/historical-prices/{ticker}")
async def historical_prices(ticker: str) -> JSONResponse:
    return await service_quote(ticker, 'HISTORICAL_PRICES')

# Add feature for end-user to choose if they want csv file or string response.