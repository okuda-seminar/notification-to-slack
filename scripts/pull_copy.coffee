module.exports = (robot) ->

  github = require("githubot")(robot)

  unless (url_api_base = process.env.HUBOT_GITHUB_API)?
    url_api_base = "https://api.github.com"

  robot.respond /showpr\s+(me\s+)?(.*)\s+pulls(\s+with\s+)?(.*)?/i, (msg)->
    repo = github.qualified_repo msg.match[2]
    filter_reg_exp = new RegExp(msg.match[4], "i") if msg.match[3]
    summary = ""

    github.get "#{url_api_base}/repos/#{repo}/pulls", (pulls) ->
      if pulls.length == 0
        summary = "Achievement unlocked: open pull requests zero!"
      else
        for pull in pulls
          for reviewer in pull.requested_reviewers
            if "#{reviewer.login}" == "tkkawa"
              summary = summary + "\n\t#{pull.title} - #{pull.user.login}: #{pull.html_url}"
              
      msg.send summary

