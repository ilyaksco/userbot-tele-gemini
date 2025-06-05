import google.generativeai as genai
from config import settings
from services import database_service 

genai.configure(api_key=settings.GEMINI_API_KEY)

generation_config = {
    "temperature": settings.GEMINI_TEMPERATURE,
    "top_p": settings.GEMINI_TOP_P,
    "top_k": settings.GEMINI_TOP_K,
    "max_output_tokens": settings.GEMINI_MAX_OUTPUT_TOKENS,
}

gemini_model = genai.GenerativeModel(
    model_name=settings.GEMINI_MODEL_NAME,
    generation_config=generation_config,
    safety_settings=settings.GEMINI_SAFETY_SETTINGS,
    system_instruction=settings.GEMINI_SYSTEM_PROMPT
)

def _format_history_for_gemini(history_records: list) -> list:
    """Mengubah format histori dari DB ke format yang diterima Gemini."""
    gemini_history = []
    for record in history_records:
        if record['role'] in ["user", "model"]:
            gemini_history.append({
                "role": record['role'],
                "parts": [{"text": record['content']}]
            })
    return gemini_history

async def get_gemini_response(chat_id: int, user_prompt: str) -> str:
    try:
        
        print(f"GEMINI_SERVICE: Mengambil histori untuk chat_id: {chat_id} SEBELUM prompt baru: '{user_prompt}'")
        raw_history = await database_service.get_conversation_history(chat_id)
        print(f"GEMINI_SERVICE: Histori mentah yang diambil untuk chat_id {chat_id}: {raw_history}") # Log histori yang diambil
        formatted_history = _format_history_for_gemini(raw_history)

        
        convo = gemini_model.start_chat(history=formatted_history)

        response = await convo.send_message_async(user_prompt)
        ai_response_text = response.text

        
        if ai_response_text:
             await database_service.add_message_to_history(chat_id, "model", ai_response_text)

        return ai_response_text

    except Exception as e:
        print(f"Error saat menghubungi Gemini atau memproses histori (chat_id: {chat_id}): {e}")
        import traceback
        traceback.print_exc()
        return "Maaf, terjadi sedikit gangguan dengan AI saat ini."
