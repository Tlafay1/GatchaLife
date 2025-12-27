from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import AsyncJob
from .registry import JobRegistry
import logging
import json

logger = logging.getLogger(__name__)


class N8NCallbackView(APIView):
    """
    Generic callback endpoint for N8N workflows.
    Expected Payload:
    {
        "job_id": "UUID",
        "status": "success" | "error",
        "data": { ... } (optional results),
        "error": "Error message" (optional)
    }
    """
    permission_classes = [] # Ideally protect with a secret key check

    def post(self, request, *args, **kwargs):
        job_id = request.data.get("job_id")
        n8n_status = request.data.get("status")
        data = request.data.get("data", {})

        # If multipart/form-data, 'data' might be a JSON string
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                # If it's not JSON, keep it as is or log warning
                pass

        error_msg = request.data.get("error", "")

        if not job_id:
            return Response({"error": "job_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Received N8N callback for Job {job_id} with status {n8n_status}")

        try:
            job = AsyncJob.objects.get(id=job_id)
        except AsyncJob.DoesNotExist:
             logger.error(f"AsyncJob {job_id} not found.")
             return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        if job.status in [AsyncJob.Status.COMPLETED, AsyncJob.Status.FAILED]:
             logger.warning(f"Job {job_id} is already in final state {job.status}. Ignoring callback.")
             return Response({"message": "Job already completed"}, status=status.HTTP_200_OK)

        handler = JobRegistry.get_handler(job.job_type)
        if not handler:
            job.status = AsyncJob.Status.FAILED
            job.error_message = f"No handler registered for job type: {job.job_type}"
            job.save()
            logger.error(job.error_message)
            return Response({"error": "Handler not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if n8n_status == "success":
            try:
                job.status = AsyncJob.Status.PROCESSING # Or keep processing until handler finishes?
                job.result = data
                handler.handle_success(job, data, files=request.FILES)
                
                # If handler didn't fail, mark as completed
                job.status = AsyncJob.Status.COMPLETED
                job.save()
            except Exception as e:
                logger.exception(f"Handler failed for job {job_id}")
                job.status = AsyncJob.Status.FAILED
                job.error_message = str(e)
                job.save()
                handler.handle_failure(job, str(e))
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else: # n8n_status == "error" or anything else
            job.status = AsyncJob.Status.FAILED
            job.error_message = error_msg or "Unknown error from N8N"
            job.save()
            handler.handle_failure(job, job.error_message)

        return Response({"message": "Callback processed"})
