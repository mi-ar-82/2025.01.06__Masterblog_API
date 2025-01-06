from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


# Add Endpoint: Create a new post
@app.route('/api/posts', methods = ['POST'])
def add_post():
    try:
        # Parse JSON data from request body
        data = request.json
        
        # Validate input fields
        if not data or 'title' not in data or 'content' not in data:
            missing_fields = []
            if 'title' not in data:
                missing_fields.append('title')
            if 'content' not in data:
                missing_fields.append('content')
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
        
        # Generate a new unique ID
        new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
        
        # Create new post
        new_post = {
            "id": new_id,
            "title": data['title'],
            "content": data['content']
        }
        
        # Add to POSTS list
        POSTS.append(new_post)
        
        # Return the newly created post with status code 201 (Created)
        return jsonify(new_post), 201
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500


# Delete Endpoint: Delete a post by ID
@app.route('/api/posts/<int:post_id>', methods = ['DELETE'])
def delete_post(post_id):
    global POSTS  # Use global to modify the POSTS list
    # Find the post by ID
    post = next((post for post in POSTS if post["id"] == post_id), None)
    
    if post:
        # Remove the post from the list
        POSTS = [p for p in POSTS if p["id"] != post_id]
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200
    else:
        # Post not found
        return jsonify({"error": f"Post with id {post_id} not found."}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
