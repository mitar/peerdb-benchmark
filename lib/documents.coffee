# This file defines PeerDB based documents.

class @Person extends Document
  # username

  @Meta
    name: 'Person'

class @Tag extends Document
  # name

  @Meta
    name: 'Tag'

class @Post extends Document
  # body

  @Meta
    name: 'Post'
    fields: =>
      author: @ReferenceField Person
      tags: [@ReferenceField Tag]

class @Comment extends Document
  # body

  @Meta
    name: 'Comment'
    fields: =>
      post: @ReferenceField Post, [], true, 'comments'
