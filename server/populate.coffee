Future = Npm.require 'fibers/future'

# This timeout should be subtracted when timing the full wait period.
WAIT_FOR_DATABASE_TIMEOUT = 6000 # ms

observerCallbackCalledCount = 0
observerCallbackCalledFutures = []

observerCallbackCalled = _.debounce ->
  futures = observerCallbackCalledFutures
  observerCallbackCalledFutures = []
  for future in futures when not future.isResolved()
    future.return()
,
  WAIT_FOR_DATABASE_TIMEOUT

originalObserverCallback = null
unless originalObserverCallback
  originalObserverCallback = Document._observerCallback
  Document._observerCallback = (f) ->
    originalObserverCallback (args...) ->
      observerCallbackCalledCount++
      observerCallbackCalled()
      ret = f args...
      observerCallbackCalled()
      ret

# To match the function name in other implementations.
charGenerator = Random.secret

# Input: ordered objects, object_ids, fields to embed besides id, n
# Output: PeerDB compatible objects to embed
randomObjects = (objects, objectIds, fields, n) ->
  assert objects.length is objectIds.length
  lengthObjects = objects.length

  for i in [0...n]
    # TODO: It is possible that same objectI is selected multiple times, we should do something better here, similar to Python implementation
    objectI = Math.floor(Random.fraction() * lengthObjects)
    obj = _id: objectIds[objectI]
    for field in fields
      obj[field] = objects[objectI][field]
    out

Meteor.methods
  'peerdb-populate-database': (settings) ->
    NUMBER_OF_PERSONS = settings['NUMBER']['PERSONS']
    NUMBER_OF_TAGS = settings['NUMBER']['TAGS']
    NUMBER_OF_POSTS = settings['NUMBER']['POSTS']
    NUMBER_OF_TAGS_PER_POST = settings['NUMBER']['TAGS_PER_POST']
    NUMBER_OF_COMMENTS = settings['NUMBER']['COMMENTS']

    PERSON_NAME_SIZE = settings['SIZE']['PERSON_NAME']
    PERSON_BIO_SIZE = settings['SIZE']['PERSON_BIO']
    PERSON_PICTURE_SIZE = settings['SIZE']['PERSON_PICTURE']
    TAG_NAME_SIZE = settings['SIZE']['TAG_NAME']
    TAG_DESCRIPTION_SIZE = settings['SIZE']['TAG_DESCRIPTION']
    POST_BODY_SIZE = settings['SIZE']['POST_BODY']
    COMMENT_BODY_SIZE = settings['SIZE']['COMMENT_BODY']

    console.log "Cleaning the database"

    Comment.documents.remove {}
    Post.documents.remove {}
    Person.documents.remove {}
    Tag.documents.remove {}

    console.log "Done"

    Meteor.call 'wait-for-database'

    Meteor.call 'reset-observe-callback-count'

    console.log "Adding #{ NUMBER_OF_PERSONS } persons"

    start = new Date().valueOf()

    persons = []
    personIds = for person in [0...NUMBER_OF_PERSONS]
      person =
        name: charGenerator PERSON_NAME_SIZE
        bio: charGenerator PERSON_BIO_SIZE
        picture: charGenerator PERSON_PICTURE_SIZE
      persons.push person
      Person.documents.insert person

    console.log "Done"

    console.log "Adding #{ NUMBER_OF_TAGS } tags"

    tags = []
    tagIds = for tag in [0...NUMBER_OF_TAGS]
      tag =
        name: charGenerator TAG_NAME_SIZE
        description: charGenerator TAG_DESCRIPTION_SIZE
      tags.push tag
      Tag.documents.insert tag

    console.log "Done"

    console.log "Adding #{ NUMBER_OF_POSTS } posts"

    posts = []
    postIds = for post in [0...NUMBER_OF_POSTS]
      post =
        author: randomObjects(persons, personIds, ['name', 'picture'], 1)[0]
        body: charGenerator POST_BODY_SIZE
        tags: randomObjects(tags, tagIds, ['name', 'description'], NUMBER_OF_TAGS_PER_POST)
      posts.push post
      Post.documents.insert post

    console.log "Done"

    console.log "Adding #{ NUMBER_OF_COMMENTS } comments"

    comments = []
    commentIds = for comment in [0...NUMBER_OF_COMMENTS]
      comment =
        body: charGenerator COMMENT_BODY_SIZE
        post:
          # TODO: We should use here some long-tail distribution (20% of posts has 80% of comments)
          _id: _.sample postIds
      comments.push comment
      Comment.documents.insert comment

    console.log "Done"

    writeTime = new Date().valueOf()

    Meteor.call 'wait-for-database'

    callbackCount = Meteor.call 'reset-observe-callback-count'

    console.log "#{ callbackCount } PeerDB updates made"

    endTime = new Date().valueOf()
    [
      (writeTime - start) / 1000
      # We subtract WAIT_FOR_DATABASE_TIMEOUT, an overhead made by wait-for-database.
      (endTime - start - WAIT_FOR_DATABASE_TIMEOUT) / 1000
    ]

  'collections-populate-database': (settings) ->
    NUMBER_OF_PERSONS = settings['NUMBER']['PERSONS']
    NUMBER_OF_TAGS = settings['NUMBER']['TAGS']
    NUMBER_OF_POSTS = settings['NUMBER']['POSTS']
    NUMBER_OF_TAGS_PER_POST = settings['NUMBER']['TAGS_PER_POST']
    NUMBER_OF_COMMENTS = settings['NUMBER']['COMMENTS']

    PERSON_NAME_SIZE = settings['SIZE']['PERSON_NAME']
    PERSON_BIO_SIZE = settings['SIZE']['PERSON_BIO']
    PERSON_PICTURE_SIZE = settings['SIZE']['PERSON_PICTURE']
    TAG_NAME_SIZE = settings['SIZE']['TAG_NAME']
    TAG_DESCRIPTION_SIZE = settings['SIZE']['TAG_DESCRIPTION']
    POST_BODY_SIZE = settings['SIZE']['POST_BODY']
    COMMENT_BODY_SIZE = settings['SIZE']['COMMENT_BODY']

    console.log "Cleaning the database"

    commentsCollection.remove {}
    postsCollection.remove {}
    personsCollection.remove {}
    tagsCollection.remove {}

    console.log "Done"

    console.log "Adding #{ NUMBER_OF_PERSONS } persons"

    start = new Date().valueOf()

    persons = []
    personIds = for person in [0...NUMBER_OF_PERSONS]
      person =
        name: charGenerator PERSON_NAME_SIZE
        bio: charGenerator PERSON_BIO_SIZE
        picture: charGenerator PERSON_PICTURE_SIZE
      persons.push person
      personsCollection.insert person

    console.log "Done"

    console.log "Adding #{ NUMBER_OF_TAGS } tags"

    tags = []
    tagIds = for tag in [0...NUMBER_OF_TAGS]
      tag =
        name: charGenerator TAG_NAME_SIZE
        description: charGenerator TAG_DESCRIPTION_SIZE
      tags.push tag
      tagsCollection.insert tag

    console.log "Done"

    console.log "Adding #{ NUMBER_OF_POSTS } posts"

    posts = []
    postIds = for post in [0...NUMBER_OF_POSTS]
      post =
        author: _.sample personIds
        body: charGenerator POST_BODY_SIZE
        tags: _.sample tagIds, NUMBER_OF_TAGS_PER_POST
      posts.push post
      postsCollection.insert post

    console.log "Done"

    console.log "Adding #{ NUMBER_OF_COMMENTS } comments"

    comments = []
    commentIds = for comment in [0...NUMBER_OF_COMMENTS]
      comment =
        body: charGenerator COMMENT_BODY_SIZE
        # TODO: We should use here some long-tail distribution (20% of posts has 80% of comments)
        post: _.sample postIds
      comments.push comment
      commentsCollection.insert comment

    console.log "Done"

    (new Date().valueOf() - start) / 1000

  'reset-observe-callback-count': ->
    old = observerCallbackCalledCount
    observerCallbackCalledCount = 0
    old

  'wait-for-database': ->
    console.log "Waiting for database"

    future = new Future()
    observerCallbackCalledFutures.push future

    # We make sure it is called at least once.
    observerCallbackCalled()

    future.wait()

    console.log "Done"

    observerCallbackCalledCount
