# OrthopedicAI-Backend/app/routers/analysis.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.services import image_service
from app.services.llm_service import analyzer_service

router = APIRouter()

@router.post("/analyze")
async def analyze_medical_image(
    file: UploadFile = File(...),
    prompt: str = Form("Analyze this medical image and identify potential anomalies.")
):
    """
    Receives an image and a prompt, sends it to multiple LLMs, and returns a synthesized report.
    Bir resim ve istem alır, bunu birden fazla LLM'e gönderir ve sentezlenmiş bir rapor döndürür.
    """
    
    # 1. Validate the image
    # 1. Resmi doğrula
    image_service.validate_image(file)
    
    # 2. Save the image temporarily
    # 2. Resmi geçici olarak kaydet
    file_path = image_service.save_upload_file(file)
    
    try:
        # 3. Send to LLM Orchestrator (Gemini, etc.)
        # 3. LLM Orkestratörüne gönder (Gemini vb.)
        # Returns a dictionary: {"Gemini 1.5 Flash": "Analysis text...", "GPT-4": "..."}
        # Bir sözlük döndürür: {"Gemini 1.5 Flash": "Analiz metni...", "GPT-4": "..."}
        individual_results = await analyzer_service.analyze_with_all(file_path, prompt)
        
        # 4. Synthesize the results (Create a summary)
        # 4. Sonuçları sentezle (Bir özet oluştur)
        final_report = await analyzer_service.synthesize_results(individual_results)
        
        return {
            "status": "success",
            "individual_analyses": individual_results,
            "final_report": final_report
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
        
    finally:
        # 5. Cleanup: Delete the temporary file
        # 5. Temizlik: Geçici dosyayı sil
        image_service.delete_file(file_path)