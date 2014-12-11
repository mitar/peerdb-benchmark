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

  'collection-query-database': ->
    console.log "Checking collection counts"

    console.log "Persons: #{ personsCollection.count() }, Tags: #{ tagsCollection.count() }" +
      ", Posts: #{ postsCollection.count() }, Comments: #{ commentsCollection.count() }"

    console.log "Querying all posts and content for each tag"

    start = new Date().valueOf()

    for tag in tagsCollection.find {}, fields: {'name': 1}
      # We pretend that tag name is the only thing we have to begin with.
      tagName = tag['name']

      # Get the tag.
      tag = tagsCollection.findOne {'name': tagName}, fields: {'_id': 1}

      # Query to get posts that include current tag.
      tp = postsCollection.find({'tags': tag['_id']}, fields: {'body': 1, 'author': 1, 'tags': 1}).fetch()

      # Query to get authors for all posts.
      tpAuthors = {}
      personsCollection.find({'_id': {'$in': (post['author'] for post in tp)}}, fields: {'name': 1, 'picture': 1}).forEach (person) ->
        tpAuthors[person['_id']] = person

      # Query to get comment body for all comments of all posts.
      tpComments = {}
      commentsCollection.find({'post': {'$in': (post['_id'] for post in tp)}}, fields: {'body': 1, 'post': 1}).forEach (comment) ->
        unless comment['post'] of tpComments
          tpComments[comment['post']] = []
        tpComments[comment['post']].push comment['body']

      list_of_all_tags_ids = _.flatten (post['tags'] for post in tp)
      # Query to get post tag names and descriptions for all posts.
      tpTags = {}
      tagsCollection.find({'_id': {'$in': list_of_all_tags_ids}}, fields: {'name': 1, 'description': 1}).forEach (tag) ->
        tpTags[tag['_id']] = tag

      # Making sure I got all info for each post.
      # Make a list of dicts where each dict contains post contents.
      tpContents = for post in tp
        body: post.body
        comments: tpComments[post._id] or []
        author_name: tpAuthors[post.author].name
        author_pic: tpAuthors[post.author].picture
        tags_name: (tpTags[tagId].name for tagId in post.tags)
        tags_description: (tpTags[tagId].description for tagId in post.tags)

    (new Date().valueOf() - start) / 1000
