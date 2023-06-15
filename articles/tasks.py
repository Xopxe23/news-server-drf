import time

from celery import shared_task


@shared_task
def sent_comment(comment_id):
    time.sleep(5)
    from articles.models import Comment
    comment = Comment.objects.filter(id=comment_id).first()
    text = replace_bad_words(comment.text)
    comment.text = text
    comment.save(save_model=False)


def replace_bad_words(text: str) -> str:
    bad_words = ['хуй', 'бляд', 'пизда']
    for word in bad_words:
        if word in text:
            text = text.replace(word, '***')
    return text
