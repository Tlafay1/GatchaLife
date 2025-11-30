class TickTickRouter:
    """
    A router to control all database operations on models in the
    ticktick application.
    """
    
    route_app_labels = {'ticktick'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read ticktick models go to ticktick db.
        """
        if model._meta.app_label in self.route_app_labels:
            # Check if it's one of the n8n models
            if model.__name__ in ['TickTickTask', 'TickTickProject', 'TickTickColumn']:
                return 'ticktick'
            # ProcessedTask stays in default
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write ticktick models go to ticktick db.
        """
        if model._meta.app_label in self.route_app_labels:
            if model.__name__ in ['TickTickTask', 'TickTickProject', 'TickTickColumn']:
                return 'ticktick'
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the ticktick app is involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the ticktick app only appears in the 'ticktick'
        database.
        """
        if app_label in self.route_app_labels:
            # ProcessedTask is in default
            if model_name == 'processedtask':
                return db == 'default'
            # Others are in ticktick
            return db == 'ticktick'
        return None
