function fillParenId(parentId){
    $('#parent_id').val(parentId);
}

function fillProductId(productId) {
    document.getElementById('product_id').value = productId;  // Set the product ID in the hidden input
    document.getElementById('delete-form').submit();          // Submit the form
}

function fillProductIdToFavorite(productId) {
    document.getElementById('favorite-product-id').value = productId;  // Set the product ID in the hidden input
    document.getElementById('add-to-favorite-form').submit();          // Submit the form
}


// question and answer section to post the data to view 
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('qaa-form');
    
    if (!form.dataset.listenerAttached) {
        console.log('Script loaded and event listener attached.');

        form.addEventListener('submit', function(event) {
            console.log('Form submit event triggered.');

            event.preventDefault(); // Prevent the default form submission

            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true; // Disable the button to prevent multiple submissions

            const formData = new FormData(form); // Collect form data
            formData.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value);

            console.log('Starting AJAX request...');

            $.ajax({
                url: form.getAttribute('action') || 'http://127.0.0.1:8000/products/qustion-and-answer/',
                type: 'POST',
                data: formData,
                processData: false, // Prevent jQuery from processing the data
                contentType: false, // Prevent jQuery from setting the content type
                success: function(response) {
                    console.log('AJAX request successful:', response);
                    window.location.reload(); // Reload the page on success
                },
                error: function(xhr, status, error) {
                    console.error('AJAX request failed:', error);
                    submitButton.disabled = false; // Re-enable the button on error
                }
            });
        });

        form.dataset.listenerAttached = true; // Mark the listener as attached
    }
});

// comment section to post the data to view 
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('comment-form');
    // Ensure the listener is only attached once
    if (!form.dataset.listenerAttached) {
        console.log('Script loaded and event listener attached.');

        form.addEventListener('submit', function(event) {
            console.log('Form submit event triggered.');

            event.preventDefault(); // Prevent the default form submission

            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true; // Disable the button to prevent multiple submissions

            const formData = new FormData(form); // Collect form data
            formData.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value);

            console.log('Starting AJAX request...');

            $.ajax({
                url: form.getAttribute('action') || 'http://127.0.0.1:8000/products/new-comment/',
                type: 'POST',
                data: formData,
                processData: false, // Prevent jQuery from processing the data
                contentType: false, // Prevent jQuery from setting the content type
                success: function(response) {
                    console.log('AJAX request successful:', response);
                    // Optionally, you can update the page with the response instead of reloading
                    // Example: $('#response-container').html(response);
                    window.location.reload(); // Reload the page on success
                },
                error: function(xhr, status, error) {
                    console.error('AJAX request failed:', error);
                    // Optionally, display an error message to the user
                    // Example: $('#error-message').text('There was an error submitting your form.');
                    submitButton.disabled = false; // Re-enable the button on error
                }
            });
        });

        form.dataset.listenerAttached = true; // Mark the listener as attached
    }
});

// filling the stars by average rate 
function fillStars() {
    // Get the rating value from the h2 element
    const productRate = parseFloat(document.getElementById('productRate').textContent);
    
    // Get all star elements
    const stars = document.querySelectorAll('#starRating i');
    
    // Loop through each star and fill it accordingly
    stars.forEach((star, index) => {
        if (productRate >= index + 1) {
            // Fully fill the star if the rate is greater than or equal to this star index
            star.classList.remove('bi-star', 'bi-star-half');
            star.classList.add('bi-star-fill');
        } else if (productRate > index && productRate < index + 1) {
            // Half fill the star if the rate is between this star index and the next
            star.classList.remove('bi-star', 'bi-star-fill');
            star.classList.add('bi-star-half');
        } else {
            // Leave the star empty if the rate is lower
            star.classList.remove('bi-star-fill', 'bi-star-half');
            star.classList.add('bi-star');
        }
    });
}

// Run the function when the page loads
document.addEventListener('DOMContentLoaded', fillStars);


// likes and dislike section
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    headers: { "X-CSRFToken": csrftoken }
});

$(document).ready(function() {
    $('.btn-like').click(function(e) {
        e.preventDefault();
        
        var button = $(this);
        var commentId = button.data('comment-id');
        var opinion = button.data('opinion');
        
        $.ajax({
            url: 'http://127.0.0.1:8000/products/comment-likes-and-dislikes/',  // URL for the view
            type: 'POST',
            data: {
                'comment_id': commentId,
                'opinion': opinion
            },
            success: function(response) {
                if (response.status === 'success') {
                    // Update the like and dislike counts
                    $('a[data-comment-id="' + commentId + '"][data-opinion="like"]').html('<i class="bi bi-hand-thumbs-up"></i> ' + response.total_likes);
                    $('a[data-comment-id="' + commentId + '"][data-opinion="dislike"]').html('<i class="bi bi-hand-thumbs-down"></i> ' + response.total_dislikes);
                } else if (response.status === 'error') {
                    // Display the error message to the user
                    alert(response.message);
                }
            },
            error: function(xhr, status, error) {
                // Handle any other errors
                console.error("An error occurred: " + error);
                alert("An unexpected error occurred. Please try again later.");
            }
        });
    });
});


// sending values to create or add product to basket
$(document).ready(function () {
    $('#add-to-basket-button').click(function (event) {
        event.preventDefault();

        // Collect form data
        var formData = {
            'product_id': $("input[name='count-product-id']").val(),
            'color': $("input[name='options']:checked").val(),
            'count': $("input[name='count']").val(),
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val() // Include CSRF token
        };

        // Debugging: Log formData to verify values
        console.log('Form Data:', formData);

        $.ajax({
            type: 'POST',
            url: "http://127.0.0.1:8000/products/add-product-to-basket/",  // Replace with your URL
            data: formData,
            success: function(response) {
                // Handle the response from the server // Use response.message if your server returns a JSON object with a message
                if (response.success) {
                    window.location.reload();
                } else if (response.failed) {
                    alert(response.failed);
                } else {
                    // Handle any unexpected responses
                    alert('An unexpected error occurred');
                }
                    
            },
            error: function(xhr, status, error) {
                // Handle errors
                alert('An error occurred: ' + error);
            }
        });
    });
});
