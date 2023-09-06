document.addEventListener('DOMContentLoaded', function () {
    // Get all like icons using a common class name
    const likeIcons = document.querySelectorAll('.like-icon');

    // Add click event listeners to each like icon
    likeIcons.forEach((likeIcon) => {
        likeIcon.addEventListener('click', function () {
            const postId = this.getAttribute('data-post-id'); // Get the post ID
            handleLikes(postId, this); // Pass the post ID and the clicked icon to handleLikes
        });
    });

    function handleLikes(postId, iconElement) {
        fetch(`/post/${postId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken, // Include the CSRF token
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}),
        })
        .then(response => {
            console.log(response);
             if (response.status === 200) {
                return response.json(); // Valid JSON response
            } else if (response.status === 302) {
                // Redirect response, extract the redirect URL
                const redirectUrl = response.headers.get('Location');
                if (redirectUrl && redirectUrl.includes('login')) {
                    // Redirect the user to the new URL
                    console.log('redirecting to:', redirectUrl);
                    window.location.href = redirectUrl;
            }
        } else {
            console.log('Handle other response statuses here');
        }
        })
        .then(data => {
            if (data.liked) {
                iconElement.style.color = 'blue'; // Change the color to blue when liked
                console.log('I am liked', data.id);
                // Show the corresponding opposite icon if needed (e.g., dislike)
            } else {
                iconElement.style.color = 'black'; // Change the color to black when not liked
                console.log('I am disliked')
                // Hide the corresponding opposite icon if needed (e.g., dislike)
            }

            const countLikes = data.countLikes;
            console.log(countLikes);

            const countBadge = document.getElementById(`count-badge-${postId}`);
            if (countBadge) {
                countBadge.textContent = countLikes;
            }
        })
        .catch(error => {
            // Handle any errors here
            console.error(error);
         });
    }
});


