from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from app.apiauthhelper import token_required
from app.ig.forms import PostForm
from app.models import Post, db, User

ig = Blueprint('ig', __name__, template_folder = 'igtemplates')



@ig.route('/posts/create', methods=['GET','POST'])
@login_required
def createPost():
    form = PostForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post = Post(title, img_url, caption, current_user.id)

            # db.session.add(post)
            # db.session.commit()
            post.save()
            flash('Sucessfully created post!', 'success')
        else:
            flash('Invalid form. Please fill out the form correctly', 'danger')
    return render_template('createpost.html', form=form)

@ig.route('/posts')
# @login_required # another valid option but the feed is still going to be a button shown
def getAllPosts():
    if current_user.is_authenticated:
        posts = current_user.get_followed_posts()
    else:
        posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('feed.html', posts=posts)

@ig.route('/posts/<int:post_id>')
def getSinglePost(post_id):
    post = Post.query.get(post_id)
    # post = Post.query.filter_by(id=post_id).first()
    return render_template('singlepost.html', post=post)

@ig.route('/posts/update/<int:post_id>', methods=["GET","POST"])
@login_required
def updatePost(post_id):
    form = PostForm()
    # post = Post.query.get(post_id)
    post = Post.query.filter_by(id=post_id).first()
    if current_user.id != post.user_id:
        flash('You are not allowed to update another user\'s post.', 'danger')
        return redirect(url_for('ig.getSinglePost', post_id=post_id))
    if request.method=="POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post.updatePostInfo(title, img_url, caption)
            # post.title=title
            # post.img_url=img_url
            # post.caption=caption

            # db.session.commit()
            post.saveUpdates()
            flash('Successfully updated!', 'success')
            return redirect(url_for('ig.getSinglePost', post_id=post_id))
        else:
            flash('Invalid form. Please fill out the form correctly', 'danger')
    return render_template('updatepost.html', form=form, post=post)

@ig.route('/posts/delete/<int:post_id>')
@login_required
def deletePost(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        flash('You are not allowed to delete another user\'s post.', 'danger')
        return redirect(url_for('ig.getSinglePost', post_id=post_id))
    # db.session.delete(post)
    # db.session.commit()
    post.delete()
    flash('Successfully deleted!', 'success')
    return redirect(url_for('ig.getAllPosts'))

@ig.route('/follow/<int:user_id>')
@login_required
def followUser(user_id):
    user = User.query.get(user_id)

    # The User class is going to have a new method:
    # current_user.followed.append(user)
    # db.session.commit()
    current_user.follow(user)
    return redirect(url_for('index'))


@ig.route('/unfollow/<int:user_id>')
@login_required
def unfollowUser(user_id):
    user = User.query.get(user_id)
    current_user.unfollow(user)
    return redirect(url_for('index'))


####################### API ROUTES #######################
@ig.route('/api/posts', methods=['POST', 'GET'])
def getAllPostsAPI():
    # args = request.args
    # pin = args.get('pin')
    # print(pin, type(pin))
    # if pin == '1234':

        posts = Post.query.all() #list of posts
        posts = Post.query.order_by(Post.date_created.desc()).all() #orders posts in react app

        my_posts = [p.to_dict() for p in posts]
        print(my_posts)
        return {'status': 'ok', 'total_results': len(posts), 'posts': my_posts}
    # else:
    #     return {
    #         'status': 'not ok',
    #         'code': 'Invalid pin',
    #         'message': 'The pin number was incorrect, please try again'
    #     }

@ig.route('/api/posts/<int:post_id>', methods=['POST'])
def getSinglePostsAPI(post_id):
    post = Post.query.get(post_id) #post object
    if post:
        return {
            'status': 'ok', 
            'total_results': 1, 
            'post': post.to_dict(),
            }
    else:
        return{
            'status': 'error',
            'message': f'A post with the id : {post_id} does not exist.'
        }

# decorated protected route
# passing this func to apiauthhelper
@ig.route('/api/posts/create', methods=["POST"])
@token_required #running apiauthhelper first that's why it's on top
# user is current_user. If u passed all the checks, now accepting the user who that token belongs to
# token is required & it belongs to that user
def createPostsAPI(user):
    data = request.json # this is coming from POST request Body

    title = data['title']
    caption = data['caption']
    img_url = data['imgUrl']

    post = Post(title, img_url, caption, user.id)
    post.save()

    return{
        'status': 'ok',
        'message': "Post was successfully created."
    }