from threading import Thread
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntryManager, LogEntry


class LoggingThread(Thread):
    # ADDITION = 1
    # CHANGE = 2
    # DELETION = 3
    def __init__(self, user_id=1, modelname='logentry', object_id=1, object_repr='Object', action_flag=2,
                 change_message='change'):
        self.user_id = user_id
        self.modelname = modelname
        self.object_id = object_id
        self.object_repr = object_repr
        self.action_flag = action_flag
        self.change_message = change_message
        Thread.__init__(self)

    def run(self):
        content_type = ContentType.objects.get(model=self.modelname)
        print(content_type)
        try:
            content_type_id = content_type.id
            LogEntry.objects.log_action(
                user_id=self.user_id,
                content_type_id=content_type_id,
                object_id=self.object_id,
                object_repr=self.object_repr,
                action_flag=self.action_flag,
                change_message=self.change_message)
        except:
            print('failed')
            pass
