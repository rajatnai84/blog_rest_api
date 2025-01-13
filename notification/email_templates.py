def comment_delete_by_author_notification(user, blog, comment):
    subject = f"Your comment deleted by {blog.author.username} on blog {blog.title}"
    message = (
        f"Hello {comment.author.username},\n\n"
        f"Your comment on the blog {blog.title} is removed from blog by author:{blog.author.username}:\n"
        f"Comment: '{comment.content}'\n"
    )
    return subject, message

def comment_add_to_author_notification(user, blog, comment):
    subject = f"Comment on blog {blog.title} by {comment.author.username}"
    message = (
        f"Hello {blog.author.username},\n\n"
        f"Comment: '{comment.content}'\n"
    )
    return subject, message