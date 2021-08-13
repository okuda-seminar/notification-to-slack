module.exports = (robot) ->

  robot.respond /hello/i, (msg) ->
    msg.send "bbb"
