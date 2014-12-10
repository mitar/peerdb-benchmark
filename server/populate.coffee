Future = Npm.require 'fibers/future'

NUMBER_OF_PERSONS = 100
NUMBER_OF_TAGS = 100
NUMBER_OF_POSTS = 1000
NUMBER_OF_TAGS_PER_POST = 10
NUMBER_OF_COMMENTS = 10000

# This timeout should be substracted when timinig the full wait period.
WAIT_FOR_DATABASE_TIMEOUT = 2500 # ms

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
      observerCallbackCalled()
      ret = f args...
      observerCallbackCalled()
      ret

Document._observerCallback

populateDatabase = (commentClass, postClass, personClass, tagClass) ->
  console.log "Cleaning the database"

  commentClass.remove {}
  postClass.remove {}
  personClass.remove {}
  tagClass.remove {}

  console.log "Done"

  Meteor.call 'wait-for-database'

  console.log "Adding #{ NUMBER_OF_PERSONS } persons"

  persons = for person in [0...NUMBER_OF_PERSONS]
    personClass.insert
      username: "username#{ person }"

  console.log "Done"

  console.log "Adding #{ NUMBER_OF_TAGS } tags"

  tags = for tag in [0...NUMBER_OF_TAGS]
    tagClass.insert
      name: "tag#{ tag }"

  console.log "Done"

  console.log "Adding #{ NUMBER_OF_POSTS } posts"

  posts = for post in [0...NUMBER_OF_POSTS]
    postClass.insert
      body: "Body content for post #{ post }."
      author:
        _id: _.sample persons
      tags: (_id: tagId for tagId in _.sample tags, NUMBER_OF_TAGS_PER_POST)

  console.log "Done"

  console.log "Adding #{ NUMBER_OF_COMMENTS } comments"

  comments = for comment in [0...NUMBER_OF_COMMENTS]
    commentClass.insert
      body: "Body content for comment #{ comment }."
      post:
        _id: _.sample posts

  console.log "Done"

  Meteor.call 'wait-for-database'

Meteor.methods
  'peerdb-populate-database': ->
    populateDatabase Comment.documents, Post.documents, Person.documents, Tag.documents

  'collections-populate-database': ->
    populateDatabase commentsCollection, postsCollection, personsCollection, tagsCollection

  'wait-for-database': ->
    console.log "Waiting for database"

    future = new Future()
    observerCallbackCalledFutures.push future

    # We make sure it is called at least once.
    observerCallbackCalled()

    future.wait()

    console.log "Done"
