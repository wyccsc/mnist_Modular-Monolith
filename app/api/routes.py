from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.file_service import save_uploaded_file, save_predictions
from app.services.prediction_service import predict_from_csv
from app.config import RESULT_FILE

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.post("/upload_predict")
async def upload_predict(request: Request, datafile: UploadFile = File(...)):

    try:

        if datafile.filename == "":
            return templates.TemplateResponse(
                "result.html",
                {"request": request, "success": False, "msg": "未選擇檔案"}
            )

        filepath = save_uploaded_file(
            await datafile.read(),
            datafile.filename
        )

        labels = predict_from_csv(filepath)

        save_predictions(labels)

        return RedirectResponse(
            url="/download_page",
            status_code=303
        )

    except Exception as e:

        return templates.TemplateResponse(
            "result.html",
            {"request": request, "success": False, "msg": str(e)}
        )


@router.get("/download")
async def download():

    return FileResponse(
        RESULT_FILE,
        filename="predictions.csv"
    )


@router.get("/download_page", response_class=HTMLResponse)
async def download_page(request: Request):

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "success": True,
            "msg": "預測完成！請下載結果。"
        }
    )