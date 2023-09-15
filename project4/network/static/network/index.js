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
            if (response.status === 302) {
                // Get the redirect URL from the 'Location' header
                //  this ain't working
                const redirectUrl = response.headers.get('Location');

                if (redirectUrl) {
                    // Redirect the user to the specified URL
                    console.log(redirectUrl);
                    window.location.href = redirectUrl;
                    return;
                }
            } else if (response.status === 200) {
                // Handle a successful response
                return response.json();
            } else {
                // Handle other response status codes
                console.error(`Unexpected status code: ${response.status}`);
            }
        })
        .then(data => {
            // console.log(data.error);
            if (data.error) {
                // Redirect the user to the login URL with the 'next' parameter
                return; // Return to exit further execution
            } else if (data.liked) {
                iconElement.style.color = 'blue'; // Change the color to blue when liked
            } else {
                iconElement.style.color = 'black'; // Change the color to black when not liked
            }

            const countLikes = data.countLikes;

            const countBadge = document.getElementById(`count-badge-${postId}`);
            if (countBadge) {
                countBadge.textContent = countLikes;
            }

            // this block not working
            if (data.redirect_url) {
                console.error(data.redirect_url);
                window.location.href = response.headers.get('Location');
                return; // Return to exit further execution
            }
        })
        .catch(error => {
            // Handle any errors here
            // console.error(error);
         });
    }

    console.log(document.querySelector('.card-text').textContent);
    // handle editPost
        // Add click event listeners to all "Edit" buttons
    const editButtons = document.querySelectorAll('.edit-btn');

    editButtons.forEach((editButton) => {
        console.log('I am clicked', editButton);
        editButton.addEventListener('click', function () {
            const editPostId = this.getAttribute('data-editPost-id');
            const postElement = document.getElementById(`post-card-${editPostId}`);
            
            if (postElement) {

                // Create a textarea for editing
                const textarea = document.createElement('textarea');
                // textarea.value = postContent;
                textarea.value = postElement.textContent;
                textarea.setAttribute('rows', '4');

                // Create a "Save" button
                const saveButton = document.createElement('button');
                saveButton.textContent = 'Save';

                // Replace the post content with the textarea and save button
                postElement.innerHTML = '';
                postElement.appendChild(textarea);
                postElement.appendChild(saveButton);

                // Add a click event listener to the "Save" button
                saveButton.addEventListener('click', function () {
                    const updatedContent = textarea.value;

                    // Send an AJAX request to update the post content
                    fetch(`/editPost/${editPostId}`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'Content-Type': 'application/json',
                        },
                        mode:'same-origin',
                        body: JSON.stringify({ content: updatedContent }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Replace the textarea with the updated post content
                            postElement.innerHTML = `<p>${updatedContent}</p>`;
                        } else {
                            console.error('Failed to update post.');
                        }
                    })
                    .catch(error => {
                        console.error(error);
                    });
                });
            }
        });
    });
});


