# Twitter-Like Social Network

Design and implement a Twitter-like social network website for making posts and following users. This README will guide you through setting up and understanding the project.

## Getting Started

1. Download the distribution code from [this link](https://cdn.cs50.net/web/2020/spring/projects/4/network.zip) and unzip it.
2. In your terminal, navigate to the project4 directory.
3. Run `python manage.py makemigrations network` to make migrations for the network app.
4. Run `python manage.py migrate` to apply migrations to your database.

## Understanding

In the distribution code, you will find a Django project called project4, which contains a single app named network. The structure is similar to Project 2's auctions app.

### URLs and Views

- The URL configuration is defined in `network/urls.py`, with pre-defined routes for index, login, logout, and register.
- The associated views can be found in `network/views.py`.
  - `index` renders the main page.
  - `login_view` handles user login.
  - `logout_view` logs users out.
  - `register` allows user registration.

### Layout

- The HTML layout can be customized in `network/templates/network/layout.html`.
- Content is conditionally rendered based on whether the user is authenticated.

### Models

- `network/models.py` is where you define models for the application.
- A User model is provided, but you can add additional fields if needed.
- You will also create models for posts, likes, and followers.

## Specification

Implement a social network with the following features using Python, JavaScript, HTML, and CSS:

### New Post

- Signed-in users can create new text-based posts.
- Posts can be submitted via a text area and a submit button.

### All Posts

- The "All Posts" link in the navigation bar displays all posts from all users, with the most recent posts first.
- Each post shows the poster's username, post content, timestamp, and the number of likes.

### Profile Page

- Clicking on a username loads the user's profile page.
- The profile displays the user's followers and users they follow.
- All posts by the user are shown in reverse chronological order.
- For other users, a "Follow" or "Unfollow" button is displayed to toggle following.

### Following

- The "Following" link displays posts from users the current user follows.
- This page is only accessible to signed-in users.

### Pagination

- Display 10 posts per page.
- Include "Next" and "Previous" buttons for navigation.

### Edit Post

- Users can edit their own posts.
- Editing should happen without a full page reload.
- Ensure users cannot edit others' posts.

### Like and Unlike

- Users can like/unlike posts asynchronously.
- Use JavaScript to update like counts without page reloads.

## Hints

- Refer to JavaScript fetch calls from Project 3 for guidance.
- Modify `network/models.py` to define models for posts, likes, and followers.
- Utilize Django's Paginator class for server-side pagination.
- Use Bootstrap's Pagination for front-end display.

## How to Submit

1. Visit [this link](https://github.com/me50/USERNAME/tree/web50/projects/2020/x/network), replacing USERNAME with your GitHub username.
2. Ensure your code follows the specified file structure.
3. Submit your project:
   - If you have submit50 installed, execute `submit50 web50/projects/2020/x/network`.
   - Otherwise, push your work to your GitHub repository under a branch named `web50/projects/2020/x/network`.

That's it! You're ready to start building your Twitter-like social network. Happy coding!
