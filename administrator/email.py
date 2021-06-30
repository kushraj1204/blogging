from threading import Thread
from django.core.mail import send_mail


class EmailThread(Thread):

    def __init__(self, subject='Welcome to KushBlogs', message='Welcome to KushBlogs', email_from='info@kushblogs.com',
                 email_to=''):
        self.message = message
        self.email_from = email_from
        self.email_to = email_to
        self.subject = subject
        Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.message,
            self.email_from,
            self.email_to,
            fail_silently=False,
        )

# call as  EmailThread(subject="Subject",message="message",email_from="info@kushblogs.com",email_to=["spam_victim@gmail.com","kushraj1204@gmail.com"]).start()
