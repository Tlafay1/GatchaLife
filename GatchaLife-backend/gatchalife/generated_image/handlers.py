import logging
from io import BytesIO
import base64
from django.core.files.base import ContentFile
from gatchalife.workflow_engine.registry import WorkflowHandler, JobRegistry
from gatchalife.generated_image.models import GeneratedImage

logger = logging.getLogger(__name__)

@JobRegistry.register("generate_image")
class ImageGenerationHandler(WorkflowHandler):
    def handle_success(self, job, data, files=None):
        try:
            generated_image = job.content_object
            if not isinstance(generated_image, GeneratedImage):
                 raise ValueError(f"Job {job.id} content_object is not a GeneratedImage")

            # Priority 1: Check for uploaded file in 'files'
            if files and len(files) > 0:
                # Iterate and find the first file, or specific key if known.
                # N8N "Send Binary Data" usually sends it with key 'data' or 'file'
                uploaded_file = next(iter(files.values()))

                logger.info(
                    f"Received file upload for Job {job.id}: {uploaded_file.name}"
                )

                # Use string format for random suffix if needed, but here simple ID is enough
                # or trust uploaded_file.name if meaningful.
                # However, ensure extension.
                import os

                ext = os.path.splitext(uploaded_file.name)[1] or ".png"
                filename = f"generated_image_{generated_image.id}{ext}"

                generated_image.image.save(filename, uploaded_file, save=True)

            else:
                # Priority 2: Base64 in JSON data
                image_data_b64 = data.get("image_base64") or data.get("data")

                if not image_data_b64:
                    raise ValueError(
                        "No image data found (files or base64) in callback payload"
                    )

                try:
                    # Decode base64
                    file_content = base64.b64decode(image_data_b64)
                    filename = f"generated_image_{generated_image.id}.png"
                    generated_image.image.save(
                        filename, ContentFile(file_content), save=True
                    )
                except Exception:
                    # Maybe it is already bytes or invalid
                    raise ValueError("Failed to decode base64 image data")

            logger.info(
                f"Successfully saved image for GeneratedImage {generated_image.id}"
            )
            
            logger.info(f"Successfully saved image for GeneratedImage {generated_image.id}")

        except Exception as e:
            logger.error(f"Error in ImageGenerationHandler: {e}")
            raise e

    def handle_failure(self, job, error_message):
        generated_image = job.content_object
        logger.error(f"Image generation failed for {generated_image.id if generated_image else 'Unknown'}: {error_message}")
        # Optionally delete the empty object or mark as failed in DB if we added a status field
