Meteor.methods
  'peerdb-query-database': ->
    console.log "Checking collection counts"

    console.log "Persons: #{ Person.documents.count() }, Tags: #{ Tag.documents.count() }" +
      ", Posts: #{ Post.documents.count() }, Comments: #{ Comment.documents.count() }"

    console.log "Querying all posts and content for each tag"

    start = new Date().valueOf()

    # Iterate over all tags.
    for tag in Tag.documents.find {}, fields: {name: 1}
      # We pretend that tag name is the only thing we have to begin with.
      tagName = tag.name

      # Query to get posts that include current tag.
      # Making sure I got all info for each post.
      # Make a list of dicts where each dict contains post contents.
      tpContents = for post in Post.documents.find {'tags.name': tagName}, fields: {'body': 1, 'comments.body': 1, 'author.name': 1, 'author.picture': 1, 'tags.name': 1, 'tags.description' : 1}
        body: post.body
        comments: (comment.body for comment in post.comments)
        author_name: post.author.name
        author_picture: post.author.picture
        tags_name: (tag.name for tag in post.tags)
        tags_description: (tag.description for tag in post.tags)

    (new Date().valueOf() - start) / 1000
