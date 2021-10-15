module.exports = (robot) ->

  class PullRequest
    filter_reviewer: (slack_user_id, repo) ->
      {PythonShell} = require('python-shell');
      pyshell = new PythonShell('./scripts/read_pr.py');
      pyshell.send([slack_user_id, repo]);
      pyshell.on('pr_titles', (pr_titles)->
        msg.send pr_titles
      )

  main = (slack_user_id, repo) ->
    pr_titles = new PullRequest().filter_reviewer(slack_user_id, repo)
    return pr_titles

  github = require("githubot")(robot)

  unless (url_api_base = process.env.HUBOT_GITHUB_API)?
    url_api_base = "https://api.github.com"

  robot.respond /showpr_test\s+(me\s+)?(.*)\s+pulls(\s+with\s+)?(.*)?/i, (msg)->
    repo = github.qualified_repo msg.match[2]
    slack_user_id = msg.message.user.id;
    message = main(slack_user_id, repo)
    msg.send message