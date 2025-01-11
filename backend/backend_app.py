from flask import Flask, jsonify, request
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
@app.route('/api/posts', methods=['POST'])
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
            return jsonify(
                {"error": f"Missing fields: {', '.join(missing_fields)}"}
            ), 400

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
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS  # Use global to modify the POSTS list
    # Find the post by ID
    post = next((post for post in POSTS if post["id"] == post_id), None)

    if post:
        # Remove the post from the list
        POSTS = [p for p in POSTS if p["id"] != post_id]
        return jsonify(
            {"message": f"Post with id {post_id} "
                        f"has been deleted successfully."}
        ), 200
    else:
        # Post not found
        return jsonify({"error": f"Post with id {post_id} not found."}), 404


# Update Endpoint: Update a post by ID
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    # Find the post by ID
    post = next((post for post in POSTS if post["id"] == post_id), None)

    if not post:
        # Post not found
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    # Parse JSON data from request body
    data = request.json

    # Update fields only if provided in the request body
    # Use current title if not provided
    title = data.get('title', post['title'])
    # Use current content if not provided
    content = data.get('content', post['content'])

    # Update the post
    post['title'] = title
    post['content'] = content

    # Return updated post with status code 200 OK
    return jsonify(post), 200


# Search Endpoint: Search posts by title or content
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    # Get query parameters
    title_query = request.args.get('title', '').strip().lower()
    content_query = request.args.get('content', '').strip().lower()

    # Filter posts based on the queries
    filtered_posts = POSTS

    if title_query:
        filtered_posts = [
            post for post in filtered_posts
            if title_query in post['title'].lower()
        ]

    if content_query:
        filtered_posts = [
            post for post in filtered_posts
            if content_query in post['content'].lower()
        ]

    # Return the filtered posts as JSON
    return jsonify(filtered_posts), 200


# List Endpoint with Sorting
@app.route('/api/posts/sorted', methods=['GET'])
def get_sorted_posts():
    sort_field = request.args.get('sort', 'title')
    sort_direction = request.args.get('direction', 'asc')

    if sort_field not in ['title', 'content']:
        return jsonify({"error": f"Invalid sort field: {sort_field}"}), 400

    reverse = (sort_direction == 'desc')
    sorted_posts = sorted(
        POSTS, key=lambda x: x[sort_field].lower(), reverse=reverse
    )
    return jsonify(sorted_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True, )
