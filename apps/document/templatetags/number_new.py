from django import template
from django.db.models import Q
register = template.Library()

@register.filter
def number_new(this_object, user):
    ''' Given the object and the user, find the number of answer posts
    that the user has not seen based on the user's last visit datetime
    '''
    if type(this_object).__name__ == 'Document':
        total_unread = 0
        for question in this_object.question_set.all():
            answers = question.answer_set
            if not user.userquestionlastvisit_set.first():
                total_unread += answers.count()
            else:
                visit_datetime = user.userquestionlastvisit_set.first().created_on
                unseen_answers = answers.filter(~Q(created_by=user), created_on__gt=visit_datetime)
                total_unread += unseen_answers.count()

        return str(total_unread)

    elif type(this_object).__name__ == 'Question':
        answers = this_object.answer_set
        if not user.userquestionlastvisit_set.first():
            return str(answers.count())
        else:
            visit_datetime = user.userquestionlastvisit_set.first().created_on
            unseen_answers = answers.filter(~Q(created_by=user), created_on__gt=visit_datetime)
            return str(unseen_answers.count())
