from google.cloud import aiplatform
from google.generativeai.types import GenerateContentResponse
from vertexai.vision_models import ImageGenerationModel
from typing import Optional
from io import BytesIO
import base64
import json # For parsing structured responses if needed

from ...config.settings import settings

class GeminiService:
    def __init__(self):
        # Initialize Vertex AI SDK. This needs project and location.
        # It's defensive here; ideally, it's globally managed.
        try:
            aiplatform.init(project=settings.PROJECT_ID, location=settings.LOCATION)
            self.gemini_model = aiplatform.GenerativeModel(settings.GEMINI_MODEL_NAME)
            self.imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
            print(f"GeminiService initialized with models: {settings.GEMINI_MODEL_NAME}, imagen-3.0-generate-002")
        except Exception as e:
            print(f"ERROR: Failed to initialize Vertex AI for GeminiService: {e}")
            self.gemini_model = None
            self.imagen_model = None
            import traceback
            traceback.print_exc()

    def generate_text(self, prompt: str, temperature: float = 0.4) -> Optional[str]:
        """
        Generates text using the configured Gemini model.
        Returns the generated text string, or None if generation fails or no content is produced.
        """
        if self.gemini_model is None:
            print("GeminiService (text model) is not initialized. Cannot generate text.")
            return None

        try:
            response: GenerateContentResponse = self.gemini_model.generate_content(
                prompt,
                generation_config=aiplatform.types.GenerationConfig(temperature=temperature),
            )
            if response.candidates:
                if response.candidates[0].content.parts:
                    return response.candidates[0].content.parts[0].text
            return None
        except Exception as e:
            print(f"Error calling Gemini Text API for prompt '{prompt[:100]}...': {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_image(self, prompt: str) -> Optional[str]:
        """
        Generates an image from a text prompt using the Imagen model.
        Returns base64 encoded image string, or None if generation fails.
        """
        if self.imagen_model is None:
            print("GeminiService (image model) is not initialized. Cannot generate image.")
            return None

        try:
            print(f"Calling Imagen for prompt: {prompt[:100]}...")
            images = self.imagen_model.generate_images(
                prompt=prompt,
                number_of_images=1
            )
            if images.images and len(images.images) > 0:
                buffered = BytesIO()
                images.images[0].save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                print("Imagen image generation successful.")
                return img_str
            else:
                print("Imagen image generation response missing image.")
                return None
        except Exception as e:
            print(f"Error generating image with Imagen for prompt '{prompt[:100]}...': {e}")
            import traceback
            traceback.print_exc()
            return None