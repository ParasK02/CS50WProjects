document.addEventListener("DOMContentLoaded", function () {
	document.querySelector("#new-post-view").style.display = "none";

	const newPostButton = document.querySelector("#newPost");
	if (newPostButton) {
		newPostButton.addEventListener("click", post_fields); // Pass the function reference without invoking it
	}

	document
		.querySelector("#new-post-form")
		.addEventListener("submit", create_post);
	document.querySelector("#closeForm").addEventListener("click", close_form);
});

function close_form() {
	document.querySelector("#new-post-view").style.display = "none";
	document.querySelector("#new-post-text").value = "";
}

function post_fields() {
	document.querySelector("#new-post-view").style.display = "block";
	document.querySelector("#new-post-text").value = "";
	
}

function create_post(event) {
	event.preventDefault();
	const newPostText = document.querySelector("#new-post-text").value;

	if (newPostText.trim() === "") {
		return;
	}

	document.querySelector("#new-post-view").style.display = "none";
	fetch("/posts", {
		method: "POST",
		body: JSON.stringify({
			text: document.querySelector("#new-post-text").value,
		}),
	})
		.then((response) => response.json())
		.then(() => {
			location.reload();
		})
		.catch((error) => console.log(error));
}


function followUser(user_id, follow) {
	const data = {
		followers: follow,
	};

	fetch(`/users/${user_id}`, {
		method: "PUT",
		body: JSON.stringify(data),
	})
		.then((response) => {
			if (response.status === 204) {
				if (follow) {
					console.log("User followed successfully");
				} else {
					console.log("User unfollowed successfully");
				}
				location.reload(); // Refresh the page
			} else {
				console.error("Error following/unfollowing user");
			}
		})
		.catch((error) => {
			console.error("Error following/unfollowing user:", error);
		});
}
async function isPostLiked(postId) {
	return fetch(`/posts/${postId}`)
		.then((response) => response.json())
		.then((data) => {
			const isLiked = data.liked;
			const likeCount = data.like_count; // Access the like count from the response
			return { isLiked, likeCount };
		})
		.catch((error) => {
			console.error("Error checking liked posts:", error);
			return { isLiked: false, likeCount: 0 }; // Return default values in case of an error
		});
}


function handleLikePost(postId) {
	isPostLiked(postId)
		.then(({ isLiked, likeCount }) => {
			likePost(postId, !isLiked, likeCount); // Pass the like count to likePost
		})
		.catch((error) => {
			console.error("Error handling like:", error);
		});
}

function likePost(postID, condition, likeCount) {
	console.log(postID)
	const data = {
		likes: condition,
	};

	fetch(`/posts/${postID}`, {
		method: "PUT",
		body: JSON.stringify(data),
	})
		.then((response) => {
			if (response.status === 204) {
				console.log(likeCount)
				const likeButton = document.querySelector(`#like-button-${postID}`);
				likeButton.innerHTML = likeCount + (condition? 1:-1)

			} else {
				console.error("Error updating likes");
			}
		})
		.catch((error) => {
			console.log(error);
		});
}


function editPost(postID) {
	// Find the post element by its ID
	const postElement = document.querySelector(`#post-${postID}`);

	// Get the existing post text
	const postTextElement = postElement.querySelector(".post-text");
	const postText = postTextElement.textContent;

	// Create a container div for the textarea and the button
	const containerDiv = document.createElement("div");
	containerDiv.className = "edit-container";

	// Create an editable textarea
	const editableTextarea = document.createElement("textarea");
	editableTextarea.value = postText;
	editableTextarea.className = "editable-textarea";

	// Create a "Save" button
	const saveButton = document.createElement("button");
	saveButton.textContent = "Save";
	saveButton.className = "save-button btn-primary btn";
	
	// Append the textarea and the button to the container
	containerDiv.appendChild(editableTextarea);
	containerDiv.appendChild(saveButton);

	// Replace the post text with the container
	postTextElement.replaceWith(containerDiv);

	// Add an event listener to the "Save" button
	saveButton.addEventListener("click", () => {
		const newText = editableTextarea.value;
		// Send a request to update the post text on the server
		editableTextarea.replaceWith(newText);
		saveButton.style.visibility = "none";
		updatePost(postID, newText);
		containerDiv.removeChild(saveButton)
	});
}
function updatePost(postID,text){
	fetch(`/posts/edit/${postID}`,{
		method: "PUT",
		body: JSON.stringify(text)
	}).then(response=>{
		if(response.status===204){
			console.log('Edit Sucess')
		}
		else{
			console.log("Edit can not be made")
		}
	})

}
