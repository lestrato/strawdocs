from django import template

register = template.Library()

@register.filter
def latest_activity(question):
    def compare_dates(obj1, obj2):
        ''' compare dates between two objects and return the most recent'''
        return obj1 if obj1.created_on>obj2.created_on else obj2

    latest_activity_object = question

    # if the question has replies
    if question.post_reply.count() > 0:
        latest_activity_object = question.post_reply.reverse().first()

    # for each answer, check if the answer has replies
    for answer in question.question_answer.all():
        if answer.post_reply.count() > 0:
            latest_activity_object = compare_dates(latest_activity_object, answer.post_reply.all().reverse().first())
        else:
            latest_activity_object = compare_dates(latest_activity_object, answer)

    return latest_activity_object
