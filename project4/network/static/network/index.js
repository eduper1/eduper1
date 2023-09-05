const likeId = document.getElementById('like-icon');
const postId = likeId.getAttribute('data-post-id');
const dislikeId = document.getElementById('unlike-icon');
const dispostId = dislikeId.getAttribute('data-post-id');

document.addEventListener('DOMContentLoaded',function(){

    function handleLikes(postId){
        fetch(`post/${postId}`,{
            method:'POST',
            headers: {
                'X-CSRFToken': csrfToken, // Include the CSRF token
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}),
        })
        .then(response => response.json())
        .then(data => {
            if (data.liked){
                likeId.style.display = 'none';
                dislikeId.style.display = 'block';
            }else{
                dislikeId.style.display = 'none';
                likeId.style.display =  'block';
            }
        })
    }
})
