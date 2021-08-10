module.exports = (robot) ->

  robot.respond /a/i, (msg) ->
    msg.send "bbb"
