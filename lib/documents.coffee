# This file defines PeerDB based documents.

class @Person extends Document
  # name
  # username
  # bio

  @Meta
    name: 'Person'

class @Tag extends Document
  # name
  # description

  @Meta
    name: 'Tag'

class @Post extends Document
  # author
  # tags
  # body
  # comments: reverse field of Comment.post

  @Meta
    name: 'Post'
    fields: =>
      author: @ReferenceField Person
      tags: [@ReferenceField Tag]

class @Comment extends Document
  # body
  # post

  @Meta
    name: 'Comment'
    fields: =>
      post: @ReferenceField Post, [], true, 'comments'
