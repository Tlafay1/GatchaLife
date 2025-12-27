import logging
from gatchalife.workflow_engine.registry import WorkflowHandler, JobRegistry
from gatchalife.character.models import Character
from gatchalife.character.services import update_character_from_ai, update_variants_from_ai

logger = logging.getLogger(__name__)

@JobRegistry.register("character_profiling")
class CharacterProfilingHandler(WorkflowHandler):
    def handle_success(self, job, data, files=None):
        try:
            character = job.content_object
            if not isinstance(character, Character):
                raise ValueError(f"Job {job.id} content_object is not a Character")
            
            # Use existing service logic
            update_character_from_ai(character, data)
            
            # Update legacy status field if we decide to keep it in sync, 
            # or rely solely on AsyncJob status.
            # character.profiling_status = "COMPLETED" 
            # character.save()
            
            logger.info(f"Successfully profiled character {character.name}")
            
        except Exception as e:
            logger.error(f"Error in CharacterProfilingHandler: {e}")
            raise e

    def handle_failure(self, job, error_message):
        character = job.content_object
        logger.error(f"Character profiling failed for {character.name if character else 'Unknown'}: {error_message}")
        # Update character status if needed
        # character.profiling_status = "FAILED"
        # character.save()


@JobRegistry.register("create_variants")
class VariantGenerationHandler(WorkflowHandler):
    def handle_success(self, job, data, files=None):
        try:
            character = job.content_object
            if not isinstance(character, Character):
                raise ValueError(f"Job {job.id} content_object is not a Character")

            created_variants = update_variants_from_ai(character, data)
            logger.info(f"Successfully created {len(created_variants)} variants for {character.name}")

        except Exception as e:
            logger.error(f"Error in VariantGenerationHandler: {e}")
            raise e

    def handle_failure(self, job, error_message):
        character = job.content_object
        logger.error(f"Variant generation failed for {character.name if character else 'Unknown'}: {error_message}")
