# OrthopedicAI-Backend/app/services/llm_service.py

import asyncio
import google.generativeai as genai
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from app.core.config import settings

# --- BASE INTERFACE (ŞABLON) ---

class LLMProvider(ABC):
    """
    Abstract base class that all LLM providers must implement.
    Tüm LLM sağlayıcılarının uygulaması gereken soyut temel sınıf.
    """
    @abstractmethod
    async def analyze_image(self, image_path: str, prompt: str) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

# --- GEMINI IMPLEMENTATION (GEMINI UYARLAMASI) ---

class GeminiProvider(LLMProvider):
    def __init__(self):
        # Configure Gemini with the API key
        # Gemini'yi API anahtarı ile yapılandır
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-flash') # Or gemini-pro-vision
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY is missing.")

    def get_name(self) -> str:
        return "Gemini 2.5 Flash"

    async def analyze_image(self, image_path: str, prompt: str) -> str:
        if not self.model:
            return "Error: Gemini API key not configured."
        
        try:
            # Load the image using helper or library
            # Resmi yardımcı veya kütüphane kullanarak yükle
            # Note: generativeai library handles file I/O for images usually via specific format
            # Not: generativeai kütüphanesi resimler için dosya giriş/çıkışını genellikle belirli formatla halleder
            
            # For simplicity, we read bytes here to pass to Gemini
            # Basitlik olması adına, Gemini'ye iletmek için burada baytları okuyoruz
            import PIL.Image
            img = PIL.Image.open(image_path)

            # Generate content (Run in a thread pool because it's synchronous library code)
            # İçerik üret (Senkron kütüphane kodu olduğu için iş parçacığı havuzunda çalıştır)
            response = await asyncio.to_thread(
                self.model.generate_content,
                [prompt, img]
            )
            return response.text
        except Exception as e:
            print(f"Error in Gemini analysis: {str(e)}")
            return f"Error analyzing with Gemini: {str(e)}"

# --- OPENAI IMPLEMENTATION (PLACEHOLDER FOR FUTURE) ---
# --- OPENAI UYARLAMASI (GELECEK İÇİN YER TUTUCU) ---

# class OpenAIProvider(LLMProvider):
#     def __init__(self):
#         # self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
#         pass
#
#     def get_name(self) -> str:
#         return "GPT-4o"
#
#     async def analyze_image(self, image_path: str, prompt: str) -> str:
#         # Implement OpenAI logic here
#         # OpenAI mantığını buraya uygula
#         return "OpenAI analysis placeholder"


# --- ORCHESTRATOR (ORKESTRA ŞEFİ) ---

class MultiModelAnalyzer:
    def __init__(self):
        # Initialize active providers
        # Aktif sağlayıcıları başlat
        self.providers: List[LLMProvider] = []
        
        # Add Gemini
        # Gemini'yi ekle
        self.providers.append(GeminiProvider())
        
        # Add OpenAI or others in the future
        # Gelecekte OpenAI veya diğerlerini ekle
        # self.providers.append(OpenAIProvider())

    async def analyze_with_all(self, image_path: str, prompt: str) -> Dict[str, str]:
        """
        Sends the image to all configured providers in parallel.
        Resmi yapılandırılmış tüm sağlayıcılara paralel olarak gönderir.
        """
        results = {}
        
        # Define a wrapper to catch exceptions for individual providers
        # Bireysel sağlayıcılar için istisnaları yakalamak adına bir sarmalayıcı tanımla
        async def safe_analyze(provider: LLMProvider):
            try:
                response = await provider.analyze_image(image_path, prompt)
                return provider.get_name(), response
            except Exception as e:
                print(f"Provider {provider.get_name()} failed: {e}")
                return provider.get_name(), f"Failed: {str(e)}"

        # Run all tasks concurrently
        # Tüm görevleri eşzamanlı çalıştır
        tasks = [safe_analyze(p) for p in self.providers]
        provider_results = await asyncio.gather(*tasks)

        for name, response in provider_results:
            results[name] = response

        return results

    async def synthesize_results(self, individual_results: Dict[str, str]) -> str:
        """
        Creates a final summary combining all results.
        Tüm sonuçları birleştiren nihai bir özet oluşturur.
        """
        # We use the primary model (Gemini for now) to synthesize
        # Sentezlemek için birincil modeli (şimdilik Gemini) kullanıyoruz
        if not self.providers:
            return "No providers available for synthesis."
        
        primary_provider = self.providers[0] # Use the first available one
        
        synthesis_prompt = "Here are analyses from different AI models about a medical image:\n\n"
        for model, result in individual_results.items():
            synthesis_prompt += f"--- Model: {model} ---\n{result}\n\n"
            
        synthesis_prompt += (
            "Based on these analyses, provide a comprehensive, merged summary. "
            "Highlight any consensus and discrepancies. "
            "The output should be a single coherent report."
            "\n\nBu analizlere dayanarak, kapsamlı ve birleştirilmiş bir özet sun. "
            "Fikir birliklerini ve tutarsızlıkları vurgula. "
            "Çıktı tek ve tutarlı bir rapor olmalıdır."
        )

        # For synthesis, we don't need the image again, just the text prompt
        # Sentez için resme tekrar ihtiyacımız yok, sadece metin istemi yeterli
        # However, our interface requires image_path, so we might need a text-only method
        # Ancak arayüzümüz image_path gerektiriyor, bu yüzden sadece metin içeren bir metoda ihtiyacımız olabilir.
        # For now, we utilize the model directly or adapt the provider.
        # Şimdilik modeli doğrudan kullanıyoruz veya sağlayıcıyı uyarlıyoruz.
        
        # Quick hack: Use Gemini directly for text-only synthesis if strictly needed
        # Hızlı çözüm: Kesinlikle gerekliyse sadece metin sentezi için doğrudan Gemini kullan
        try:
             # Assuming GeminiProvider exposes the model
             if isinstance(primary_provider, GeminiProvider) and primary_provider.model:
                 response = await asyncio.to_thread(
                     primary_provider.model.generate_content,
                     synthesis_prompt
                 )
                 return response.text
        except Exception as e:
            return f"Error during synthesis: {str(e)}"
            
        return "Synthesis not implemented for this provider."

# Create a singleton instance
# Tekil bir örnek oluştur
analyzer_service = MultiModelAnalyzer()