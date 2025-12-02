from django.db import models

class TickTickProject(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=50, blank=True, null=True)
    sortOrder = models.BigIntegerField(blank=True, null=True)
    groupid = models.CharField(max_length=255, blank=True, null=True)
    viewmode = models.CharField(max_length=50, blank=True, null=True)
    kind = models.CharField(max_length=50, blank=True, null=True)
    last_synced_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'projects'
        managed = False

    def __str__(self):
        return self.name

class TickTickColumn(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    projectId = models.CharField(max_length=255, blank=True, null=True) # Not using ForeignKey to avoid constraint issues if n8n syncs out of order
    name = models.CharField(max_length=255)
    sortOrder = models.BigIntegerField(blank=True, null=True)
    last_synced_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'columns'
        managed = False

    def __str__(self):
        return self.name

class TickTickTask(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    projectId = models.CharField(max_length=255, blank=True, null=True)
    columnId = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=1024)
    content = models.TextField(blank=True, null=True)
    task_desc = models.TextField(blank=True, null=True)
    status = models.IntegerField(default=0) # 0: Normal, 2: Completed (usually)
    priority = models.IntegerField(default=0)
    sortOrder = models.BigIntegerField(blank=True, null=True)
    kind = models.CharField(max_length=50, blank=True, null=True)
    # Using TextField to avoid JSON decoding issues with managed=False and n8n data
    reminders = models.TextField(blank=True, null=True) 
    tags = models.TextField(blank=True, null=True)
    parentId = models.CharField(max_length=255, blank=True, null=True)
    isAllDay = models.BooleanField(default=False)
    startDate = models.DateTimeField(blank=True, null=True)
    dueDate = models.DateTimeField(blank=True, null=True)
    timeZone = models.CharField(max_length=100, blank=True, null=True)
    repeatFlag = models.CharField(max_length=100, blank=True, null=True)
    etag = models.CharField(max_length=255, blank=True, null=True)
    last_synced_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tasks'
        managed = False

    def __str__(self):
        return self.title

class ProcessedTask(models.Model):
    """
    Tracks which tasks have already rewarded the player.
    """
    task_id = models.CharField(max_length=255, unique=True)
    task_title = models.CharField(max_length=1024, blank=True, null=True)
    processed_at = models.DateTimeField(auto_now_add=True)
    
    # Reward Details
    xp_gain = models.IntegerField(default=0)
    coin_gain = models.IntegerField(default=0)
    
    # "Why" Breakdown
    difficulty = models.CharField(max_length=50, default='easy') # easy, medium, hard, extreme
    is_crit = models.BooleanField(default=False)
    crit_multiplier = models.FloatField(default=1.0)
    base_reward = models.IntegerField(default=0)
    streak_multiplier = models.FloatField(default=1.0)
    daily_bonus = models.IntegerField(default=0)
    tags = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Processed {self.task_id} (+{self.coin_gain} coins)"
