import logging
from io import BytesIO
import base64
from django.core.files.base import ContentFile
from gatchalife.workflow_engine.registry import WorkflowHandler, JobRegistry
from gatchalife.generated_image.models import GeneratedImage

logger = logging.getLogger(__name__)

@JobRegistry.register("generate_image")
class ImageGenerationHandler(WorkflowHandler):
    def handle_success(self, job, data):
        try:
            generated_image = job.content_object
            if not isinstance(generated_image, GeneratedImage):
                 raise ValueError(f"Job {job.id} content_object is not a GeneratedImage")

            # Data expectation: {"image_base64": "..."} or {"url": "..."}
            # Adjust based on actual N8N output. 
            # Assuming N8N returns the binary or base64.
            # If N8N returns raw binary in webhook, it might be in request.FILES? 
            # But the callback view processes JSON.
            # So N8N should send base64 in JSON.
            
            image_data_b64 = data.get("image_base64") or data.get("data")
            
            if not image_data_b64:
                raise ValueError("No image data found in callback payload")

            try:
                # Decode base64
                file_content = base64.b64decode(image_data_b64)
            except Exception:
                # Maybe it is already bytes or invalid
                raise ValueError("Failed to decode base64 image data")

            # Save to ImageField
            filename = f"generated_image_{generated_image.id}.png"
            generated_image.image.save(filename, ContentFile(file_content), save=True)
            
            logger.info(f"Successfully saved image for GeneratedImage {generated_image.id}")

        except Exception as e:
            logger.error(f"Error in ImageGenerationHandler: {e}")
            raise e

    def handle_failure(self, job, error_message):
        generated_image = job.content_object
        logger.error(f"Image generation failed for {generated_image.id if generated_image else 'Unknown'}: {error_message}")
        # Optionally delete the empty object or mark as failed in DB if we added a status field
